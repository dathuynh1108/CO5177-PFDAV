"""VietnamNet headlines: TF-IDF baselines and frozen PhoBERT features."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from studies.evidence import (
    ROOT,
    download,
    figures,
    metrics,
    save_models,
    seal,
    source_identity,
    write_json,
)


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def canonical_url(value: str) -> str:
    url = urlsplit(value)
    if url.hostname not in {"vietnamnet.vn", "www.vietnamnet.vn"}:
        raise ValueError("Unexpected article host")
    return urlunsplit(("https", "vietnamnet.vn", url.path.rstrip("/"), "", ""))


def deduplicate(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Group identical URLs, headlines or article bodies before splitting."""
    parent = list(range(len(frame)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    seen = {}
    for i, row in enumerate(frame.itertuples()):
        keys = [("url", row.url), ("headline", normalize(row.title).casefold())]
        if hasattr(row, "content") and row.content:
            body_hash = hashlib.sha256(
                normalize(row.content).casefold().encode()
            ).hexdigest()
            keys.append(("body", body_hash))
        for key in keys:
            if key in seen:
                parent[find(i)] = find(seen[key])
            else:
                seen[key] = i
    groups = np.array([find(i) for i in range(len(frame))])
    work = frame.copy()
    work["group"] = groups
    conflict = work.groupby("group")["category"].transform("nunique") > 1
    duplicate = work["group"].duplicated()
    keep = ~conflict & ~duplicate
    retained = work.loc[keep].drop(columns="group").reset_index(drop=True)
    return retained, {
        "conflicting_category_rows_removed": int(conflict.sum()),
        "duplicate_rows_removed_after_conflicts": int((duplicate & ~conflict).sum()),
    }


def prepare(config: dict) -> tuple[pd.DataFrame, dict]:
    records = []
    lengths = []
    classes = Counter()
    empty = 0
    raw = 0
    for name, lock in config["files"].items():
        url = f"https://huggingface.co/datasets/{config['dataset']}/resolve/{config['revision']}/{name}"
        path = download(url, ROOT / "data/vietnamnet" / name, lock["sha256"])
        parquet = pq.ParquetFile(path)
        if set(parquet.schema_arrow.names) != {"class", "url", "title", "content"}:
            raise ValueError(f"Unexpected news schema: {name}")
        for batch in parquet.iter_batches(batch_size=512):
            for row in batch.to_pylist():
                raw += 1
                classes[row["class"]] += 1
                title = normalize(row["title"] or "")
                lengths.append(len(row["content"] or ""))
                if not title:
                    empty += 1
                    continue
                url_value = canonical_url(row["url"])
                identity = hashlib.sha256(
                    (url_value + "\n" + title.casefold()).encode()
                ).hexdigest()
                records.append(
                    {
                        "id": identity,
                        "category": row["class"],
                        "url": url_value,
                        "title": title,
                        "content": normalize(row["content"] or ""),
                    }
                )
    frame, duplicate_audit = deduplicate(pd.DataFrame(records))
    selected = frame.sort_values("id").reset_index(drop=True)
    if len(selected) < 2000 or selected["category"].nunique() != len(config["files"]):
        raise ValueError("Text cohort fails sample-count or category coverage contract")
    audit_data = {
        "raw_rows": raw,
        "raw_class_counts": dict(sorted(classes.items())),
        "empty_headlines_removed": empty,
        **duplicate_audit,
        "unique_usable_rows": len(frame),
        "modeling_rows": len(selected),
        "selected_class_counts": {
            k: int(v)
            for k, v in selected["category"].value_counts().sort_index().items()
        },
        "body_length_quantiles": {
            str(q): float(np.quantile(lengths, q))
            for q in [0, 0.25, 0.5, 0.75, 0.95, 1]
        },
        "empty_bodies_retained": int((selected["content"] == "").sum()),
        "input": "Shared full-article cohort; headline baseline uses titles only, fine-tuning uses titles and bodies. URLs and category strings are excluded from model inputs",
        "sampling": "None; all usable records after documented quality checks are retained",
        "duplicate_scope": "Connected components of canonical URL OR normalized casefolded headline OR nonempty normalized casefolded body; conflicting-category components removed",
    }
    return selected, audit_data


def segmented_headlines(frame: pd.DataFrame) -> list[str]:
    from pyvi import ViTokenizer

    texts = [ViTokenizer.tokenize(title) for title in frame["title"]]
    # The actual segmented inputs also need to remain unique after segmentation.
    if len({t.casefold() for t in texts}) != len(texts):
        raise ValueError(
            "Word segmentation merged distinct input identities; revise grouping before splitting"
        )
    return texts


def _model_texts(title: str, body: str) -> tuple[str, str]:
    from pyvi import ViTokenizer

    words = body.split()
    if len(words) > 300:
        body = " ".join(words[:220] + words[-80:])
    article = unicodedata.normalize("NFC", f"{title} {body}").lower()
    article = re.sub(r"[^\w\s]|[0-9]+", " ", article, flags=re.UNICODE)
    article = ViTokenizer.tokenize(" ".join(article.split()))
    return ViTokenizer.tokenize(title), article


def prepare_inputs(frame: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, dict]:
    """Construct both model inputs and group token-identical articles before splitting."""
    from joblib import Parallel, delayed
    from transformers import AutoTokenizer

    from studies.evidence import sha256

    identity = {
        "article_ids_sha256": hashlib.sha256(
            "\n".join(frame["id"]).encode()
        ).hexdigest(),
        "source_sha256": sha256(Path(__file__)),
        "data_revision": config["revision"],
        "model_revision": config["model_revision"],
        "headline_max_tokens": config["max_length"],
        "article_max_tokens": 256,
    }
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    cache = ROOT / "data/text-inputs" / key
    path = cache / "inputs.parquet"
    metadata_path = cache / "metadata.json"
    if path.is_file() and metadata_path.is_file():
        audit = json.loads(metadata_path.read_text())
        if sha256(path) != audit["inputs_sha256"]:
            raise ValueError("Prepared input checksum mismatch")
        inputs = pd.read_parquet(path)
        if inputs["id"].tolist() != frame["id"].tolist():
            raise ValueError("Prepared input article IDs differ")
        result = frame.copy()
        for column in ("headline_text", "article_text", "input_group"):
            result[column] = inputs[column].to_numpy()
        return result, audit

    workers = min(8, os.cpu_count() or 1)
    print(
        f"Preparing both model inputs for all {len(frame):,} articles with {workers} workers",
        flush=True,
    )
    texts = Parallel(n_jobs=workers)(
        delayed(_model_texts)(title, body)
        for title, body in zip(frame["title"], frame["content"])
    )
    result = frame.copy()
    result["headline_text"] = [pair[0] for pair in texts]
    result["article_text"] = [pair[1] for pair in texts]
    tokenizer = AutoTokenizer.from_pretrained(
        config["phobert"], revision=config["model_revision"], use_fast=False
    )
    parent = list(range(len(result)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    seen = {}
    for i, (headline, article) in enumerate(texts):
        headline_ids = tokenizer.encode(
            headline, max_length=config["max_length"], truncation=True
        )
        article_ids = tokenizer.encode(
            article, add_special_tokens=False, truncation=False
        )
        if len(article_ids) > 254:
            article_ids = article_ids[:127] + article_ids[-127:]
        article_ids = [tokenizer.cls_token_id] + article_ids + [tokenizer.sep_token_id]
        for kind, ids in (("headline", headline_ids), ("article", article_ids)):
            digest = hashlib.sha256(np.asarray(ids, dtype="<i4").tobytes()).digest()
            token_key = (kind, digest)
            if token_key in seen:
                parent[find(i)] = find(seen[token_key])
            else:
                seen[token_key] = i
        if (i + 1) % 25000 == 0:
            print(f"Grouped token inputs: {i + 1:,}/{len(result):,}", flush=True)
    result["input_group"] = [find(i) for i in range(len(result))]
    sizes = result.groupby("input_group").size()
    cache.mkdir(parents=True, exist_ok=True)
    result[["id", "headline_text", "article_text", "input_group"]].to_parquet(
        path, index=False
    )
    audit = {
        **identity,
        "input_rows": len(result),
        "input_groups": len(sizes),
        "groups_with_multiple_articles": int((sizes > 1).sum()),
        "largest_group": int(sizes.max()),
        "grouping": "Union of equal final headline token IDs or final Head-Tail article token IDs",
        "rows_removed": 0,
        "preprocessing_workers": workers,
        "inputs_sha256": sha256(path),
    }
    write_json(metadata_path, audit)
    return result, audit


def split_indices(frame: pd.DataFrame, config: dict) -> dict[str, np.ndarray]:
    """Assign whole input groups to approximately 70/15/15 stratified partitions."""
    folds = StratifiedGroupKFold(
        n_splits=20, shuffle=True, random_state=config["split_seed"]
    )
    fold_id = np.empty(len(frame), dtype=np.int64)
    for number, (_, heldout) in enumerate(
        folds.split(np.zeros(len(frame)), frame["category"], frame["input_group"])
    ):
        fold_id[heldout] = number
    return {
        "train": np.flatnonzero(fold_id < 14),
        "validation": np.flatnonzero((fold_id >= 14) & (fold_id < 17)),
        "test": np.flatnonzero(fold_id >= 17),
    }


def embeddings(texts: list[str], config: dict) -> tuple[np.ndarray, dict]:
    import torch
    from transformers import AutoModel, AutoTokenizer

    from studies.evidence import sha256

    encoder_source = sha256(Path(__file__))

    key = hashlib.sha256(
        json.dumps(
            {
                "texts": texts,
                "model": config["phobert"],
                "revision": config["model_revision"],
                "max_length": config["max_length"],
                "pooling": "attention-mask mean including BOS/EOS",
                "encoder_source_sha256": encoder_source,
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode()
    ).hexdigest()
    cache = ROOT / "data/text-features" / key
    cache.mkdir(parents=True, exist_ok=True)
    features_path = cache / "features.npy"
    meta_path = cache / "metadata.json"
    if features_path.exists() and meta_path.exists():
        from studies.evidence import sha256

        meta = json.loads(meta_path.read_text())
        if sha256(features_path) != meta["features_sha256"]:
            raise ValueError("Cached PhoBERT feature checksum mismatch")
        array = np.load(features_path, allow_pickle=False)
        if array.shape != (len(texts), 768) or not np.isfinite(array).all():
            raise ValueError("Invalid cached feature shape or values")
        return array, meta
    device = config["device"]
    if device == "auto":
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available() else "cpu"
        )
    if device not in {"cpu", "mps", "cuda"}:
        raise ValueError("Unsupported explicit inference device")
    torch.set_num_threads(config["cpu_threads"])
    tokenizer = AutoTokenizer.from_pretrained(
        config["phobert"],
        revision=config["model_revision"],
        use_fast=False,
        trust_remote_code=False,
    )
    model = (
        AutoModel.from_pretrained(
            config["phobert"],
            revision=config["model_revision"],
            trust_remote_code=False,
            add_pooling_layer=False,
        )
        .to(device)
        .eval()
    )
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    arrays = []
    truncated = 0
    started = time.monotonic()
    with torch.inference_mode():
        for start in range(0, len(texts), config["batch_size"]):
            batch = texts[start : start + config["batch_size"]]
            lengths = [len(tokenizer.encode(text, truncation=False)) for text in batch]
            truncated += sum(length > config["max_length"] for length in lengths)
            inputs = tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=config["max_length"],
            ).to(device)
            hidden = model(**inputs).last_hidden_state
            mask = inputs["attention_mask"].unsqueeze(-1)
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1)
            arrays.append(pooled.cpu().numpy().astype(np.float32))
            if start % 512 == 0:
                print(
                    f"PhoBERT features: {start + len(batch)}/{len(texts)}", flush=True
                )
    array = np.concatenate(arrays)
    if array.shape != (len(texts), 768) or not np.isfinite(array).all():
        raise ValueError("Invalid PhoBERT feature shape or values")
    np.save(features_path, array, allow_pickle=False)
    from huggingface_hub import hf_hub_download

    from studies.evidence import sha256

    model_artifacts = {}
    for filename in ["pytorch_model.bin", "config.json", "vocab.txt", "bpe.codes"]:
        path = hf_hub_download(
            config["phobert"],
            filename,
            revision=config["model_revision"],
            local_files_only=True,
        )
        model_artifacts[filename] = sha256(Path(path))
    meta = {
        "model": config["phobert"],
        "revision": config["model_revision"],
        "device": device,
        "feature_cache_sha256": key,
        "encoder_source_sha256": encoder_source,
        "features_sha256": sha256(features_path),
        "rows": len(texts),
        "max_length": config["max_length"],
        "batch_size": config["batch_size"],
        "pooling": "Attention-mask mean including BOS/EOS",
        "frozen": True,
        "model_artifacts_sha256": model_artifacts,
        "segmentation": "pyvi.ViTokenizer",
        "truncated_headlines": truncated,
        "encoding_seconds": time.monotonic() - started,
    }
    write_json(meta_path, meta)
    del model
    return array, meta


def run() -> dict:
    sources = source_identity("text")
    config = json.loads((ROOT / "configs/text.json").read_text())
    output = ROOT / "reports/text/generated"
    output.mkdir(parents=True, exist_ok=True)
    frame, data_audit = prepare(config)
    frame, input_audit = prepare_inputs(frame, config)
    data_audit["model_input_grouping"] = input_audit
    texts = frame["headline_text"].to_numpy(dtype=object)
    labels = sorted(frame["category"].unique())
    label_ids = {label: i for i, label in enumerate(labels)}
    target = frame["category"].map(label_ids).to_numpy()
    indices = split_indices(frame, config)
    train, val, test = (indices[name] for name in ("train", "validation", "test"))
    splits = {
        name: frame.iloc[idx]["id"].tolist()
        for name, idx in [("train", train), ("validation", val), ("test", test)]
    }
    write_json(output / "splits.json", splits)
    data_audit["split_sizes"] = {key: len(value) for key, value in splits.items()}
    write_json(output / "data-audit.json", data_audit)
    encoded, encoding_info = embeddings(texts.tolist(), config)
    write_json(output / "phobert.json", encoding_info)
    representations = {"phobert": encoded}
    fitted = []
    results = []
    identifiers = ["majority", "word", "character", "phobert"]
    names = {
        "majority": "Majority baseline",
        "word": "Word TF-IDF + Linear SVM",
        "character": "Character TF-IDF + Linear SVM",
        "phobert": "Frozen PhoBERT + Logistic regression",
    }
    for identifier in identifiers:
        started = time.monotonic()
        trials = []
        best = None
        for c in [None] if identifier == "majority" else config["classifier_c"]:
            if identifier == "majority":
                model = DummyClassifier(strategy="most_frequent")
                features = np.ones((len(frame), 1))
            elif identifier == "phobert":
                model = LogisticRegression(
                    C=c, max_iter=2000, random_state=config["model_seed"]
                )
                features = representations["phobert"]
            else:
                vectorizer = TfidfVectorizer(
                    analyzer="word" if identifier == "word" else "char_wb",
                    ngram_range=(1, 2) if identifier == "word" else (3, 5),
                    min_df=2,
                    max_df=0.98,
                    max_features=config["max_features"],
                    sublinear_tf=True,
                )
                model = Pipeline(
                    [
                        ("tfidf", vectorizer),
                        (
                            "classifier",
                            LinearSVC(
                                C=c,
                                dual="auto",
                                max_iter=5000,
                                random_state=config["model_seed"],
                            ),
                        ),
                    ]
                )
                features = texts
            model.fit(features[train], target[train])
            value = metrics(target[val], model.predict(features[val]), labels)
            trials.append(
                {"C": c, "macro_f1": value["macro_f1"], "accuracy": value["accuracy"]}
            )
            if best is None or value["macro_f1"] > best[0]["macro_f1"]:
                best = (value, model, features, c)
        value, model, features, c = best
        results.append(
            {
                "id": identifier,
                "name": names[identifier],
                "selected_C": c,
                "validation": value,
                "validation_trials": trials,
                "fit_and_validation_seconds": time.monotonic() - started,
            }
        )
        fitted.append((model, features))
        print(f"{identifier}: validation macro-F1={value['macro_f1']:.4f}", flush=True)
    predictions = pd.DataFrame(
        {"id": frame.iloc[test]["id"].tolist(), "target": target[test]}
    )
    for result, (model, features) in zip(results, fitted):
        predicted = model.predict(features[test])
        result["test"] = metrics(target[test], predicted, labels)
        predictions[result["id"]] = predicted
    predictions.to_csv(output / "predictions.csv", index=False)
    # Source URLs identify errors without redistributing full article content.
    chosen = max(results, key=lambda item: item["validation"]["macro_f1"])["id"]
    errors = frame.iloc[test][["id", "url", "category"]].copy()
    errors["prediction"] = [labels[value] for value in predictions[chosen]]
    errors.loc[errors["category"] != errors["prediction"]].head(30).to_csv(
        output / "errors.csv", index=False
    )
    summary = {
        "track": "text",
        "classes": labels,
        "models": results,
        "test_opened_after_validation_choices": True,
        "pretrained": encoding_info,
    }
    write_json(output / "summary.json", summary)
    figures(output, summary, data_audit)
    model_files = save_models(
        "text", {result["id"]: model for result, (model, _) in zip(results, fitted)}
    )
    seal(
        "text",
        output,
        config,
        encoding_info,
        expected_sources=sources,
        model_files=model_files,
    )
    return summary


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    run()
