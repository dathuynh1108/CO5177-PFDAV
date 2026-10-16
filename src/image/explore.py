"""Inspect the full public CIFAR-100 mirror, checking original pixel identities."""
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import os
import numpy as np
from PIL import Image
import pyarrow.parquet as pq
from image.data import stratified_split, array_hash
from image.protocol import ROOT

REVISION='aadb3af77e9048adbea6b47c21a81e47dd092ae5'


def load_images(split, data_root=None):
    data_root=Path(data_root or ROOT/'data');data_root.mkdir(parents=True,exist_ok=True)
    path=data_root/f'{split}.parquet'
    if not path.exists():
        url=f'https://huggingface.co/datasets/uoft-cs/cifar100/resolve/{REVISION}/cifar100/{split}-00000-of-00001.parquet'
        temporary=path.with_suffix('.partial')
        try:
            with urllib.request.urlopen(url,timeout=60) as response, temporary.open('wb') as target:
                while block:=response.read(1024*1024):target.write(block)
            os.replace(temporary,path)
        finally:temporary.unlink(missing_ok=True)
    table=pq.read_table(path)
    images=np.stack([np.asarray(Image.open(io.BytesIO(x['bytes'])).convert('RGB')) for x in table['img'].to_pylist()])
    labels=np.asarray(table['fine_label'].to_pylist(),dtype=np.int64)
    # A1 trained with the Toronto archive. Equality of ordered pixels/labels
    # verifies this mirror is the same complete data for exploratory analysis.
    evidence=ROOT/'reports/image/generated/evidence/resnet18_full/seed_42'
    if split=='train':expected=json.loads((evidence/'metadata.json').read_text())['signature']['data']
    else:expected=json.loads((evidence/'evaluation_test.json').read_text())['identity']['test_data']
    if array_hash(images)!=expected['images_sha256'] or array_hash(labels)!=expected['labels_sha256']:
        raise ValueError(f'{split}: mirror pixels/labels differ from the measured data')
    return images,labels


def explore(destination=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    destination=Path(destination or ROOT/'reports/image/analysis');destination.mkdir(parents=True,exist_ok=True)
    images,labels=load_images('train');test,test_labels=load_images('test')
    train,val=stratified_split(labels)
    split=json.loads((ROOT/'reports/image/generated/evidence/resnet18_full/seed_42/split.json').read_text())
    if train!=split['train'] or val!=split['val']:raise ValueError('Split indices differ from measured split')
    hashes=[hashlib.sha256(x.tobytes()).hexdigest() for x in images]
    test_hashes=[hashlib.sha256(x.tobytes()).hexdigest() for x in test]
    tr={hashes[i] for i in train};va={hashes[i] for i in val};te=set(test_hashes)
    stats={'train':len(train),'validation':len(val),'test':len(test),'classes':len(np.unique(labels)),
           'shape':list(images.shape[1:]),'train_per_class':np.bincount(labels[train]).tolist(),
           'validation_per_class':np.bincount(labels[val]).tolist(),'test_per_class':np.bincount(test_labels).tolist(),
           'train_unique_images':len(tr),'validation_unique_images':len(va),'test_unique_images':len(te),
           'exact_overlap_train_val':len(tr&va),'exact_overlap_train_test':len(tr&te),'exact_overlap_val_test':len(va&te),
           'development_duplicate_count':len(images)-len(set(hashes)),
           'train_rgb_mean_01':(images[train].mean(axis=(0,1,2))/255).tolist(),
           'mirror_revision':REVISION,'ordered_pixels_match_original_training':True,
           'note':'Post-hoc exact pixel duplicate audit; splits and measured training are not changed. Near duplicates are not measured.'}
    (destination/'dataset.json').write_text(json.dumps(stats,indent=2)+'\n')
    rng=np.random.default_rng(2026);indices=rng.choice(train,20,replace=False)
    fig,axes=plt.subplots(4,5,figsize=(10,8))
    for ax,index in zip(axes.flat,indices):
        ax.imshow(images[index]);ax.set_title(f'{split["classes"][labels[index]]}\ntrain index {index}',fontsize=8);ax.axis('off')
    fig.tight_layout();fig.savefig(destination/'training_samples.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,3.8));x=np.arange(100)
    for values,label,color in [(stats['train_per_class'],'Train','#263e35'),(stats['validation_per_class'],'Validation','#b74c32'),(stats['test_per_class'],'Test','#b5c69d')]:
        ax.plot(x,values,label=label,color=color,linewidth=2)
    ax.set(xlabel='Fine class index (0–99)',ylabel='Images per class',ylim=(0,510));ax.legend();ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(destination/'class_counts.png',dpi=160);plt.close(fig)
    return stats


if __name__=='__main__':print(json.dumps(explore(),indent=2))


def overlap_sensitivity(destination=None):
    import csv
    import statistics
    destination=Path(destination or ROOT/'reports/image/analysis')
    images,labels=load_images('train');test,test_labels=load_images('test')
    train,val=stratified_split(labels)
    tr={hashlib.sha256(images[i].tobytes()).hexdigest() for i in train}
    va={hashlib.sha256(images[i].tobytes()).hexdigest() for i in val}
    test_hashes=[hashlib.sha256(x.tobytes()).hexdigest() for x in test]
    excluded=[i for i,h in enumerate(test_hashes) if h in tr]
    overlap={'train_validation_shared_hashes':sorted(tr&va),'test_indices_matching_train':excluded,
             'test_image_hashes':{str(i):test_hashes[i] for i in excluded},
             'note':'Exact pixel equality only. Post-hoc sensitivity on fixed predictions, no new checkpoint selection or retraining.'}
    (destination/'overlap.json').write_text(json.dumps(overlap,indent=2)+'\n')
    protocol=json.loads((ROOT/'configs/image.json').read_text());rows=[];groups=[]
    for experiment in protocol['experiments']:
        for seed in protocol['seeds']:
            path=ROOT/'reports/image/generated/evidence'/experiment['id']/f'seed_{seed}'/'predictions_test.csv'
            with path.open() as f:predictions=list(csv.DictReader(f))
            kept=[p for p in predictions if int(p['index']) not in set(excluded)]
            cm=np.zeros((100,100),dtype=np.int64)
            for p in kept:cm[int(p['target']),int(p['prediction'])]+=1
            rows.append({'experiment':experiment['id'],'seed':seed,'n':len(kept),
                         'accuracy':float(cm.trace()/cm.sum()),
                         'macro_f1':float(np.mean(2*np.diag(cm)/np.maximum(cm.sum(0)+cm.sum(1),1)))})
        own=rows[-3:]
        groups.append({'experiment':experiment['id'],'accuracy':statistics.mean(x['accuracy'] for x in own),
                       'sd':statistics.stdev(x['accuracy'] for x in own)})
    result={'excluded_test_images':len(excluded),'retained_test_images':10000-len(excluded),'groups':groups,'runs':rows,
            'note':'These are not leakage-free retraining results. Two train/validation duplicate pixel hashes remain in the measured selection protocol.'}
    (destination/'sensitivity.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
