# Current experiment protocol

The entry points are [Tabular](../notebooks/tabular.ipynb), [full-article Text](../notebooks/text.ipynb), [headline Text](../notebooks/text_baselines.ipynb), and [Image](../notebooks/image.ipynb). Current notebooks use English presentation and actual Jupyter outputs. Reports use Vietnamese. Tabular has completed a fresh hosted Google Colab Run all with 17 executed code cells and no errors; the exported execution is in `reports/tabular/notebook-evidence/colab-executed.ipynb`. Text and Image Colab checks remain incomplete.

## Environment and evidence

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-studies.txt
.venv/bin/python -m pip install --no-deps -e .
```

Run the notebooks from fresh kernels, with a GPU for full-article fine-tuning and Image. Raw data, model caches, and weights stay outside Git. Run directories store configuration, seeds, split IDs, fitting history, metrics, predictions, and figures. Published notebook evidence is separate from imported historical evidence. Verification JSON files record the checks performed for their respective snapshots; they do not certify later notebook execution or external submission.

## Tabular: UCI Adult

Source: [UCI Adult](https://archive.ics.uci.edu/dataset/2/adult), DOI `10.24432/C5XW20`, CC BY 4.0. The archive checksum is pinned in `configs/tabular.json`.

- Inspect all 48,842 source rows and 14 predictors, including genuine missing values, six numerical columns, and eight categorical columns.
- Combine the official files; remove 10 conflicting-label rows and 52 repeated rows before splitting. Use all 48,780 remaining records.
- Stratify into 34,146/7,317/7,317 train/validation/test records using seeds 2026 and 2027. These are new partitions, not the official test split.
- Numerical summaries, histograms, and IQR flags use train only. Retain flagged values: the flags do not establish invalid observations.
- Fit median/most-frequent imputation on train only. Logistic models use scaling and one-hot encoding; histogram boosting uses ordinal encoding with explicit categorical positions.
- Fit majority, logistic regression, balanced logistic regression, and histogram gradient boosting. Select logistic C from `{0.1, 1, 10}` using validation macro-F1. Boosting uses 150 iterations, 31 leaves, L2=1, no early stopping; model seed 42.
- Finish validation selection before test predictions. Report accuracy, macro-F1, class precision/recall, and confusion. `fnlwgt` is a predictor, not a sample weight.

## Text: shared full-corpus partitions

Source: [VietnamNet News](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news), published on student Huỳnh Thành Đạt's Hugging Face account, revision `d70a9601f36dcb1e5c534d30e2d3921c2ba16284`. The 19 source parquet checksums are pinned in `configs/text.json`. Article-content redistribution terms are unspecified in the dataset card; raw articles remain outside Git.

- Inspect all 212,705 source rows. Remove 1,167 empty headlines, 3,636 rows in conflicting-category components, and 527 other duplicates. Keep all 207,375 valid articles, including seven with empty bodies; apply no sampling cap.
- Deduplication uses connected components of canonical URL, normalized casefolded headline, or nonempty normalized casefolded body.
- Prepare final headline and Head–Tail article token IDs. Union records sharing either input into 207,108 groups. This grouping removes no rows.
- Use 20-fold `StratifiedGroupKFold`, shuffle enabled, seed 2026. Assign 14/3/3 folds to train/validation/test: 145,162/31,107/31,106 records. Equal input groups remain together. Both Text notebooks share these IDs and splits.

### Headline classifiers

Fit four classifiers on titles only: majority, word TF-IDF + Linear SVM, character TF-IDF + Linear SVM, and frozen PhoBERT + logistic regression. URL, body, and category strings are excluded from headline inputs.

TF-IDF vocabulary and IDF fit train only: word n-grams 1–2 or character-within-word n-grams 3–5, min-df=2, max-df=.98, sublinear TF, at most 80,000 features. Select C from `{0.5, 1, 2}` using validation macro-F1; model seed 42.

PhoBERT uses `vinai/phobert-base-v2`, revision `86cd7fd4c148980922ac11a2cf5e257f2ba639e1`, PyVi segmentation, maximum length 128, and masked mean pooling including BOS/EOS. The encoder remains frozen. The completed notebook fits all four classifiers on CPU using a verified cache of frozen embeddings originally encoded on RTX 5090; it contains 19 executed code cells and two PNG outputs.

| Headline classifier | Test accuracy | Test macro-F1 |
| --- | ---: | ---: |
| Majority | 6.002057% | 0.005960 |
| Word TF-IDF + Linear SVM | 80.190317% | 0.783883 |
| Character TF-IDF + Linear SVM | 80.251398% | 0.785580 |
| Frozen PhoBERT + logistic regression | 80.981161% | 0.794315 |

### Full-article fine-tuning

The current RTX 5090 run completes all seven epochs with effective batch size 64. Article input combines the title with the first 220 and last 80 body words, followed by Head–Tail token selection to maximum length 256. Class weights use train only. Checkpoint selection uses validation macro-F1 and selects epoch 7. Temperature and class thresholds fit validation before test evaluation.

Test accuracy/macro-F1 are 91.840802%/0.910916 before calibration and 91.892239%/0.911448 after validation calibration. [Published metrics](../reports/text/notebook-evidence/metrics.json), [input audit](../reports/text/notebook-evidence/input_audit.json), and [split audit](../reports/text/notebook-evidence/split_audit.json) record this run. Headline-only and article inputs differ, so the comparison does not isolate backbone fine-tuning alone.

## Image and historical material

Image completes six pretrained configurations × three seeds × 20 epochs on RTX 5090 GPUs, using 44,976/5,000/9,998 images after exact-pixel deduplication. The executed notebook contains 21 code cells, six PNG outputs, and no errors; see its [execution receipt](../reports/image/notebook-evidence/execution-receipt.json).

[TEXT_REUSE.md](TEXT_REUSE.md) and [IMAGE_REUSE.md](IMAGE_REUSE.md) distinguish current results from the byte-preserved Kaggle notebook and imported CO5085 A1 evidence. The [submission checklist](SUBMISSION_REVIEW.md) records unverified Colab and external submission items.
