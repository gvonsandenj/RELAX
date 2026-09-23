#!/usr/bin/env python3
"""Clear all cell outputs and execution counts from Jupyter notebooks in the repo.

Run this before pushing to keep diffs clean and avoid committing large/stale
notebook outputs. No third-party dependencies required (pure stdlib).

Usage:
    python3 scripts/clear_notebook_outputs.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IGNORED_DIRS = {".git", ".ipynb_checkpoints", "node_modules", "venv", ".venv"}


def find_notebooks(root: Path):
    for path in root.rglob("*.ipynb"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        yield path


def clear_outputs(notebook_path: Path) -> bool:
    """Clear outputs/execution_count in-place. Returns True if modified."""
    original_text = notebook_path.read_text(encoding="utf-8")
    notebook = json.loads(original_text)

    changed = False
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs"):
            cell["outputs"] = []
            changed = True
        if cell.get("execution_count") is not None:
            cell["execution_count"] = None
            changed = True
        metadata = cell.get("metadata", {})
        if metadata.pop("execution", None) is not None:
            changed = True

    if not changed:
        return False

    new_text = json.dumps(notebook, indent=1, ensure_ascii=False) + "\n"
    notebook_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    notebooks = sorted(find_notebooks(REPO_ROOT))
    if not notebooks:
        print("No notebooks found.")
        return 0

    modified = 0
    for path in notebooks:
        rel = path.relative_to(REPO_ROOT)
        if clear_outputs(path):
            print(f"Cleared outputs: {rel}")
            modified += 1
        else:
            print(f"Already clean:   {rel}")

    print(f"\nDone. {modified}/{len(notebooks)} notebook(s) updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
