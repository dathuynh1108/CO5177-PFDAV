# Working on CO5177 PFDAV

- Static site: root HTML and `assets/`; preserve its English UI, paper/moss palette, mobile navigation and no-JavaScript content.
- Read `docs/IMAGE_REUSE.md` and `docs/COURSE_REUSE.md` before changing the Image study. Tabular/Text are new studies documented in `docs/STUDIES_PROTOCOL.md`, not reused E1–E3 experiments.
- Tabular uses all source UCI Adult records, deduplicated before a new split. Text audits all 212,705 VietnamNet articles and models a fixed 7,600-headline cohort, 19 classes. Preserve the explicit distinction between the corpus and modeling cohort.
- Text uses pinned VinAI PhoBERT as a frozen encoder with PyVi segmentation. The old user PhoBERT repository has no weights. Do not call feature extraction backbone fine-tuning or copy NER metrics into classification.
- New studies use `src/studies/`, `configs/{text,tabular}.json`, their own notebooks and `reports/{text,tabular}/`. Fit preprocessing/classifiers on train only; choose settings by validation before held-out evaluation. Keep raw data, feature caches and fitted models outside Git.
- Image uses all CIFAR-100 images, 100 classes, split 45,000/5,000/10,000. The original 32px short edge is below the 128px recommendation; justify the 96px experimental input explicitly.
- Reused CO5085 A1 metrics are the SAME measurements, not another independent training study. Preserve `reports/image/reuse-manifest.json` and imported CSV/JSON bytes. No pretrained prohibition applies to this track; pretrained is required when using deep learning.
- Main Image comparisons are six pretrained configurations; scratch runs are context. Ported source only changes imports/layout and has new source guards; do not bypass them to resume old checkpoints.
- The Image notebook reruns analysis and dataset inspection; its GPU training is a separate explicit CLI. Tabular/Text notebooks rerun their own training and evaluation. No notebook rents hardware or submits paid jobs.
- Reports use neutral Vietnamese academic prose and few personal pronouns. AI disclosure in the main report is one sentence pointing to `AI_USE_REPORT.md`; keep that file accurate. Do not assign unverified contributions to a team member.
- Run `python -m pytest -q`, `python -m studies.audit`, the Image audit, notebook validation and site-link checks after relevant edits. Install new-study dependencies from `requirements-studies.txt`. Compile each `reports/<track>/report.tex` with `scripts/build_report.py --track <track>` and visually inspect.
