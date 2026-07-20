#!/usr/bin/env python3
"""
Cross-platform setup helper.

Copies every .env.example file to .env (skips any that already exist).
Works on Windows, macOS, and Linux — no shell required.

Usage:
    python setup.py          # copy all .env.example → .env
    python setup.py --force  # overwrite existing .env files
"""
import argparse
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(description="Copy .env.example → .env for all challenges")
    parser.add_argument("--force", action="store_true", help="Overwrite existing .env files")
    args = parser.parse_args()

    copied = []
    skipped = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Don't descend into hidden dirs or __pycache__
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]

        if ".env.example" in filenames:
            src = os.path.join(dirpath, ".env.example")
            dst = os.path.join(dirpath, ".env")
            rel = os.path.relpath(dirpath, ROOT)

            if os.path.exists(dst) and not args.force:
                skipped.append(rel)
            else:
                shutil.copy2(src, dst)
                copied.append(rel)

    if copied:
        print("Copied .env.example → .env in:")
        for p in copied:
            print(f"  {p}")

    if skipped:
        print("\nSkipped (already exist — use --force to overwrite):")
        for p in skipped:
            print(f"  {p}")

    if not copied and not skipped:
        print("No .env.example files found.")
        sys.exit(1)

    print("\nDone. Edit each .env to set your FLAG before running docker compose.")


if __name__ == "__main__":
    main()
