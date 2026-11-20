"""Copy a TokunizaIgbo version into another project, then check the copy.

  python copy_to.py path/to/SomeProject          # copies v1 to SomeProject/models/tokenizer/tokunizaigbo-v1/
  python copy_to.py path/to/SomeProject --version v1

Never overwrites an existing copy: delete it yourself first if you really mean to replace it.
Remember to keep the copy out of that project's git (add models/tokenizer/ to its .gitignore).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path)
    ap.add_argument("--version", default="v1")
    a = ap.parse_args()
    src = HERE / a.version
    if not (src / "tokenizer.model").exists():
        sys.exit(f"no such version: {src}")
    dst = a.project.expanduser().resolve() / "models" / "tokenizer" / f"tokunizaigbo-{a.version}"
    if dst.exists():
        sys.exit(f"already there, not overwriting: {dst}")
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    print("copied to", dst)
    sys.exit(subprocess.call([sys.executable, str(dst / "check.py")]))


if __name__ == "__main__":
    main()
