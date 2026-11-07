# CO5177 · PFDAV

Course project website for **Programming Foundations for Data Analysis and Visualization**.

**[Visit the website](https://dathuynh1108.github.io/CO5177-PFDAV/)**

## Course

| Field | Details |
| --- | --- |
| University | Ho Chi Minh City University of Technology, VNU-HCM |
| Faculty | Computer Science and Engineering |
| Course code | CO5177 |
| Instructor | Lê Thành Sách |
| Semester | 261 · Academic year 2026–2027 |

## Team CTG

| Student ID | Name | Contribution |
| --- | --- | --- |
| 2570161 | Huỳnh Thành Đạt | 50% |
| 2570083 | Lương Minh Duy | 50% |

## Selected assignments

| Assignment | Data type | Track | Overview |
| --- | --- | --- | --- |
| 01 | [Tabular](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/tabular.html) | Required | Structured-data exploration, preprocessing and modeling. |
| 02 | [Text](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/text.html) | Required | Corpus exploration, text representations and analysis. |
| 03 | [Image](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/image.html) | Selected elective | Visual exploration, feature extraction and model evaluation. |

Each assignment has a notebook and a Vietnamese report. The landing page links to the notebooks as the experiment entry points. Current notebooks contain English Markdown, code presentation, and actual Jupyter outputs. Tabular fits four classifiers on all cleaned Adult records; Text fine-tunes on all valid articles and includes four headline classifiers; Image completes 18 training runs on RTX 5090 GPUs. Tabular has also completed a fresh hosted Google Colab Run all (17 code cells, three PNG outputs, no errors). Fresh Colab checks for Text and Image remain incomplete. The prior PhoBERT notebook remains byte-identical at [`text_historical.ipynb`](notebooks/text_historical.ipynb). See the [reuse record](docs/COURSE_REUSE.md) and [submission checklist](docs/SUBMISSION_REVIEW.md). YouTube fields are intentionally blank.

## Technology

The website uses static HTML5, CSS3 and vanilla JavaScript; it needs no backend, package installation or build step. The interface is in English. Current notebooks are in English; reports are in Vietnamese. The historical notebook preserves its original language and outputs. Python dependencies are needed for the experiments and their checks.

## Repository structure

```text
.
├── index.html                 # Course and team landing page
├── requirements.html          # Assignment brief summary
├── assignments/
│   ├── tabular.html           # Assignment 01
│   ├── text.html              # Assignment 02
│   └── image.html             # Assignment 03
├── assets/
│   ├── styles.css             # Design system and responsive styles
│   ├── site-config.js         # Team settings and resource links
│   ├── app.js                 # Navigation and configuration handling
│   └── favicon.svg
├── src/image/                 # Ported Image training and evidence audit
├── src/studies/               # New Tabular/headline baseline studies
├── src/text_reuse/            # Full PhoBERT notebook provenance and result audit
├── configs/                   # Separate image, tabular and text configurations
├── notebooks/                 # One main notebook for each data modality
├── reports/                   # Separate image/, tabular/ and text/ reports
├── docs/                      # Requirements mapping and reuse provenance
├── scripts/                   # Report compilation and site checks
├── tests/                     # Training contracts and evidence checks
├── .github/workflows/         # CPU checks
├── requirements.txt
├── requirements-studies.txt   # Additional dependencies for Tabular/Text
├── pyproject.toml
├── AI_USE_REPORT.md
├── .gitignore
└── .nojekyll
```

## Run locally

```bash
git clone https://github.com/dathuynh1108/CO5177-PFDAV.git
cd CO5177-PFDAV
python3 -m http.server 8000
```

Open **http://localhost:8000**. Core page content is also readable by opening `index.html` directly.

## Deploy to GitHub Pages

In **Settings → Pages → Build and deployment**, select:

```text
Source: Deploy from a branch
Branch: main
Folder: / (root)
```

Save the settings. GitHub Pages publishes the files from `main`. No custom GitHub Actions workflow is needed. Internal assets and links use relative paths compatible with the `/CO5177-PFDAV/` project URL. The `.nojekyll` file disables Jekyll processing.

## Update content

The registered group name and contribution percentages are recorded in `assets/site-config.js`. The file also holds member GitHub profiles and assignment resource links. For example, after a report is available:

```js
report: 'reports/tabular/tabular.pdf'
```

Use HTTPS URLs for external resources and project-relative paths for repository files. Leave unavailable resources empty; the page displays their publication status without creating broken links. Do not put credentials or private information in this public configuration file.

Main page copy and requirement summaries live in the corresponding HTML files. Keep these in sync with the configuration when updating published content so that the no-JavaScript view remains accurate.

## Accessibility and presentation

The site includes responsive layouts, keyboard-accessible navigation, a skip link, visible focus states, reduced-motion support and print styles. Core content is available without JavaScript. Fonts are loaded from Google Fonts with local system fallbacks; font files are not stored in the repository.

## Assignment reference

Requirements are summarized from **Course Assignment v4.0, dated 14 September 2026**, for Semester 261. The official assignment brief and course LMS announcements determine final requirements and deadlines.

## Experiments and current evidence

| Study | Data and model | Accuracy | Macro-F1 | Evaluation |
| --- | --- | --- | --- | --- |
| Tabular | 48,780 deduplicated UCI Adult rows; histogram gradient boosting | 87.4812% | 0.818526 | Fresh local notebook run; 34,146/7,317/7,317 train/validation/test split |
| Text · full articles | All 207,375 valid VietnamNet articles; PhoBERT fine-tuning | 91.831158% | 0.910653 | RTX 5090; seven epochs; 145,162/31,107/31,106 grouped split |
| Text · validation calibrated | Same full-article model; calibration fitted on validation | 91.889025% | 0.911218 | Same held-out test records |
| Text · headline baseline | All 207,375 headlines; frozen PhoBERT + logistic regression | 80.926509% | 0.793345 | Four classifiers fitted on CPU using the same grouped split |
| Image | CIFAR-100; Swin-T full fine-tuning | 86.81% | 0.8681 | Three-seed mean; 9,998 held-out images after exact-pixel deduplication |

Text uses the [`vietnamnet-news` dataset](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news) published on the Hugging Face account of student Huỳnh Thành Đạt. This records the dataset publisher, without attributing article collection. All 207,375 valid records from 212,705 source rows are retained. Equal final headline token IDs or Head–Tail article token IDs form 207,108 groups; grouping removes no rows. A 20-fold `StratifiedGroupKFold` with seed 2026 assigns 14/3/3 folds to training/validation/test. Article and headline models use identical article IDs and partitions. Fine-tuning completes all seven epochs with effective batch size 64 and selects epoch 6 by validation macro-F1. Temperature and class thresholds are fitted on validation before test evaluation. Headline-only and article inputs differ, so the comparison does not isolate the effect of fine-tuning alone.

| Notebook | Run in Colab |
| --- | --- |
| [Tabular · UCI Adult](notebooks/tabular.ipynb) | [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/tabular.ipynb) |
| [Text · PhoBERT and headline baselines](notebooks/text.ipynb) | [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text.ipynb) |
| [Image · CIFAR-100](notebooks/image.ipynb) | [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb) |

The Text notebook contains 38 executed code cells and six PNG outputs, with no errors; it fine-tunes the article model and fits all four headline baselines in one run. Text fine-tuning uses a GPU; Image trains six configurations over three seeds for 20 epochs each. The executed Image notebook contains 21 code cells, six PNG outputs, and no error outputs. Fresh run directories retain configurations, seeds, fitting history, metrics, predictions, and plots. [Text evidence](reports/text/notebook-evidence/metrics.json) and [Image execution receipt](reports/image/notebook-evidence/execution-receipt.json) accompany the reports. The Text archive [`text_historical.ipynb`](notebooks/text_historical.ipynb) preserves the prior Kaggle/Tesla T4 run and its original outputs; it is historical evidence, not a current result. Further provenance is recorded in [TEXT_REUSE.md](docs/TEXT_REUSE.md).

[Tabular PDF](reports/tabular/tabular.pdf) · [Full Text PDF](reports/text/text.pdf) · [Image PDF](reports/image/image.pdf) · [New-study protocol](docs/STUDIES_PROTOCOL.md)

## Image study

[Image notebook](notebooks/image.ipynb) · [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb) · [PDF](reports/image/image.pdf) · [LaTeX](reports/image/report.tex) · [Run evidence](reports/image/notebook-evidence/summary.json)

The Image notebook trained six pretrained configurations with seeds 42–44 for 20 epochs. Exact RGB duplicates were removed after the stratified split, leaving 44,976 training, 5,000 validation and 9,998 test images. Swin-T and ResNet18 reached 86.81% and 79.16% test accuracy in full fine-tuning. Earlier CO5085 A1 measurements remain documented as historical reuse in [IMAGE_REUSE.md](docs/IMAGE_REUSE.md) and are not results of this CO5177 run. CIFAR-100 images are 32px before resizing; the experimental input is 96px, below the brief's recommended 128px short edge. `AI_USE_REPORT.md` records the assistance used.
