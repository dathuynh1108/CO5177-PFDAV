# Full-corpus PhoBERT study

The main Text study is the executed full-training notebook supplied by Huỳnh Thành Đạt on 19 October 2026. It replaces the earlier headline-only study as the main notebook and report; that newer experiment remains a separate baseline study.

## Source and measured runtime

- Source: [phobert-news-classification-app](https://github.com/dathuynh1108/phobert-news-classification-app), commit `e17168883b8a80a5c77b670018dd9ac8afb15913`.
- Attachment: `notebookb4f8845517.ipynb`, SHA256 `32a22cbe811bc8f1035cd80b819a5eb8da0e2390ca3b5d6ca32dbcca9c238c66`.
- [`notebooks/text.ipynb`](../notebooks/text.ipynb) is byte-identical to the attachment, including historical outputs. All 36 cell sources match the pinned repository notebook; 25 code cells have outputs and seven PNG figures are embedded.
- Historical runtime: Kaggle, two Tesla T4 GPUs, Python 3.12.12, PyTorch 2.10.0+cu128. Papermill records 26 April 2026 11:01–22:02 UTC (26–27 April in Vietnam). Fine-tuning took about 38,115 seconds; the whole notebook took 39,660 seconds. These are historical timings, not a new run on Vast or this Mac.
- The repository's first-commit notebook has 213,954 rows and different results. Those figures and scores are **not** mixed into this 212,705-row run.

## Complete pipeline

| Section | Processing | Observed output |
| --- | --- | --- |
| 0 | Dependencies, device, precision, paths, dataset download/check | Two T4s; FP16; batch 16/GPU; accumulation 2; effective batch 64 |
| 1 | Batched loading of all 19 parquet files | 212,705 rows; 1,167 missing titles; seven missing bodies; zero missing both |
| 2 | Class distribution, word length and per-class summary | Imbalance 3.73×; median length 625 words |
| 3 | Title + compact body, lowercase, punctuation/digit removal, PyVi and cache | All rows retained; body first 220 + last 80 words |
| 4 | Stratified 85/15 split (seed 42), balanced class weights + boosts, Head–Tail tensors | 180,799 train / 31,906 evaluation; 127+127 subwords plus special tokens |
| 5 | Sequence classifier + weighted cross-entropy; all parameters trainable | Seven epochs, 19,775 steps; AdamW, LR 2e-5, weight decay .01, warmup 200; select checkpoint by macro-F1 |
| 6 | Argmax, class report, confusion, class F1, curves and support analysis | Accuracy .905190; weighted-F1 .905308; macro-F1 .898581 |
| 7 | Save model, tokenizer and label metadata; sampled smoke inference | 19-class PhoBERT head, not a logistic regression classifier |
| 8.0 | Temperature via bounded NLL minimization [.5, 5]; ECE with 15 bins | T=1.4583027; printed NLL .3828→.3237; ECE .0608→.0218 |
| 8.1–8.3 | Coordinate search: 200 thresholds [.3, 3.5], three passes; export JSON | Accuracy .908638; weighted-F1 .908457; macro-F1 .901626 |
| 9 | Weak/minority classes, precision/recall trade-offs, confusion pairs | Largest calibrated confusion: Thời sự→Pháp luật, 236 rows |

Prediction uses `argmax(softmax(logits / T) / thresholds)`. Temperature alone preserves argmax. The threshold ratios are ranking scores, not normalized probabilities; this remains single-label classification. Coordinate search optimizes one current class's F1 at a time, not a guaranteed global macro-F1 optimum.

## Evidence and limits

[`reuse-manifest.json`](../reports/text/reuse-manifest.json) records the source commit, attachment identity, 17 imported-file hashes and checkpoint/tokenizer identities. Metadata in `reports/text/reused/evidence/` is copied byte-for-byte from the pinned `train/artifacts/active/`. Seven figures in `reports/text/reused/figures/` are decoded directly from the supplied outputs, with cell/output indices.

`python -m text_reuse.analysis` verifies all imported hashes and recomputes calibrated accuracy, macro/weighted F1, class precision/recall/F1 and normalized confusion from the count matrix. Before-calibration class metrics and epoch metrics are parsed from printed output (four and six decimals). NLL/ECE remain historical printed values: raw logits are unavailable.

The original `test_dataset` also serves as epoch evaluation and calibration data. The scores are **not an untouched independent-test estimate**. Exact split membership and source file checksums/revision were not recorded by this run. Matching counts do not prove identical data bytes. The old workflow does not deduplicate before splitting. Its checkpoint reload logs contain LayerNorm beta/gamma versus weight/bias warnings, which remain a reproducibility limitation. No warning or split issue is silently repaired while retaining the old score.

The newer headline experiment uses an audited 7,600-headline cohort and its own train/validation/test split. Its 77.54% cannot be ranked directly against full-article fine-tuning because inputs, volume, priors and evaluation roles differ. See [`text_baselines.ipynb`](../notebooks/text_baselines.ipynb), [`baselines.pdf`](../reports/text/baselines.pdf) and [`STUDIES_PROTOCOL.md`](STUDIES_PROTOCOL.md).

## Review and reproduce

Opening the main notebook only displays saved outputs. **Run All in a fresh runtime performs full training** unless the notebook's model-cache condition is satisfied. Configure paths in Section 0.3, choose an isolated workspace and clear caches after data changes. Original `train/runs/` paths are retained to preserve notebook bytes. No cell rents hardware or submits paid jobs. No fresh Kaggle/Colab run or new fine-tuning is claimed by this import.

```bash
.venv/bin/python -m text_reuse.analysis --export
.venv/bin/python scripts/build_report.py --track text
.venv/bin/python -m studies.audit --models  # newer baseline evidence
```

To re-import the attachment with the pinned source checkout:

```bash
.venv/bin/python scripts/import_text_study.py \
  --notebook /path/to/notebookb4f8845517.ipynb \
  --source /path/to/phobert-news-classification-app
```

The full report maps Sections 0–9, including temperature, thresholds, class trade-offs, model export and diagnostics. All original images are retained. The main epoch plot is redrawn from printed values so evaluation epochs and train steps do not share one mixed-unit x-axis; it adds no observations. `reports/text/report.tex` includes `chapters/study.tex`; `baselines.tex` retains the earlier report. `write_study_reports.py` updates the baseline report and derived full-report tables, without replacing the full report prose.

The checkpoint/tokenizer was copied with SHA256 verification into ignored `runs/text-full/model/`. `scripts/check_text_model.py --model runs/text-full/model` verifies its files, loads all tensor keys under Transformers 4.57.6 and performs three synthetic CPU examples (3×19 finite logits). This local load had no missing/unexpected keys; it does not prove the historical Trainer reload had the same behavior and does not re-evaluate historical scores.
