"""Recompute reused metrics from predictions, verifying their recorded lineage."""
import csv
import hashlib
import json
from pathlib import Path
import statistics
import numpy as np
from image.protocol import ROOT, CONFIG, load_protocol


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root=ROOT):
    manifest = json.loads((root / 'reports/image/reuse-manifest.json').read_text())
    for path, expected in manifest['imported_files'].items():
        if sha(root / path) != expected:
            raise ValueError(f'Imported artifact changed: {path}')
    if sha(root / 'configs/image.json') != manifest['source_config_sha256']:
        raise ValueError('Protocol differs from the measured source')
    for path, entry in manifest['ported_sources'].items():
        if sha(root / path) != entry['ported_sha256']:
            raise ValueError(f'Ported source changed: {path}')
    protocol = json.loads((root / 'configs/image.json').read_text())
    source = {key: value for key, value in manifest['source_files'].items()
              if key != 'A1/export_report.py'}
    rows = []
    reference_data = None
    for experiment in protocol['experiments']:
        for seed in protocol['seeds']:
            run = root / 'reports/image/generated/evidence' / experiment['id'] / f'seed_{seed}'
            metadata = json.loads((run / 'metadata.json').read_text())
            signature = metadata['signature']
            canonical = json.dumps(signature,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
            if hashlib.sha256(canonical).hexdigest() != metadata['signature_sha256']:
                raise ValueError('Signature hash mismatch')
            if (signature['protocol'] != protocol or signature['experiment'] != experiment
                or signature['seed'] != seed or signature['source'] != source
                or signature['config_sha256'] != manifest['source_config_sha256']):
                raise ValueError('Measured protocol/source/seed mismatch')
            if reference_data is not None and signature['data'] != reference_data:
                raise ValueError('Cross-run data mismatch')
            reference_data = signature['data']
            split = json.loads((run / 'split.json').read_text())
            split_hash = hashlib.sha256(json.dumps(split,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if split_hash != signature['data']['split_sha256']:
                raise ValueError('Split hash mismatch')
            with (run / 'history.csv').open() as f: history=list(csv.DictReader(f))
            if len(history) != protocol['epochs'] or metadata['completed_epochs'] != protocol['epochs']:
                raise ValueError('Incomplete history')
            winner=max(history,key=lambda x:(float(x['val_accuracy']),-float(x['val_ce']),-int(x['epoch'])))
            if int(winner['epoch']) != metadata['best_validation']['epoch']:
                raise ValueError('Validation checkpoint selection mismatch')
            evaluation = json.loads((run / 'evaluation_test.json').read_text())
            if evaluation['identity']['signature_sha256'] != metadata['signature_sha256']:
                raise ValueError('Evaluation signature mismatch')
            if evaluation['best_state_sha256'] != metadata['best_validation']['state_sha256']:
                raise ValueError('Checkpoint identity mismatch')
            with (run / 'predictions_test.csv').open() as f: predictions=list(csv.DictReader(f))
            if len(predictions) != 10000 or [int(x['index']) for x in predictions] != list(range(10000)):
                raise ValueError('Missing or reordered held-out predictions')
            cm=np.zeros((100,100),dtype=np.int64)
            for item in predictions: cm[int(item['target']),int(item['prediction'])]+=1
            if not np.array_equal(cm, evaluation['confusion']) or not np.all(cm.sum(1)==100):
                raise ValueError('Prediction/confusion mismatch')
            accuracy=float(cm.trace()/cm.sum())
            f1=float(np.mean(2*np.diag(cm)/np.maximum(cm.sum(0)+cm.sum(1),1)))
            if abs(accuracy-evaluation['accuracy'])>1e-12 or abs(f1-evaluation['macro_f1'])>1e-12:
                raise ValueError('Metrics do not match predictions')
            rows.append(dict(experiment=experiment['id'],seed=seed,accuracy=accuracy,macro_f1=f1,
                             train_seconds=metadata['train_seconds'],memory_mib=metadata['peak_gpu_memory_bytes']/2**20))
    summary=[]
    for experiment in protocol['experiments']:
        selected=[x for x in rows if x['experiment']==experiment['id']]
        summary.append(dict(experiment=experiment['id'],regime=experiment['regime'],
                            accuracy=statistics.mean(x['accuracy'] for x in selected),
                            sd=statistics.stdev(x['accuracy'] for x in selected),
                            macro_f1=statistics.mean(x['macro_f1'] for x in selected)))
    if len(rows)!=24: raise ValueError('Expected 24 measured runs')
    return {'verified_runs':len(rows),'new_training_runs':0,'source_commit':manifest['source_commit'],
            'summary':summary,'runs':rows}


if __name__=='__main__':
    result=audit()
    print(json.dumps(result,indent=2))
