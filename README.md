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

## Team

| Student ID | Name |
| --- | --- |
| 2570161 | Huỳnh Thành Đạt |
| 2570083 | Lương Minh Duy |

## Selected assignments

| Assignment | Data type | Track | Overview |
| --- | --- | --- | --- |
| 01 | [Tabular](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/tabular.html) | Required | Structured-data exploration, preprocessing and modeling. |
| 02 | [Text](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/text.html) | Required | Corpus exploration, text representations and analysis. |
| 03 | [Image](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/image.html) | Selected elective | Visual exploration, feature extraction and model evaluation. |

All three tracks have source code, an executed notebook and a separate LaTeX/PDF report. Tabular and Text are new CO5177 experiments; Image reuses the code and 24 measured runs from CO5085 A1. The [cross-course comparison](docs/COURSE_REUSE.md) documents that match. Presentation videos and the consolidated LMS report are still pending.

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
├── src/studies/               # New Tabular/Text studies and evidence audit
├── configs/                   # Separate image, tabular and text configurations
├── notebooks/                 # One executed notebook per track
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

Edit `assets/site-config.js` to set the registered group name, member contributions, GitHub profiles and assignment resource links. For example, after a report is available:

```js
report: 'reports/tabular/tabular.pdf'
```

Use HTTPS URLs for external resources and project-relative paths for repository files. Leave unavailable resources empty; the page displays their publication status without creating broken links. Do not put credentials or private information in this public configuration file.

Main page copy and requirement summaries live in the corresponding HTML files. Keep these in sync with the configuration when updating published content so that the no-JavaScript view remains accurate.

## Accessibility and presentation

The site includes responsive layouts, keyboard-accessible navigation, a skip link, visible focus states, reduced-motion support and print styles. Core content is available without JavaScript. Fonts are loaded from Google Fonts with local system fallbacks; font files are not stored in the repository.

## Assignment reference

Requirements are summarized from **Course Assignment v4.0, dated 14 September 2026**, for Semester 261. The official assignment brief and course LMS announcements determine final requirements and deadlines.

## Tabular and Text studies

| Study | Modeling data | Model selected by validation | Test accuracy | Test macro-F1 |
| --- | --- | --- | --- | --- |
| Tabular | 48,780 deduplicated Adult rows, 14 features | Histogram gradient boosting | 87.48% | 0.8185 |
| Text | 7,600 VietnamNet headlines, 19 classes | Frozen PhoBERT + logistic regression | 77.54% | 0.7738 |

Both use one fixed stratified split and model seed. Text audits all 212,705 source articles before selecting its balanced cohort; it does not train on the entire corpus. The frozen encoder is pinned VinAI PhoBERT, since the old user model repository has no weights. These results are new measurements and do not reuse NER evaluation scores.

[Tabular notebook](notebooks/tabular.ipynb) · [Tabular PDF](reports/tabular/tabular.pdf) · [Tabular LaTeX](reports/tabular/report.tex)
[Text notebook](notebooks/text.ipynb) · [Text PDF](reports/text/text.pdf) · [Text LaTeX](reports/text/report.tex)
[Data, models and protocol](docs/STUDIES_PROTOCOL.md)

```bash
.venv/bin/python -m pip install -r requirements-studies.txt
.venv/bin/python -m pip install --no-deps -e .
.venv/bin/python -m studies.tabular
.venv/bin/python -m studies.text
.venv/bin/python -m studies.audit --models
.venv/bin/python scripts/write_study_reports.py
.venv/bin/python scripts/build_report.py --track tabular
.venv/bin/python scripts/build_report.py --track text
```

Raw data, PhoBERT features and fitted classifiers remain outside Git in `data/` and `runs/`. Published predictions, source/config hashes, dataset checksums, class metrics and figures are in `reports/<track>/generated/`. The notebooks rerun training; local execution has been checked, while a fresh Google Colab session has not been tested here.

## Image study

[Image notebook](notebooks/image.ipynb) · [Open in Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb) · [PDF](reports/image/image.pdf) · [LaTeX](reports/image/report.tex) · [Source](src/image/) · [Reuse protocol](docs/IMAGE_REUSE.md)

| Pretrained model | Head-only test accuracy | Partial test accuracy | Full test accuracy |
| --- | --- | --- | --- |
| ResNet18 | 60.95 ± 0.29% | 73.96 ± 0.12% | 78.97 ± 0.04% |
| Swin-T | 71.67 ± 0.09% | 78.25 ± 0.22% | 86.63 ± 0.22% |

Mean ± sample SD over seeds 42, 43, 44. The notebook includes learning curves for all six pretrained configurations; the PDF compares both full fine-tuning curves with the scratch controls.

The Image study reuses the **same** 24 CO5085 A1 runs at commit `1250e56`; no additional training was performed. Six pretrained configurations are the primary CO5177 comparisons. Data inspection and result analysis are specific to this Image report. CIFAR-100 original images are 32px, measured input is 96px, below the recommended 128px short edge; this limitation is explained. Exact-pixel duplicates cross the measured splits (2 train/validation, 10 train/test shared image contents); the report includes a fixed-prediction sensitivity check and does not claim leakage-free retraining.

Python code is organized under `src/image/`, with `configs/image.json`, `notebooks/`, `tests/`, and separate `reports/image/`. The static site still runs without Python dependencies or a build. See `docs/IMAGE_REUSE.md` for Python setup and audit commands. `python -m image.analysis` verifies the import hashes and reproduces all 24 metrics from held-out predictions. `AI_USE_REPORT.md` records the assistance used.
