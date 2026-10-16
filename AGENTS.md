# Working on CO5177 PFDAV

- Static site: root HTML and `assets/`; preserve its English UI, paper/moss palette, mobile navigation and no-JavaScript content.
- Read `docs/IMAGE_REUSE.md` before changing the Image study. Tabular/Text have no selected datasets or measured results yet.
- Image uses all CIFAR-100 images, 100 classes, split 45,000/5,000/10,000. The original 32px short edge is below the 128px recommendation; justify the 96px experimental input explicitly.
- Reused CO5085 A1 metrics are the SAME measurements, not another independent training study. Preserve `reports/image/reuse-manifest.json` and imported CSV/JSON bytes. No pretrained prohibition applies to this track; pretrained is required when using deep learning.
- Main Image comparisons are six pretrained configurations; scratch runs are context. Ported source only changes imports/layout and has new source guards; do not bypass them to resume old checkpoints.
- Notebook reruns analysis and dataset inspection; it does not silently rent/train on GPUs. Full training is an explicit separate CLI.
- Reports use neutral Vietnamese academic prose and few personal pronouns. AI disclosure in the main report is one sentence pointing to `AI_USE_REPORT.md`; keep that file accurate. Do not assign unverified contributions to a team member.
- Run `python -m pytest -q`, the Image audit, notebook validation and site-link checks after relevant edits. PDF source is `reports/image/report.tex`; compile with Tectonic and visually inspect.
