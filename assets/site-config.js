/* Public website settings. Use HTTPS URLs or project-relative file paths.
   Leave unavailable resources empty. Never store credentials here. */
window.PFDAV = {
  groupName: '', // Set this to the name registered on GroupRegistration.
  members: {
    '2570161': { role: '', github: 'https://github.com/dathuynh1108' },
    '2570083': { role: '', github: '' }
  },
  assignments: {
    tabular: { dataset: '', description: '', datasetUrl: '', notebook: '', report: '', video: '' },
    text: { dataset: '', description: '', datasetUrl: '', notebook: '', report: '', video: '' },
    image: { dataset: 'CIFAR-100 · 60,000 RGB images · 100 fine classes', description: 'Fixed 45,000 / 5,000 / 10,000 split. Original 32×32 images, measured input 96×96. The CO5085 A1 experiments are reused with a separate data audit and Image report.', datasetUrl: 'https://www.cs.toronto.edu/~kriz/cifar.html', notebook: 'https://github.com/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb', report: 'reports/image/image.pdf', video: '' }
  }
};
