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

Each assignment has its own notebook and report. The notebooks are the primary workflow: open the current notebook in Colab, choose a GPU runtime for the full Text and Image experiments, then use **Runtime → Run all**. Each experiment prints its data audit, configuration and seeds, validation/training log, metrics and charts. Tabular and the separate headline baseline have both been executed locally from fresh kernels. The current full Text run was fine-tuned on an RTX 5090. All 18 Image runs completed on RTX 5090 GPUs after exact-pixel deduplication. The prior PhoBERT notebook is preserved separately as [`text_historical.ipynb`](notebooks/text_historical.ipynb) for provenance. The [cross-course comparison](docs/COURSE_REUSE.md) and [submission checklist](docs/SUBMISSION_REVIEW.md) explain evidence status. YouTube fields remain blank pending presentation links.

## Technology

The website uses static HTML5, CSS3 and vanilla JavaScript; it needs no backend, package installation or build step. The interface is in English. Notebooks and reports are in Vietnamese. Python dependencies are needed for the experiments and their checks.

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
├── notebooks/                 # Main notebooks plus the separate Text baseline
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
| Text · full articles | 7,600 VietnamNet articles; PhoBERT fine-tuning | 83.7719% | 0.835296 | RTX 5090 run; shared 5,320/1,140/1,140 split |
| Text · validation calibrated | Same full-article model with validation-fitted calibration | 83.2456% | 0.829602 | Same held-out test split; calibrated decisions |
| Text · headline baseline | 7,600 headlines; frozen PhoBERT + logistic regression | 77.5439% | 0.773780 | Fresh local notebook run; 5,320/1,140/1,140 split |
| Image | CIFAR-100; Swin-T full fine-tuning | 86.81% | 0.8681 | 9,998 held-out images after exact-pixel deduplication |

The full Text study uses 7,600 articles collected by Huỳnh Thành Đạt from public VietnamNet URLs and published as the [`vietnamnet-news` dataset](https://huggingface.co/datasets/dathuynh1108/vietnamnet-news). It fine-tunes PhoBERT and uses the same stratified 5,320/1,140/1,140 split as the separate headline comparison. Calibration is fit on validation; its test metrics are listed separately. The headline baseline uses headlines only and frozen PhoBERT features, so it is not a direct model comparison with full-article fine-tuning.

| Notebook | Run in Colab |
| --- | --- |
| [Tabular · UCI Adult](notebooks/tabular.ipynb) | [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/tabular.ipynb) |
| [Text · full-article PhoBERT](notebooks/text.ipynb) | [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text.ipynb) |
| [Text · headline baseline](notebooks/text_baselines.ipynb) | [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text_baselines.ipynb) |
| [Image · CIFAR-100](notebooks/image.ipynb) | [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb) |

The Text run requires a GPU for practical fine-tuning; Image trains six configurations over three seeds and 20 epochs. A full Colab Run all has not been independently verified. New Tabular and headline-baseline runs save their configuration, seeds, fit history, metrics, predictions and plots to a fresh ignored `artifacts/notebook-runs/` directory. The Text archive [`text_historical.ipynb`](notebooks/text_historical.ipynb) preserves the prior Kaggle/Tesla T4 run and its original outputs; it is historical evidence, not a current result. Further provenance is recorded in [TEXT_REUSE.md](docs/TEXT_REUSE.md).

[Tabular PDF](reports/tabular/tabular.pdf) · [Full Text PDF](reports/text/text.pdf) · [Headline baseline PDF](reports/text/baselines.pdf) · [Image PDF](reports/image/image.pdf) · [New-study protocol](docs/STUDIES_PROTOCOL.md)

## Image study

[Image notebook](notebooks/image.ipynb) · [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb) · [PDF](reports/image/image.pdf) · [LaTeX](reports/image/report.tex) · [Run evidence](reports/image/notebook-evidence/summary.json)

The Image notebook trained six pretrained configurations with seeds 42–44 for 20 epochs. Exact RGB duplicates were removed after the stratified split, leaving 44,976 training, 5,000 validation and 9,998 test images. Swin-T and ResNet18 reached 86.81% and 79.16% test accuracy in full fine-tuning. Earlier CO5085 A1 measurements remain documented as historical reuse in [IMAGE_REUSE.md](docs/IMAGE_REUSE.md) and are not results of this CO5177 run. CIFAR-100 images are 32px before resizing; the experimental input is 96px, below the brief's recommended 128px short edge. `AI_USE_REPORT.md` records the assistance used.
