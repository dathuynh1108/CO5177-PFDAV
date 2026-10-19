"""VietnamNet headlines: TF-IDF baselines and frozen PhoBERT features."""

from __future__ import annotations

import argparse
import hashlib
import json
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
from sklearn.model_selection import train_test_split
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
    """Union equal URLs or normalized model inputs before sampling/splitting."""
    parent = list(range(len(frame)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    seen = {}
    for i, row in enumerate(frame.itertuples()):
        for key in [("url", row.url), ("headline", normalize(row.title).casefold())]:
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
                    }
                )
    frame, duplicate_audit = deduplicate(pd.DataFrame(records))
    # Rank IDs with a fixed salt. Sampling is independent of validation/test scores.
    frame["sample_rank"] = frame["id"].map(
        lambda value: hashlib.sha256(
            f"{config['sample_seed']}:{value}".encode()
        ).hexdigest()
    )
    selected = (
        frame.sort_values("sample_rank")
        .groupby("category", sort=True)
        .head(config["max_per_class"])
        .sort_values("id")
        .reset_index(drop=True)
    )
    if len(selected) < 2000 or selected["category"].nunique() != len(config["files"]):
        raise ValueError("Text cohort fails sample-count or category coverage contract")
    audit_data = {
        "raw_rows": raw,
        "raw_class_counts": dict(sorted(classes.items())),
        "empty_headlines_removed": empty,
        **duplicate_audit,
        "unique_usable_rows": len(frame),
        "modeling_rows": len(selected),
        "max_per_class": config["max_per_class"],
        "selected_class_counts": {
            k: int(v)
            for k, v in selected["category"].value_counts().sort_index().items()
        },
        "body_length_quantiles": {
            str(q): float(np.quantile(lengths, q))
            for q in [0, 0.25, 0.5, 0.75, 0.95, 1]
        },
        "input": "Headline only; URLs, body and category strings are excluded from model inputs",
        "sampling": "Deterministic capped cohort after full-corpus quality audit, not full-corpus training",
        "duplicate_scope": "Connected components of canonical URL OR normalized casefolded headline; conflicting-category components removed",
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
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
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
        "feature_cache_key": key,
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
    texts = np.array(segmented_headlines(frame), dtype=object)
    labels = sorted(frame["category"].unique())
    label_ids = {label: i for i, label in enumerate(labels)}
    target = frame["category"].map(label_ids).to_numpy()
    train, other = train_test_split(
        np.arange(len(frame)),
        test_size=0.30,
        random_state=config["split_seed"],
        stratify=target,
    )
    val, test = train_test_split(
        other,
        test_size=0.5,
        random_state=config["split_seed"] + 1,
        stratify=target[other],
    )
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
