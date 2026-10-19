"""UCI Adult: missing data, mixed features and held-out classification."""

from __future__ import annotations

import argparse
import io
import json
import time
import zipfile

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

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

NUMERIC = [
    "age",
    "fnlwgt",
    "education_num",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
]
CATEGORICAL = [
    "workclass",
    "education",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native_country",
]
COLUMNS = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education_num",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
    "native_country",
    "income",
]


def clean(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    frame = frame.copy()
    frame["income"] = frame["income"].str.rstrip(".")
    if not frame["income"].isin(["<=50K", ">50K"]).all():
        raise ValueError("Unexpected Adult target label")
    # Equal features must never occur in different splits, even with conflicting labels.
    keys = pd.util.hash_pandas_object(frame[NUMERIC + CATEGORICAL], index=False).astype(
        str
    )
    conflicts = frame.groupby(keys)["income"].transform("nunique") > 1
    duplicates = keys.duplicated()
    keep = ~conflicts & ~duplicates
    cleaned = frame.loc[keep].copy()
    cleaned["id"] = "adult-" + keys.loc[keep]
    return cleaned.reset_index(drop=True), {
        "raw_rows": len(frame),
        "feature_columns": len(NUMERIC + CATEGORICAL),
        "missing_by_column": {
            c: int(frame[c].isna().sum()) for c in NUMERIC + CATEGORICAL
        },
        "conflicting_label_rows_removed": int(conflicts.sum()),
        "duplicate_rows_removed_after_conflicts": int((duplicates & ~conflicts).sum()),
        "retained_rows": int(keep.sum()),
        "selected_class_counts": {
            k: int(v) for k, v in cleaned["income"].value_counts().items()
        },
    }


def load(config: dict) -> tuple[pd.DataFrame, dict]:
    archive = download(config["url"], ROOT / "data/adult.zip", config["sha256"])
    parts = []
    with zipfile.ZipFile(archive) as data:
        for name in ["adult.data", "adult.test"]:
            frame = pd.read_csv(
                io.BytesIO(data.read(name)),
                header=None,
                names=COLUMNS,
                skipinitialspace=True,
                na_values="?",
                comment="|",
            )
            parts.append(frame)
    return clean(pd.concat(parts, ignore_index=True))


def preprocessing(tree: bool = False) -> ColumnTransformer:
    numeric = [("impute", SimpleImputer(strategy="median"))]
    if not tree:
        numeric.append(("scale", StandardScaler()))
    categorical = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            (
                "encode",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
                if tree
                else OneHotEncoder(handle_unknown="ignore", sparse_output=True),
            ),
        ]
    )
    return ColumnTransformer(
        [
            ("numeric", Pipeline(numeric), NUMERIC),
            ("categorical", categorical, CATEGORICAL),
        ]
    )


def run() -> dict:
    sources = source_identity("tabular")
    config = json.loads((ROOT / "configs/tabular.json").read_text())
    output = ROOT / "reports/tabular/generated"
    output.mkdir(parents=True, exist_ok=True)
    frame, data_audit = load(config)
    target = (frame["income"] == ">50K").astype(int).to_numpy()
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
    data_audit["split_sizes"] = {name: len(ids) for name, ids in splits.items()}
    write_json(output / "data-audit.json", data_audit)
    labels = ["<=50K", ">50K"]
    fitted = []
    results = []
    definitions = [
        ("majority", "Majority baseline", [None]),
        ("logistic", "Logistic regression", config["logistic_c"]),
        ("balanced", "Balanced logistic regression", config["logistic_c"]),
        ("histogram", "Histogram gradient boosting", [None]),
    ]
    # All validation choices finish before any held-out predictions are made.
    for identifier, name, candidates in definitions:
        trials = []
        best = None
        started = time.monotonic()
        for c in candidates:
            if identifier == "majority":
                classifier = DummyClassifier(strategy="most_frequent")
            elif identifier == "histogram":
                classifier = HistGradientBoostingClassifier(
                    max_iter=150,
                    max_leaf_nodes=31,
                    l2_regularization=1.0,
                    early_stopping=False,
                    categorical_features=list(range(6, 14)),
                    random_state=config["model_seed"],
                )
            else:
                classifier = LogisticRegression(
                    C=c,
                    max_iter=2000,
                    class_weight="balanced" if identifier == "balanced" else None,
                    random_state=config["model_seed"],
                )
            model = Pipeline(
                [
                    ("preprocess", preprocessing(identifier == "histogram")),
                    ("classifier", classifier),
                ]
            )
            model.fit(frame.iloc[train], target[train])
            value = metrics(target[val], model.predict(frame.iloc[val]), labels)
            trials.append(
                {"C": c, "macro_f1": value["macro_f1"], "accuracy": value["accuracy"]}
            )
            if best is None or value["macro_f1"] > best[0]["macro_f1"]:
                best = (value, model, c)
        value, model, c = best
        results.append(
            {
                "id": identifier,
                "name": name,
                "selected_C": c,
                "validation": value,
                "validation_trials": trials,
                "fit_and_validation_seconds": time.monotonic() - started,
            }
        )
        fitted.append(model)
        print(f"{identifier}: validation macro-F1={value['macro_f1']:.4f}", flush=True)
    predictions = pd.DataFrame(
        {"id": frame.iloc[test]["id"].tolist(), "target": target[test]}
    )
    for result, model in zip(results, fitted):
        predicted = model.predict(frame.iloc[test])
        result["test"] = metrics(target[test], predicted, labels)
        predictions[result["id"]] = predicted
    predictions.to_csv(output / "predictions.csv", index=False)
    summary = {
        "track": "tabular",
        "classes": labels,
        "models": results,
        "test_opened_after_validation_choices": True,
    }
    write_json(output / "summary.json", summary)
    figures(output, summary, data_audit)
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4))
    missing = data_audit["missing_by_column"]
    ax.bar(list(missing), list(missing.values()), color="#b74c32")
    ax.tick_params(axis="x", labelrotation=70, labelsize=8)
    ax.set(ylabel="Missing records")
    fig.tight_layout()
    fig.savefig(output / "missing.png", dpi=160)
    plt.close(fig)
    model_files = save_models(
        "tabular", {result["id"]: model for result, model in zip(results, fitted)}
    )
    seal("tabular", output, config, expected_sources=sources, model_files=model_files)
    return summary


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    run()
