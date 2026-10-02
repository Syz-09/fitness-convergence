from pathlib import Path
import shutil
import subprocess
from .config import RAW, SOURCE_REPO


def download_dataset(force=False):
    """Clone the public dataset repository and return discovered CSV files."""
    target = RAW / "source_repo"
    if force and target.exists():
        shutil.rmtree(target)
    if not target.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", SOURCE_REPO, str(target)],
            check=True,
        )
    csvs = sorted(target.rglob("*.csv"))
    if not csvs:
        raise FileNotFoundError("Dataset repository was cloned, but no CSV files were found.")
    return csvs


if __name__ == "__main__":
    for p in download_dataset():
        print(p)
