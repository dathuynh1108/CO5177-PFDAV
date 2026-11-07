# CO5177 · PFDAV

Coursework for **Programming Foundations for Data Analysis and Visualization**, semester 261, Ho Chi Minh City University of Technology, VNU-HCM.

**Team CTG:** Huỳnh Thành Đạt (2570161) and Lương Minh Duy (2570083).

[Course website](https://dathuynh1108.github.io/CO5177-PFDAV/) · [Assignment brief](assignments/assignment-vne-v4.pdf) · [Combined report](reports/overview/CTG-report.pdf)

| Study | Notebook | Report |
| --- | --- | --- |
| Tabular · UCI Adult | [Notebook](notebooks/tabular.ipynb) · [Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/tabular.ipynb) | [PDF](reports/tabular/tabular.pdf) |
| Text · VietnamNet News | [Notebook](notebooks/text.ipynb) · [Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/text.ipynb) | [PDF](reports/text/text.pdf) |
| Image · CIFAR-100 | [Notebook](notebooks/image.ipynb) · [Colab](https://colab.research.google.com/github/dathuynh1108/CO5177-PFDAV/blob/main/notebooks/image.ipynb) | [PDF](reports/image/image.pdf) |

The notebooks contain the experiments and outputs. Reports are written in Vietnamese; the website and notebooks use English. Supporting Python code, configurations and dependencies are included in `src/`, `configs/` and the requirements files. See [AI use disclosure](AI_USE_REPORT.md).

To serve the website locally:

```bash
python3 -m http.server 8000
```

Open [localhost:8000](http://localhost:8000). The static website requires no build step.
