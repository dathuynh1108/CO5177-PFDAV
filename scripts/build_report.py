"""Compile a coursework report from its LaTeX and measured evidence."""

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--track", choices=["image", "tabular", "text"], default="image"
    )
    options = parser.parse_args()
    engine = shutil.which("tectonic")
    if engine is None:
        raise SystemExit("Install Tectonic to compile the coursework reports")
    directory = ROOT / "reports" / options.track
    subprocess.run([engine, "--keep-logs", "report.tex"], cwd=directory, check=True)
    (directory / "report.pdf").replace(directory / f"{options.track}.pdf")
    print(directory / f"{options.track}.pdf")
