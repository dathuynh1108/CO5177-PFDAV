/* Public website settings. Use HTTPS URLs or project-relative file paths.
   Leave unavailable resources empty. Never store credentials here. */
window.PFDAV = {
  groupName: 'CTG',
  members: {
    '2570161': { role: 'Contribution · 50%', github: 'https://github.com/dathuynh1108' },
    '2570083': { role: 'Contribution · 50%', github: '' }
  },
  assignments: {
    tabular: { dataset: "UCI Adult · 48,842 source rows · 14 features", description: "After duplicate and conflicting records are removed, 48,780 records are divided into new training, validation and test partitions.", datasetUrl: 'https://archive.ics.uci.edu/dataset/2/adult', notebook: 'https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/tabular.ipynb', report: 'reports/tabular/tabular.pdf', video: '' },
    text: { dataset: "VietnamNet · 212,705 articles · 19 categories", description: "The corpus contains 180,799 training articles and 31,906 evaluation articles. Each input combines the headline with the beginning and end of the body.", datasetUrl: 'https://huggingface.co/datasets/dathuynh1108/vietnamnet-news', notebook: 'https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text.ipynb', report: 'reports/text/text.pdf', video: '' },
    image: { dataset: 'CIFAR-100 · 60,000 RGB images · 100 fine classes', description: 'The original 32×32 images were resized to 96×96. The CO5085 A1 experiment used 45,000 training, 5,000 validation and 10,000 test images.', datasetUrl: 'https://www.cs.toronto.edu/~kriz/cifar.html', notebook: 'https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb', report: 'reports/image/image.pdf', video: '' }
  }
};
