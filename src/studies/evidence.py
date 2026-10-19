"""Artifact writing and evaluation shared by the two coursework studies."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import tempfile
import urllib.request
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as target:
            target.write(payload)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def download(url: str, destination: Path, expected: str) -> Path:
    if destination.exists():
        if sha256(destination) != expected:
            raise ValueError(f"Cached source checksum mismatch: {destination.name}")
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".partial")
    try:
        with (
            urllib.request.urlopen(url, timeout=60) as response,
            temporary.open("wb") as target,
        ):
            while block := response.read(1024 * 1024):
                target.write(block)
        if sha256(temporary) != expected:
            raise ValueError(f"Download checksum mismatch: {destination.name}")
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def metrics(target: np.ndarray, prediction: np.ndarray, labels: list[str]) -> dict:
    indices = np.arange(len(labels))
    return {
        "accuracy": float(accuracy_score(target, prediction)),
        "macro_f1": float(
            f1_score(
                target, prediction, labels=indices, average="macro", zero_division=0
            )
        ),
        "confusion": confusion_matrix(target, prediction, labels=indices).tolist(),
        "per_class": classification_report(
            target,
            prediction,
            labels=indices,
            target_names=labels,
            output_dict=True,
            zero_division=0,
        ),
    }


def source_identity(track: str) -> dict[str, str]:
    paths = list((ROOT / "src/studies").glob("*.py")) + [ROOT / f"configs/{track}.json"]
    return {str(path.relative_to(ROOT)): sha256(path) for path in sorted(paths)}


def save_models(track: str, models: dict) -> dict[str, str]:
    import joblib

    folder = ROOT / "runs" / track
    folder.mkdir(parents=True, exist_ok=True)
    result = {}
    for name, model in models.items():
        path = folder / f"{name}.joblib"
        joblib.dump(model, path, compress=3)
        result[str(path.relative_to(ROOT))] = sha256(path)
    return result


def seal(
    track: str,
    output: Path,
    config: dict,
    runtime: dict | None = None,
    expected_sources: dict | None = None,
    model_files: dict | None = None,
) -> None:
    files = {
        str(path.relative_to(output)): sha256(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }
    sources = source_identity(track)
    if expected_sources is not None and sources != expected_sources:
        raise ValueError("Source/config changed during measurement")
    packages = {}
    for name in [
        "numpy",
        "pandas",
        "scikit-learn",
        "pyarrow",
        "torch",
        "transformers",
        "pyvi",
    ]:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            continue
    write_json(
        output / "manifest.json",
        {
            "track": track,
            "config": config,
            "source_sha256": sources,
            "artifacts_sha256": files,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": packages,
            "runtime": runtime or {},
            "model_artifacts_sha256": model_files or {},
        },
    )


def audit(track: str, output: Path | None = None, check_models: bool = False) -> dict:
    output = output or ROOT / "reports" / track / "generated"
    manifest = json.loads((output / "manifest.json").read_text())
    for relative, expected in manifest["artifacts_sha256"].items():
        if sha256(output / relative) != expected:
            raise ValueError(f"Measured artifact changed: {track}/{relative}")
    if check_models:
        for relative, expected in manifest["model_artifacts_sha256"].items():
            if sha256(ROOT / relative) != expected:
                raise ValueError(f"Saved classifier changed: {relative}")
    import pandas as pd

    table = pd.read_csv(output / "predictions.csv")
    summary = json.loads((output / "summary.json").read_text())
    split = json.loads((output / "splits.json").read_text())
    train, val, test = (set(split[key]) for key in ["train", "validation", "test"])
    if train & val or train & test or val & test:
        raise ValueError("Split identities overlap")
    if set(table["id"].astype(str)) != test or len(table) != len(test):
        raise ValueError("Held-out prediction identities differ from split")
    for result in summary["models"]:
        value = metrics(
            table["target"].to_numpy(),
            table[result["id"]].to_numpy(),
            summary["classes"],
        )
        if abs(value["accuracy"] - result["test"]["accuracy"]) > 1e-12:
            raise ValueError("Accuracy does not match predictions")
        if abs(value["macro_f1"] - result["test"]["macro_f1"]) > 1e-12:
            raise ValueError("Macro-F1 does not match predictions")
        if value["confusion"] != result["test"]["confusion"]:
            raise ValueError("Confusion does not match predictions")
    return {
        "track": track,
        "models": len(summary["models"]),
        "test_rows": len(table),
        "verified_artifacts": len(manifest["artifacts_sha256"]),
    }


def figures(output: Path, summary: dict, audit_data: dict) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.metrics import ConfusionMatrixDisplay

    output.mkdir(parents=True, exist_ok=True)
    results = summary["models"]
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(results))
    ax.bar(
        x - 0.18,
        [r["test"]["accuracy"] for r in results],
        0.36,
        label="Accuracy",
        color="#263e35",
    )
    ax.bar(
        x + 0.18,
        [r["test"]["macro_f1"] for r in results],
        0.36,
        label="Macro-F1",
        color="#b74c32",
    )
    ax.set_xticks(x, [r["name"].replace(" + ", "\n") for r in results], fontsize=8)
    ax.set(ylim=(0, 1), ylabel="Held-out score")
    ax.legend()
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(output / "scores.png", dpi=160)
    plt.close(fig)
    # Select the illustrated model by validation, before inspecting test scores.
    selected = max(results, key=lambda r: r["validation"]["macro_f1"])
    fig, ax = plt.subplots(figsize=(8, 7))
    ConfusionMatrixDisplay(
        np.array(selected["test"]["confusion"]), display_labels=summary["classes"]
    ).plot(
        ax=ax,
        colorbar=False,
        xticks_rotation=90,
        include_values=len(summary["classes"]) <= 3,
    )
    ax.set_title(selected["name"])
    fig.tight_layout()
    fig.savefig(output / "confusion.png", dpi=160)
    plt.close(fig)
    counts = audit_data["selected_class_counts"]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(list(counts), list(counts.values()), color="#263e35")
    ax.tick_params(axis="x", labelrotation=75, labelsize=7)
    ax.set(ylabel="Records", title="Class distribution in the modeling cohort")
    fig.tight_layout()
    fig.savefig(output / "class_counts.png", dpi=160)
    plt.close(fig)
