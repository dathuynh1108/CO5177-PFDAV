"""Check the local historical checkpoint without training or fetching weights."""

import argparse
import json
import re
from pathlib import Path

import numpy as np
import torch
from pyvi import ViTokenizer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from studies.evidence import ROOT, sha256


def check(folder):
    manifest = json.loads((ROOT / "reports/text/reuse-manifest.json").read_text())
    for name, metadata in manifest["checkpoint_files"].items():
        if sha256(folder / name) != metadata["sha256"]:
            raise ValueError(f"Checkpoint/tokenizer checksum differs: {name}")
    for name in ["config.json", "label_config.json", "thresholds.json"]:
        expected = manifest["imported_files"]["reports/text/reused/evidence/" + name][
            "sha256"
        ]
        if sha256(folder / name) != expected:
            raise ValueError(f"Checkpoint metadata checksum differs: {name}")
    torch.set_num_threads(4)
    model, info = AutoModelForSequenceClassification.from_pretrained(
        folder, local_files_only=True, trust_remote_code=False, output_loading_info=True
    )
    if any(info[key] for key in ["missing_keys", "unexpected_keys", "mismatched_keys"]):
        raise ValueError("Checkpoint did not load all tensor keys")
    tokenizer = AutoTokenizer.from_pretrained(
        folder, local_files_only=True, trust_remote_code=False
    )
    examples = [
        "Đội tuyển bóng đá chuẩn bị cho giải đấu quốc tế.",
        "Bác sĩ hướng dẫn chăm sóc sức khỏe và phòng bệnh.",
        "Doanh nghiệp đầu tư công nghệ cho hoạt động sản xuất.",
    ]
    cleaned = [
        ViTokenizer.tokenize(re.sub(r"\d+", " ", re.sub(r"[^\w\s]", " ", text.lower())))
        for text in examples
    ]
    encoded = tokenizer(
        cleaned,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=256,
    )
    model.eval()
    with torch.inference_mode():
        logits = model(**encoded).logits.numpy()
    if logits.shape != (3, 19) or not np.isfinite(logits).all():
        raise ValueError("Invalid classifier logits")
    return {
        "verified_checkpoint_files": len(manifest["checkpoint_files"]),
        "tensor_load_missing_keys": [],
        "tensor_load_unexpected_keys": [],
        "parameters": sum(p.numel() for p in model.parameters()),
        "synthetic_smoke_logit_shape": list(logits.shape),
        "device": "cpu",
        "new_training_performed": False,
        "historical_scores_re_evaluated": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    options = parser.parse_args()
    print(json.dumps(check(options.model), indent=2))
