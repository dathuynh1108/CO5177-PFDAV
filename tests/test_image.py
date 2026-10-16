import json
from pathlib import Path
import numpy as np
import pytest
from image.analysis import audit
from image.data import stratified_split
from image.protocol import ROOT


def test_measured_predictions_reproduce_all_24_runs():
    result=audit()
    assert result['verified_runs']==24 and result['new_training_runs']==0
    best=max(result['summary'],key=lambda r:r['accuracy'])
    assert best['experiment']=='swin_t_full'
    assert best['accuracy']==pytest.approx(.8663)


def test_split_port_preserves_official_class_counts_and_disjoint_indices():
    train,val=stratified_split(np.repeat(np.arange(100),500))
    assert len(train)==45000 and len(val)==5000 and not set(train)&set(val)
    assert set(train)|set(val)==set(range(50000))


def test_imported_evidence_tampering_fails_closed(tmp_path):
    path=tmp_path/'reports/image';path.mkdir(parents=True)
    (path/'reuse-manifest.json').write_text(json.dumps({'imported_files':{'payload.csv':'wrong'}}))
    (tmp_path/'payload.csv').write_bytes(b'changed')
    with pytest.raises(ValueError,match='Imported artifact changed'):audit(tmp_path)
