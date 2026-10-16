"""Compile the Image report from its committed LaTeX and measured evidence."""
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]

if __name__=='__main__':
    engine=shutil.which('tectonic')
    if engine is None:raise SystemExit('Install Tectonic to compile reports/image/report.tex')
    directory=ROOT/'reports/image'
    subprocess.run([engine,'--keep-logs','report.tex'],cwd=directory,check=True)
    (directory/'report.pdf').replace(directory/'image.pdf')
    print(directory/'image.pdf')
