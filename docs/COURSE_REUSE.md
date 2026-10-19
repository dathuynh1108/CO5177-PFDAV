# Reusing CO5085 coursework in CO5177

The CIFAR-100 study in **CO5085 A1** matches the selected **Image** track in CO5177. Its training code, configuration and 24 measured runs are available here. The instructor permits reuse for equivalent work, as reported by Huỳnh Thành Đạt on 19 October 2026. The two courses therefore cite the same measurements.

## Assignment comparison

The CO5177 requirements below come from the brief summary in [requirements.html](../requirements.html). CO5085 coverage was checked against its assignment PDFs, `docs/REQUIREMENTS.md`, source and saved experiment configurations at commit `7fa80cef7e53e79846a2a1714ce08626ff65c4b4`.

| CO5085 work | Dataset and experiment | CO5177 match | Action |
| --- | --- | --- | --- |
| A1 | All 60,000 CIFAR-100 images, 100 fine classes; ResNet18 and Swin-T with scratch, head-only, partial and full fine-tuning | Image: at least 5,000 images, at least 3 classes, pretrained when using deep learning | Reuse six pretrained configurations across three seeds as the main comparison; retain two scratch configurations as context. |
| E1 | Fashion-MNIST; softmax, MLP and CNN | Image excludes Fashion-MNIST as its main dataset | Do not transfer these scores into the main Image study. |
| E2 | Fashion-MNIST; attention over rows, patches and CNN features | Image illustration only; these sequences are image features | No additional CO5177 result transferred. |
| E3 | Fashion-MNIST; LSTM/GRU over image rows or patches, including initialization/regularization extensions | Text requires at least 2,000 actual text samples | Do not label the image-sequence runs as Text results. |
| A2 | Paper has not been selected; no implementation or measurements | No completed study to compare | No transfer. |

CO5085 has no tabular experiment with at least 2,000 records, 10 columns, numerical/categorical features and missing values. Prediction CSVs and training logs are evaluation artifacts, not a substitute for that dataset. Tabular has a new UCI Adult study. Main Text reuses the full PhoBERT news-classification notebook and matching model metadata from the separate application repository; see [TEXT_REUSE.md](TEXT_REUSE.md). A newer headline-only baseline remains documented in [STUDIES_PROTOCOL.md](STUDIES_PROTOCOL.md). Shared metrics or plotting functions can be adapted when those studies have concrete inputs; unused training modules have not been copied into placeholder tracks.

## Transferred Image material

| Material | CO5085 source at the measured release | CO5177 location |
| --- | --- | --- |
| Data transforms, split, models, metrics, training loop and runner | `A1/{data,models,metrics,engine,protocol,run_suite,visuals}.py`, `common/runtime.py` | [`src/image/`](../src/image/) |
| Eight configurations and seeds 42/43/44 | `configs/a1_experiments.json` | [`configs/image.json`](../configs/image.json), byte-identical |
| 24 histories, metadata, splits, test predictions and evaluations | `A1/reports/generated/evidence/` | [`reports/image/generated/evidence/`](../reports/image/generated/evidence/) |
| Summary, tables and measured figures | `A1/reports/generated/` | [`reports/image/generated/`](../reports/image/generated/) |
| All six pretrained learning curves, added in this review | `A1/reports/generated/figures/*_{head,partial,full}_curves.png` | `reports/image/generated/figures/`; SHA256 and original paths in `additional_figure_sources` |
| Freeze, augmentation, checkpoint and resume checks | A1 tests | [`tests/test_training_contract.py`](../tests/test_training_contract.py) |

The measured release is [`1250e56`](https://github.com/dathuynh1108/CO5085-deep-learning/tree/1250e569c6ce055391b5670e2f9a31faedb44b20). Original paths precede the later CO5085 move into `src/` and `reports/assignment1/`. The authoritative full commit is recorded in the [reuse manifest](../reports/image/reuse-manifest.json).

The manifest verifies **186 imported artifacts** and nine ported Python modules. Existing evidence bytes and signatures are preserved. Import and path changes give the ported training code a new source identity; it cannot resume the original checkpoints. The [analysis notebook](../notebooks/image.ipynb) and [Image report](../reports/image/report.tex) add dataset exploration, pixel-overlap analysis and discussion for CO5177. They do not count as additional training runs.

## Results and limits

| Architecture | Head-only accuracy | Partial accuracy | Full accuracy |
| --- | --- | --- | --- |
| ResNet18 | 60.95 ± 0.29% | 73.96 ± 0.12% | 78.97 ± 0.04% |
| Swin-T | 71.67 ± 0.09% | 78.25 ± 0.22% | 86.63 ± 0.22% |

Values are test accuracy, mean ± sample SD over three seeds, with 20 epochs and 96×96 input. Full Swin-T uses 2.81 times the training time and 4.70 times the peak allocated memory of full ResNet18 under this protocol.

The original images are 32×32; 96×96 input remains below the recommended 128px short edge. The full-data audit found two exact image contents shared between train and validation and ten between train and test. The report includes sensitivity on 9,990 retained test predictions. This does not remove the train/validation overlap or measure near duplicates. The original split, checkpoint selection and measurements remain fixed. See [IMAGE_REUSE.md](IMAGE_REUSE.md) for data provenance, commands and limitations.

## Remaining deliverables

- **Image:** the notebook reruns data inspection and prediction analysis on CPU; training is a separate explicit command. This review did not verify a fresh Google Colab session or rerun GPU training. The presentation video is pending.
- **Tabular and Text:** separate notebooks/reports are available; videos are pending. Main Text reuses the supplied Kaggle PhoBERT run; Tabular and the headline-only Text baseline are new local measurements. These measurements do not come from CO5085.
- **Course submission:** registered group name, confirmed member contributions and the consolidated LMS PDF still need the corresponding project information and presentation materials.
