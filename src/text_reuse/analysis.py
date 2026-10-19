"""Verify notebook figures and recompute calibrated metrics from the saved matrix."""

import json

import numpy as np

from studies.evidence import ROOT, sha256


def audit(root=ROOT):
    manifest = json.loads((root / "reports/text/reuse-manifest.json").read_text())
    for relative, metadata in manifest["imported_files"].items():
        if sha256(root / relative) != metadata["sha256"]:
            raise ValueError(f"Reused Text artifact changed: {relative}")
    folder = root / "reports/text/reused/evidence"
    metrics = json.loads((folder / "metrics.json").read_text())
    report = json.loads((folder / "classification_report.json").read_text())
    thresholds = json.loads((folder / "thresholds.json").read_text())
    payload = json.loads((folder / "confusion_matrix.json").read_text())
    matrix = np.asarray(payload["matrix"])
    if (
        matrix.shape != (19, 19)
        or np.any(matrix < 0)
        or np.any(matrix != matrix.astype(int))
    ):
        raise ValueError("Invalid 19-class confusion matrix")
    support = matrix.sum(axis=1)
    if support.sum() != metrics["dataset"]["test"]:
        raise ValueError("Confusion support differs from the recorded evaluation size")
    tp = np.diag(matrix)
    precision = np.divide(
        tp, matrix.sum(axis=0), out=np.zeros(19), where=matrix.sum(axis=0) != 0
    )
    recall = tp / support
    f1 = np.divide(
        2 * precision * recall,
        precision + recall,
        out=np.zeros(19),
        where=(precision + recall) != 0,
    )
    recomputed = {
        "accuracy": float(tp.sum() / support.sum()),
        "f1_macro": float(f1.mean()),
        "f1_weighted": float(np.average(f1, weights=support)),
    }
    for name, value in recomputed.items():
        if abs(value - metrics["metrics_after"][name]) > 1e-12:
            raise ValueError(f"Calibrated {name} does not match saved confusion")
    if not np.allclose(
        payload["normalized_matrix"], matrix / support[:, None], rtol=0, atol=1e-12
    ):
        raise ValueError("Normalized confusion differs from counts")
    for index, label in enumerate(payload["labels"]):
        for key, value in [
            ("precision", precision[index]),
            ("recall", recall[index]),
            ("f1-score", f1[index]),
            ("support", support[index]),
        ]:
            if abs(value - report[label][key]) > 1e-12:
                raise ValueError(f"Class report differs: {label}/{key}")
    if (
        metrics["metrics_before"] != thresholds["metrics_before"]
        or metrics["metrics_after"] != thresholds["metrics_after"]
    ):
        raise ValueError("Threshold and metric packages differ")
    notebook = json.loads((root / "notebooks/text.ipynb").read_text())
    images = sum(
        "image/png" in o.get("data", {})
        for c in notebook["cells"]
        for o in c.get("outputs", [])
    )
    if images != 7:
        raise ValueError("Expected seven original figures in the executed notebook")
    return {
        "verified_files": len(manifest["imported_files"]),
        "notebook_cells": len(notebook["cells"]),
        "observed_code_cells": sum(
            c["cell_type"] == "code" and c.get("execution_count") is not None
            for c in notebook["cells"]
        ),
        "original_figures": images,
        "evaluation_rows": int(support.sum()),
        "calibrated_metrics_recomputed": recomputed,
        "new_training_performed": False,
        "independent_test": False,
    }


def export_tables(root=ROOT):
    """Write report tables and readable plots from preserved measured evidence."""
    audit(root)
    folder = root / "reports/text/reused/evidence"
    output = root / "reports/text/reused/tables"
    output.mkdir(exist_ok=True)
    load = lambda name: json.loads((folder / name).read_text())
    summary = load("run-summary.json")
    before = load("classification_before_printed.json")["per_class"]
    after = load("classification_report.json")
    thresholds = load("thresholds.json")["thresholds"]
    labels = load("label_config.json")["classes"]

    def table(name, spec, header, rows):
        text = [
            r"\begin{tabularx}{\textwidth}{" + spec + r"}\toprule",
            header + r"\\\midrule",
        ]
        text += [" & ".join(row) + r"\\" for row in rows]
        text += [r"\bottomrule\end{tabularx}"]
        (output / name).write_text("\n".join(text) + "\n")

    rows = []
    for metric, name in [
        ("accuracy", "Accuracy"),
        ("f1_weighted", "Weighted-F1"),
        ("f1_macro", "Macro-F1"),
    ]:
        a, b = summary["metrics_before"][metric], summary["metrics_after"][metric]
        rows.append([name, f"{a:.6f}", f"{b:.6f}", f"{b - a:+.6f}"])
    table(
        "metrics.tex",
        "Xrrr",
        "Chỉ số & Trước hiệu chỉnh & Sau hiệu chỉnh & Chênh lệch",
        rows,
    )
    rows = [
        [
            label,
            str(int(after[label]["support"])),
            f"{before[label]['f1-score']:.4f}",
            f"{after[label]['f1-score']:.4f}",
            f"{thresholds[label]:.4f}",
        ]
        for label in labels
    ]
    table(
        "classes.tex", "Xrrrr", "Chuyên mục & Số mẫu & F1 trước & F1 sau & Ngưỡng", rows
    )
    epochs = load("epochs.json")["epochs"]
    rows = [
        [
            str(int(r["epoch"])),
            f"{r['training_loss_printed']:.6f}",
            f"{r['evaluation_loss']:.6f}",
            f"{r['accuracy']:.6f}",
            f"{r['f1_macro']:.6f}",
        ]
        for r in epochs
    ]
    table(
        "epochs.tex",
        "Xrrrr",
        "Epoch & Train loss* & Eval loss & Accuracy & Macro-F1",
        rows,
    )
    pairs = load("confusion_matrix.json")["top_confusions"][:8]
    rows = [
        [r["true"], r["pred"], str(r["count"]), f"{100 * r['rate']:.2f}\\%"]
        for r in pairs
    ]
    table(
        "confusions.tex", "XXrr", "Nhãn thực & Dự đoán & Số lỗi & Tỷ lệ trong lớp", rows
    )
    counts = summary["source_class_counts"]
    rows = [
        [label, f"{counts[label]:,}", f"{100 * counts[label] / 212705:.2f}\\%"]
        for label in labels
    ]
    table("counts.tex", "Xrr", "Chuyên mục & Số bài & Tỷ lệ", rows)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 1, figsize=(7, 7), sharex=True)
    x = [r["epoch"] for r in epochs]
    axes[0].plot(
        x,
        [r["training_loss_printed"] for r in epochs],
        "o-",
        label="Train loss (printed)",
        color="#263e35",
    )
    axes[0].plot(
        x,
        [r["evaluation_loss"] for r in epochs],
        "o-",
        label="Evaluation loss",
        color="#b74c32",
    )
    axes[0].set(ylabel="Loss")
    axes[1].plot(
        x, [r["accuracy"] for r in epochs], "o-", label="Accuracy", color="#263e35"
    )
    axes[1].plot(
        x, [r["f1_macro"] for r in epochs], "o-", label="Macro-F1", color="#b74c32"
    )
    axes[1].set(xlabel="Epoch", ylabel="Score", xticks=x)
    for ax in axes:
        ax.legend()
        ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output / "epoch_curves.png", dpi=160)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", action="store_true")
    options = parser.parse_args()
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
    if options.export:
        export_tables()
