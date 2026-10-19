/* Public website settings. Use HTTPS URLs or project-relative file paths.
   Leave unavailable resources empty. Never store credentials here. */
window.PFDAV = {
  groupName: '', // Set this to the name registered on GroupRegistration.
  members: {
    '2570161': { role: '', github: 'https://github.com/dathuynh1108' },
    '2570083': { role: '', github: '' }
  },
  assignments: {
    tabular: { dataset: "UCI Adult · 48,842 source rows · 14 features", description: "48,780 records remain after removing conflicting labels and repeated feature rows. A new stratified 70/15/15 split is used; this is not the original official test split.", datasetUrl: 'https://archive.ics.uci.edu/dataset/2/adult', notebook: 'https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/tabular.ipynb', report: 'reports/tabular/tabular.pdf', video: '' },
    text: { dataset: "VietnamNet · 212,705 source articles · 19 categories", description: "A fixed cohort of 7,600 headlines is selected after a full-corpus quality audit. Each category contributes 280 training, 60 validation and 60 test headlines.", datasetUrl: 'https://huggingface.co/datasets/dathuynh1108/vietnamnet-news', notebook: 'https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text.ipynb', report: 'reports/text/text.pdf', video: '' },
    image: { dataset: 'CIFAR-100 · 60,000 RGB images · 100 fine classes', description: 'Fixed 45,000 / 5,000 / 10,000 split. Original 32×32 images, measured input 96×96. The CO5085 A1 experiments are reused with a separate data audit and Image report.', datasetUrl: 'https://www.cs.toronto.edu/~kriz/cifar.html', notebook: 'https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb', report: 'reports/image/image.pdf', video: '' }
  }
};
