# Tabular and Text experiments

This document describes new Tabular and headline-only Text baseline experiments. Main Text now reuses the supplied full-corpus PhoBERT notebook; see [TEXT_REUSE.md](TEXT_REUSE.md) for its training, historical results and calibration. The CIFAR-100 Image study continues to reuse CO5085 A1; its source and measurements are unchanged.

## Setup and commands

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-studies.txt
.venv/bin/python -m pip install --no-deps -e .
OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 .venv/bin/python -m studies.tabular
OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 .venv/bin/python -m studies.text
.venv/bin/python -m studies.audit --models
.venv/bin/python scripts/write_study_reports.py
.venv/bin/python scripts/build_report.py --track tabular
.venv/bin/python scripts/build_report.py --track text
```

`notebooks/tabular.ipynb` and `notebooks/text_baselines.ipynb` run these studies from top to bottom, including training. A fresh Colab session clones the public repository and installs dependencies. Colab execution itself has not been verified in this local run. No command rents hardware or submits a paid job. PhoBERT uses CUDA, MPS or CPU according to local availability; the recorded encoding used MPS on an Apple M1 Pro.

Raw data and model caches stay in ignored `data/`. Eight fitted classifiers are saved under ignored `runs/tabular/` and `runs/text/`. `reports/<track>/generated/manifest.json` records classifier checksums, source/config hashes, package versions and evidence checksums. Source/config changes during a measured run stop finalization. The default audit verifies published evidence and recomputes all scores from test predictions. `--models` additionally requires the local saved classifiers. Joblib artifacts must only be loaded from this locally produced, verified run.

## Tabular: UCI Adult

Source: [UCI Adult](https://archive.ics.uci.edu/dataset/2/adult), DOI `10.24432/C5XW20`, CC BY 4.0. The official zip SHA256 is pinned in `configs/tabular.json`.

- All 48,842 source rows and 14 features are inspected. `?` denotes genuine missing values.
- Combine the official files and create a **new** split; these are not scores on the original official test split.
- Before splitting, remove all 10 records in feature-identical groups with opposing labels, then remove 52 repeated records. The retained dataset has 48,780 rows.
- Six numerical and eight categorical columns are used. Labels and record IDs are excluded by the `ColumnTransformer` feature lists.
- Stratified train/validation/test sizes are 34,146/7,317/7,317. Seed 2026 creates the train/remaining split; seed 2027 divides validation/test.
- Median and most-frequent imputers fit train only. Logistic models use scaling and one-hot encoding; histogram boosting uses explicit categorical feature positions and ordinal encoding.
- Compare majority, logistic regression, balanced logistic regression and histogram gradient boosting. Select logistic C from `{0.1, 1, 10}` by validation macro-F1. Boosting is fixed at 150 iterations, 31 leaves, L2=1, no early stopping. Model seed is 42.
- Finish all validation choices before test evaluation. Save test predictions, confusion and per-class metrics for all four models.

The dataset is imbalanced; report minority-class precision/recall alongside accuracy and macro-F1. `fnlwgt` is a feature, not a sample weight. One split and seed do not supply confidence intervals. Census data describe a historical benchmark, not contemporary income estimates.

## Text baseline study: VietnamNet headlines

Source: [`dathuynh1108/vietnamnet-news`](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news), revision `d70a9601f36dcb1e5c534d30e2d3921c2ba16284`. Use the 19 original category parquet files, **not** the separate NER configuration. All file checksums are pinned in `configs/text.json`. The dataset card does not state a redistribution license for the article content; record its status as unspecified and keep the raw corpus outside Git.

- Stream all 212,705 source articles to inspect class counts, empty headlines and body lengths. Modeling uses **headlines only**.
- Normalize NFC/whitespace, canonicalize article URLs, then union records sharing a URL or casefolded headline. Remove entire components with conflicting categories before retaining one record per remaining component.
- Remove 1,167 empty headlines, 3,628 conflicting-category rows and 296 other duplicates; 207,614 usable records remain. Near duplicates are not measured.
- Select a fixed, hash-ranked cohort of 400 headlines per class, 7,600 total. This meets the course minimum but is **not full-corpus training**. The original distribution is retained in the audit; this balanced cohort changes the class priors.
- Use the same stratified 5,320/1,140/1,140 split for all models, with the same split seeds as Tabular. Each class contributes 280/60/60 headlines. URL, body and category fields are excluded from the model input.
- Segment with PyVi 0.1.1. Verify that segmentation does not merge distinct selected inputs.
- Word TF-IDF uses n-grams 1–2; character-within-word TF-IDF uses n-grams 3–5. Both use min-df=2, max-df=.98, sublinear TF and at most 80,000 features; vocabulary/IDF fit train only. Both classifiers are Linear SVM.
- PhoBERT: `vinai/phobert-base-v2`, revision `86cd7fd4c148980922ac11a2cf5e257f2ba639e1`, model-card license AGPL-3.0. Backbone is frozen/eval; masked mean pooling includes BOS/EOS and excludes padding. FP32, maximum length 128, batch 16. No selected headline was truncated. Fit logistic regression on the 768-dimensional vectors; this is **not backbone fine-tuning**.
- Select classifier C from `{0.5, 1, 2}` using validation macro-F1, model seed 42. A majority classifier supplies a baseline. All choices finish before held-out prediction.

The NER repository initially inspected `dathuynh1108/ner-phobert-base-v2-finetuned` at revision `98f4f3ea72e5fefb125d08421216b29a9508fe39` contains only `.gitattributes`. It has no available configuration, tokenizer or weights, so this separate headline study uses the pinned VinAI pretrained model. The actual news-classification checkpoint and full training notebook were subsequently supplied; they are the main Text study documented in TEXT_REUSE.md. Existing Electra NER evaluation metrics are not reused as news-classification results.

PhoBERT feature identity includes the ordered segmented inputs, model revision, length and pooling settings. Cached vectors, model/tokenizer checksums, actual device and encoding time are recorded. Encoding uses a fixed pretrained model and learns no corpus statistics from validation/test. Report encoding cost separately from classifier fitting. Section labels may overlap in meaning; the error CSV stores source URLs for inspection without copying full articles.

## Verification and remaining submission items

The notebooks, classifier replay, tests, PDF rendering and site checks are summarized in `docs/STUDIES_VERIFICATION.json`. Presentation videos, confirmed per-member contribution details, the registered group name and the consolidated LMS report remain separate submission items. No video or registration is inferred from completed experiments.
