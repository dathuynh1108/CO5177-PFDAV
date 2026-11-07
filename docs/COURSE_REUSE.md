# Current studies and historical reuse

CO5177 now has independently executed Tabular, full-article Text, headline Text, and Image notebooks. Imported CO5085 A1 results and the supplied Kaggle PhoBERT notebook remain historical records; their measurements are not substituted for the current runs.

## Current CO5177 evidence

| Study | Current execution | Evidence |
| --- | --- | --- |
| Tabular | All 48,780 cleaned Adult records; four fitted models; 34,146/7,317/7,317 split | [Notebook](../notebooks/tabular.ipynb), [notebook evidence](../reports/tabular/notebook-evidence/metrics.json) |
| Text | All 207,375 valid articles; 207,108 final-input groups; 145,162/31,107/31,106 split; all seven fine-tuning epochs on RTX 5090; epoch 6 selected on validation | [Notebook](../notebooks/text.ipynb), [metrics](../reports/text/notebook-evidence/metrics.json) |
| Text headlines | Four classifiers fitted using the same complete corpus, article IDs, and grouped partitions | [Notebook](../notebooks/text.ipynb), [protocol and scores](STUDIES_PROTOCOL.md) |
| Image | Six pretrained configurations × three seeds × 20 epochs on RTX 5090; exact-pixel deduplication leaves 44,976/5,000/9,998 images | [Notebook](../notebooks/image.ipynb), [18-run summary](../reports/image/notebook-evidence/summary.json), [execution receipt](../reports/image/notebook-evidence/execution-receipt.json) |

Text uses VietnamNet News published on student Huỳnh Thành Đạt's Hugging Face account. Equal final headline or Head–Tail article token inputs remain in the same partition; grouping removes no valid records. Test accuracy/macro-F1 after validation calibration are 91.889025%/0.911218. Frozen PhoBERT + logistic regression on headlines reaches 80.926509%/0.793345; differing inputs prevent attributing the entire difference to fine-tuning.

Current Image full fine-tuning reaches three-seed mean accuracy 79.16% for ResNet18 and 86.81% for Swin-T. These differ from the archived A1 measurements below. The notebook has 21 executed code cells, six PNG outputs, and no error outputs.

## Original CO5085 comparison

The earlier reuse review inspected CO5085 assignment PDFs, `docs/REQUIREMENTS.md`, source, and saved configurations at commit `7fa80cef7e53e79846a2a1714ce08626ff65c4b4`. Instructor permission for equivalent reuse was reported by Huỳnh Thành Đạt on 19 October 2026.

| CO5085 work at that review | CO5177 relationship |
| --- | --- |
| A1: CIFAR-100, ResNet18 and Swin-T; scratch, head-only, partial and full fine-tuning | Source for the ported Image implementation and historical comparison |
| E1: Fashion-MNIST classifiers | Not the main Image dataset permitted by the CO5177 brief |
| E2: attention over Fashion-MNIST rows, patches and CNN features | Image-sequence experiments, not a Text study |
| E3: LSTM/GRU over Fashion-MNIST rows or patches | Image inputs, not actual text samples |
| A2: no completed study in the original review snapshot | No A2 material transferred in that review |

Tabular has no corresponding CO5085 experiment. The VietnamNet studies are separate from CO5085.

## Archived A1 material

| Material | Original location | CO5177 location |
| --- | --- | --- |
| Data, models, training loop, metrics and runner | `A1/{data,models,metrics,engine,protocol,run_suite,visuals}.py`, `common/runtime.py` | [`src/image/`](../src/image/) |
| Eight configurations, seeds 42/43/44 | `configs/a1_experiments.json` | [`configs/image.json`](../configs/image.json), byte-identical |
| 24 histories, metadata, splits, predictions and evaluations | `A1/reports/generated/evidence/` | [`reports/image/generated/evidence/`](../reports/image/generated/evidence/) |
| Summary, tables and measured figures | `A1/reports/generated/` | [`reports/image/generated/`](../reports/image/generated/) |
| Freeze, augmentation, checkpoint and resume checks | A1 tests | [`tests/test_training_contract.py`](../tests/test_training_contract.py) |

The measured release is [`1250e56`](https://github.com/dathuynh1108/CO5085-deep-learning/tree/1250e569c6ce055391b5670e2f9a31faedb44b20), before CO5085's later layout change. The [reuse manifest](../reports/image/reuse-manifest.json) records 186 imported artifacts, nine ported Python modules, and additional figure sources. Imported evidence bytes and signatures remain preserved. Changed imports and paths give ported code a new identity; it cannot resume the original checkpoints.

Archived test accuracy, mean ± sample SD over three seeds:

| Architecture | Head-only | Partial | Full |
| --- | --- | --- | --- |
| ResNet18 | 60.95 ± 0.29% | 73.96 ± 0.12% | 78.97 ± 0.04% |
| Swin-T | 71.67 ± 0.09% | 78.25 ± 0.22% | 86.63 ± 0.22% |

The archived split contains two exact pixel contents shared between train/validation and ten between train/test. The old 9,990-prediction sensitivity analysis is not the current deduplicated training study. See [IMAGE_REUSE.md](IMAGE_REUSE.md) and [TEXT_REUSE.md](TEXT_REUSE.md) for archive limitations.

## Submission status

Current notebooks contain English presentation and real Jupyter outputs; reports are Vietnamese. The landing page uses notebooks as experiment entry points. Tabular has completed a fresh hosted Google Colab Run all. Text and Image Colab checks, GroupLink, and LMS submission remain incomplete or unverified. YouTube fields are intentionally blank; the brief's video requirement remains outstanding. See [SUBMISSION_REVIEW.md](SUBMISSION_REVIEW.md).
