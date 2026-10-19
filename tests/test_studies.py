"""Boundary checks for deduplication, train-only transforms and evidence integrity."""

import json

import numpy as np
import pandas as pd
import pytest

from studies.evidence import audit, metrics
from studies.tabular import CATEGORICAL, NUMERIC, clean, preprocessing
from studies.text import canonical_url, deduplicate, normalize


def test_news_duplicate_components_remove_conflicting_labels_transitively():
    frame = pd.DataFrame(
        [
            {"id": "1", "url": "url-a", "title": "Một bài báo", "category": "a"},
            {"id": "2", "url": "url-a", "title": "Tên khác", "category": "a"},
            {"id": "3", "url": "url-b", "title": "Tên khác", "category": "b"},
            {"id": "4", "url": "url-c", "title": "Bài riêng", "category": "a"},
            {"id": "5", "url": "url-d", "title": "BÀI RIÊNG", "category": "a"},
        ]
    )
    retained, info = deduplicate(frame)
    assert retained["id"].tolist() == ["4"]
    assert info["conflicting_category_rows_removed"] == 3
    assert info["duplicate_rows_removed_after_conflicts"] == 1


def test_news_canonical_input_removes_tracking_but_rejects_other_hosts():
    assert (
        canonical_url("http://www.vietnamnet.vn/bai-bao.html?x=1#section")
        == "https://vietnamnet.vn/bai-bao.html"
    )
    assert normalize("  a\n b  ") == "a b"
    with pytest.raises(ValueError, match="Unexpected article host"):
        canonical_url("https://example.org/article")


def adult_frame():
    rows = []
    for i in range(3):
        row = {name: float(i + 1) for name in NUMERIC}
        row.update({name: "train-category" for name in CATEGORICAL})
        row["income"] = "<=50K"
        rows.append(row)
    return pd.DataFrame(rows)


def test_adult_duplicate_features_with_opposing_labels_are_removed():
    frame = adult_frame()
    opposing = frame.iloc[[0]].copy()
    opposing["income"] = ">50K."
    repeated = frame.iloc[[1]].copy()
    retained, info = clean(pd.concat([frame, opposing, repeated], ignore_index=True))
    assert len(retained) == 2
    assert info["conflicting_label_rows_removed"] == 2
    assert info["duplicate_rows_removed_after_conflicts"] == 1
    assert retained["id"].is_unique


@pytest.mark.parametrize("tree", [False, True])
def test_preprocessing_learns_train_statistics_and_accepts_unseen_categories(tree):
    train = adult_frame()
    transform = preprocessing(tree).fit(train)
    before = (
        transform.named_transformers_["numeric"]
        .named_steps["impute"]
        .statistics_.copy()
    )
    heldout = adult_frame().iloc[[0]].copy()
    heldout.loc[:, NUMERIC] = np.nan
    heldout.loc[:, CATEGORICAL] = "unseen-test-category"
    values = transform.transform(heldout)
    assert values.shape[0] == 1
    assert np.array_equal(
        before,
        transform.named_transformers_["numeric"].named_steps["impute"].statistics_,
    )
    assert np.array_equal(before, np.full(6, 2.0))


def test_metrics_include_absent_classes_in_macro_average():
    value = metrics(np.array([0, 0]), np.array([0, 0]), ["a", "b"])
    assert value["accuracy"] == 1.0
    assert value["macro_f1"] == 0.5
    assert value["confusion"] == [[2, 0], [0, 0]]


def test_study_audit_rejects_modified_artifact_before_reading_predictions(tmp_path):
    (tmp_path / "sample.json").write_text("changed")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"artifacts_sha256": {"sample.json": "wrong"}})
    )
    with pytest.raises(ValueError, match="Measured artifact changed"):
        audit("text", tmp_path)
