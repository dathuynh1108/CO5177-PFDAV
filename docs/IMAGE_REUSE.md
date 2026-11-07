# Image: current execution and archived A1 evidence

## Current CO5177 study

The [Image notebook](../notebooks/image.ipynb) completes 18 training runs on RTX 5090 GPUs: ResNet18 and Swin-T, each with head-only, partial, and full fine-tuning across seeds 42–44. Every run completes 20 epochs. Checkpoints are selected by validation accuracy, with validation cross-entropy breaking ties; test evaluation follows training and selection.

Exact RGB-pixel deduplication after stratification leaves 44,976 training, 5,000 validation, and 9,998 test images across all 100 CIFAR-100 classes. The current [summary](../reports/image/notebook-evidence/summary.json) records three-seed mean test accuracy of 79.16% for ResNet18 full and 86.81% for Swin-T full. The [execution receipt](../reports/image/notebook-evidence/execution-receipt.json) verifies 21 executed code cells, six PNG outputs, zero errors, 18 checkpoint fingerprints, and 179,964 test predictions.

Original images are 32×32 and are resized to 96×96. This remains below the assignment's recommended 128px short edge and does not create additional source detail. The [report](../reports/image/image.pdf) explains the setting and measured comparison. A fresh Google Colab Run all has not been independently verified.

## Archived CO5085 A1 experiment

The archive comes from CO5085 commit `1250e569c6ce055391b5670e2f9a31faedb44b20`. Its 24 runs are historical measurements. `reports/image/reuse-manifest.json` records source/config hashes, ported-code mappings, and SHA256 identities for imported evidence. Original bytes and signatures remain separate from `reports/image/notebook-evidence/`.

| A1 material | Location |
| --- | --- |
| Ported data, model, training and analysis code | `src/image/` |
| Original byte-identical configuration | `configs/image.json` |
| Original histories, metadata and predictions | `reports/image/generated/evidence/` |
| Original figures and result tables | `reports/image/generated/` |
| 186 imported artifacts, nine modules, additional learning curves | `reports/image/reuse-manifest.json` |

According to information supplied by Huỳnh Thành Đạt on 19 October 2026, the instructor permits equivalent reuse. [COURSE_REUSE.md](COURSE_REUSE.md) records the original comparison. Fashion-MNIST experiments from E1–E3 are not used as the main Image study.

## Archive audit and limitations

```bash
.venv/bin/python -m image.analysis
.venv/bin/python -m image.run_suite --list
```

`image.analysis` verifies imported hashes and recomputes the archived 24-run metrics. These commands do not execute the current notebook's 18 training runs. Original source identities and checkpoints are preserved; the ported code must not resume CO5085 checkpoints using a changed source identity.

The archived 45,000/5,000/10,000 split has two exact pixel contents shared between train/validation and ten between train/test. The old analysis on 9,990 retained test predictions does not repair train/validation overlap. These limitations belong to the archive; current results come from the separately deduplicated notebook execution.

Raw images and weights remain outside Git. [IMAGE_VERIFICATION.json](IMAGE_VERIFICATION.json) records checks for its stated snapshot, while the current notebook receipt records the new execution. Presentation video fields remain blank by user choice. GroupLink, LMS submission, and fresh Colab execution remain unverified in the [submission checklist](SUBMISSION_REVIEW.md).
