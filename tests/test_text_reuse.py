"""Check that historical Text evidence is intact and its scores are reproducible."""

import json
import shutil

import pytest

from studies.evidence import ROOT, sha256
from text_reuse.analysis import audit


def test_full_notebook_evidence_recomputes_calibrated_metrics():
    result = audit()
    assert result["observed_code_cells"] == 25
    assert result["original_figures"] == 7
    assert result["evaluation_rows"] == 31906
    assert result["calibrated_metrics_recomputed"]["accuracy"] == pytest.approx(
        0.9086378737541528
    )
    assert not result["independent_test"]
    assert not result["new_training_performed"]


def copy_evidence(destination):
    manifest_path = ROOT / "reports/text/reuse-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for name in ["reports/text/reuse-manifest.json", *manifest["imported_files"]]:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return manifest


def test_audit_rejects_changed_original_figure(tmp_path):
    copy_evidence(tmp_path)
    path = tmp_path / "reports/text/reused/figures/05_training_curves.png"
    path.write_bytes(b"changed figure")
    with pytest.raises(ValueError, match="Reused Text artifact changed"):
        audit(tmp_path)


def test_audit_recomputes_scores_even_if_modified_matrix_is_rehashed(tmp_path):
    manifest = copy_evidence(tmp_path)
    name = "reports/text/reused/evidence/confusion_matrix.json"
    path = tmp_path / name
    matrix = json.loads(path.read_text())
    matrix["matrix"][0][0] -= 1
    matrix["matrix"][0][1] += 1
    path.write_text(json.dumps(matrix))
    manifest["imported_files"][name]["sha256"] = sha256(path)
    (tmp_path / "reports/text/reuse-manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="does not match saved confusion"):
        audit(tmp_path)
