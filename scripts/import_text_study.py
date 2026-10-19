"""Import the supplied executed PhoBERT notebook and its matching public package.

This reads notebook JSON and Git blobs; it never executes training or pickle files.
"""

import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path

from studies.evidence import ROOT, sha256, write_json

SOURCE_COMMIT = "e17168883b8a80a5c77b670018dd9ac8afb15913"
SOURCE_REPO = "https://github.com/dathuynh1108/phobert-news-classification-app"
NOTEBOOK_SHA256 = "32a22cbe811bc8f1035cd80b819a5eb8da0e2390ca3b5d6ca32dbcca9c238c66"


class Table(HTMLParser):
    """Read the printed Trainer epoch table without evaluating notebook HTML."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = []
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in {"td", "th"}:
            self.cell = ""

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in {"td", "th"} and self.cell is not None:
            self.row.append(self.cell.strip())
            self.cell = None
        elif tag == "tr" and self.row:
            self.rows.append(self.row)


def git_blob(checkout, path):
    return subprocess.check_output(
        ["git", "-C", str(checkout), "show", f"{SOURCE_COMMIT}:{path}"]
    )


def stream(cell):
    return "\n".join("".join(o.get("text", [])) for o in cell.get("outputs", []))


def main(notebook_path, checkout):
    if sha256(notebook_path) != NOTEBOOK_SHA256:
        raise ValueError("The supplied executed notebook identity differs")
    notebook = json.loads(notebook_path.read_bytes())
    current = json.loads(git_blob(checkout, "train/notebooks/main_PhoBERT.ipynb"))
    if [c["source"] for c in notebook["cells"]] != [
        c["source"] for c in current["cells"]
    ]:
        raise ValueError("Notebook source differs from the pinned application release")
    if any(
        o["output_type"] == "error"
        for c in notebook["cells"]
        for o in c.get("outputs", [])
    ):
        raise ValueError("The supplied notebook contains an execution error")

    destination = ROOT / "reports/text/reused"
    evidence = destination / "evidence"
    figures = destination / "figures"
    evidence.mkdir(parents=True, exist_ok=True)
    figures.mkdir(exist_ok=True)
    primary = ROOT / "notebooks/text.ipynb"
    baseline = ROOT / "notebooks/text_baselines.ipynb"
    if primary.exists() and sha256(primary) != NOTEBOOK_SHA256:
        if baseline.exists() and sha256(primary) != sha256(baseline):
            raise ValueError("Refusing to overwrite a different baseline notebook")
        shutil.copyfile(primary, baseline)
    shutil.copyfile(notebook_path, primary)

    imported = {}

    def record(path, origin):
        imported[str(path.relative_to(ROOT))] = {"sha256": sha256(path), **origin}

    record(primary, {"kind": "user_attachment", "filename": notebook_path.name})
    for name in [
        "config.json",
        "label_config.json",
        "metrics.json",
        "thresholds.json",
        "confusion_matrix.json",
        "classification_report.json",
    ]:
        source = f"train/artifacts/active/{name}"
        path = evidence / name
        path.write_bytes(git_blob(checkout, source))
        record(path, {"kind": "git_blob", "source_path": source})

    for index, cell in enumerate(notebook["cells"]):
        latest_text = ""
        for output_index, output in enumerate(cell.get("outputs", [])):
            latest_text += "".join(output.get("text", []))
            encoded = output.get("data", {}).get("image/png")
            if encoded:
                matches = re.findall(r"Saved -> .*?/([^/\s]+\.png)", latest_text)
                if not matches:
                    raise ValueError(f"No source filename for image in cell {index}")
                path = figures / matches[-1]
                path.write_bytes(
                    base64.b64decode(
                        re.sub(r"\s+", "", "".join(encoded)), validate=True
                    )
                )
                record(
                    path,
                    {"kind": "notebook_output", "cell": index, "output": output_index},
                )
    if len(list(figures.glob("*.png"))) != 7:
        raise ValueError("Expected seven original notebook figures")

    table = Table()
    for output in notebook["cells"][19]["outputs"]:
        table.feed("".join(output.get("data", {}).get("text/html", [])))
    columns = [
        "epoch",
        "training_loss_printed",
        "evaluation_loss",
        "accuracy",
        "f1_weighted",
        "f1_macro",
    ]
    epochs = [dict(zip(columns, map(float, row))) for row in table.rows[1:]]
    if len(epochs) != 7:
        raise ValueError("Expected seven observed epochs")
    write_json(
        evidence / "epochs.json",
        {
            "source_cell": 19,
            "printed_decimals": 6,
            "evaluation_role": "checkpoint_selection_on_test_named_split",
            "epochs": epochs,
        },
    )
    record(evidence / "epochs.json", {"kind": "parsed_notebook_output", "cell": 19})

    labels = json.loads((evidence / "label_config.json").read_text())["classes"]
    report_text = stream(notebook["cells"][22])
    before = {}
    for label in labels:
        match = re.search(
            r"^\s*"
            + re.escape(label)
            + r"\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)\s*$",
            report_text,
            re.MULTILINE,
        )
        if not match:
            raise ValueError(f"Missing printed class report: {label}")
        p, r, f, count = match.groups()
        before[label] = {
            "precision": float(p),
            "recall": float(r),
            "f1-score": float(f),
            "support": int(count),
        }
    write_json(
        evidence / "classification_before_printed.json",
        {"printed_decimals": 4, "per_class": before},
    )
    record(
        evidence / "classification_before_printed.json",
        {"kind": "parsed_notebook_output", "cell": 22},
    )

    runtime = stream(notebook["cells"][3])
    settings = stream(notebook["cells"][4])
    duration = float(
        re.search(r"Training finished - (\d+)s", stream(notebook["cells"][19])).group(1)
    )
    quality = stream(notebook["cells"][7])
    counts = {}
    for line in quality.splitlines():
        match = re.search(r"source=\s*([\d,]+).*?\[(.+?)\]", line)
        if match:
            counts[match[2]] = int(match[1].replace(",", ""))
    calibration_text = stream(notebook["cells"][30])
    calibration = {}
    for key in ["NLL", "ECE"]:
        match = re.search(key + r"\s*:\s*([\d.]+) -> ([\d.]+)", calibration_text)
        calibration[key.lower()] = {
            "before": float(match[1]),
            "after_temperature": float(match[2]),
            "printed_decimals": 4,
        }
    package = json.loads((evidence / "metrics.json").read_text())
    if sum(counts.values()) != package["dataset"]["total"]:
        raise ValueError("Notebook and package corpus counts differ")
    if (
        "GLOBAL_EFF=64" not in settings
        or "CUDA GPUs visible: 2 - Tesla T4, Tesla T4" not in runtime
    ):
        raise ValueError("Unexpected measured training runtime")
    summary = {
        "dataset": package["dataset"],
        "source_class_counts": counts,
        "hardware": {
            "platform": "Kaggle",
            "gpus": ["Tesla T4", "Tesla T4"],
            "vram_gib_each_printed": 14.6,
            "python": "3.12.12",
            "torch": "2.10.0+cu128",
        },
        "execution": notebook["metadata"]["papermill"],
        "training_seconds_rounded": duration,
        "settings": {
            "epochs": 7,
            "max_length": 256,
            "raw_content_head_words": 220,
            "raw_content_tail_words": 80,
            "batch_per_gpu": 16,
            "gradient_accumulation": 2,
            "global_effective_batch": 64,
            "eval_batch_per_gpu": 32,
            "learning_rate": 2e-5,
            "weight_decay": 0.01,
            "warmup_steps": 200,
            "split_seed": 42,
            "fp16": True,
            "bf16": False,
            "early_stopping_patience": 3,
        },
        "metrics_before": package["metrics_before"],
        "metrics_after": package["metrics_after"],
        "temperature": package["temperature"],
        "calibration": calibration,
        "evaluation_role": "same_31906_rows_used_for_checkpoint_selection_temperature_and_thresholds",
        "raw_predictions_available": False,
        "data_revision_logged_by_original_run": False,
        "layernorm_reload_warning_present": "There were missing keys in the checkpoint model loaded"
        in stream(notebook["cells"][19]),
        "new_training_performed_for_import": False,
    }
    write_json(evidence / "run-summary.json", summary)
    record(
        evidence / "run-summary.json", {"kind": "parsed_notebook_and_matching_package"}
    )
    model_files = {}
    for name in [
        "model.safetensors",
        "bpe.codes",
        "vocab.txt",
        "tokenizer_config.json",
        "added_tokens.json",
    ]:
        path = f"train/artifacts/active/{name}"
        blob = git_blob(checkout, path)
        if blob.startswith(b"version https://git-lfs.github.com/spec/v1"):
            content = blob.decode()
            expected = re.search(r"oid sha256:([a-f0-9]{64})", content)[1]
            size = int(re.search(r"size (\d+)", content)[1])
        else:
            expected, size = hashlib.sha256(blob).hexdigest(), len(blob)
        model_files[name] = {"source_path": path, "sha256": expected, "bytes": size}
    write_json(
        ROOT / "reports/text/reuse-manifest.json",
        {
            "schema_version": 1,
            "source_repository": SOURCE_REPO,
            "source_commit": SOURCE_COMMIT,
            "notebook_sha256": NOTEBOOK_SHA256,
            "all_36_cell_sources_match_pinned_repository": True,
            "imported_files": imported,
            "checkpoint_files": model_files,
            "baseline_notebook": "notebooks/text_baselines.ipynb",
            "comparison_policy": "Headline baselines and full-article fine-tuning have different inputs and splits; no paired superiority claim.",
        },
    )
    print(
        f"Imported notebook, {len(imported)} verified artifacts, seven figures and seven epochs"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    options = parser.parse_args()
    main(options.notebook, options.source)
