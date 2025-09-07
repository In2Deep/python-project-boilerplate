#!/usr/bin/env python3
"""Commit message guard enforcing presence of a valid Task ID.

Reads `docs/tasks.md` to collect allowed IDs (e.g., T1, T2, TX1, D0, etc.).
Blocks the commit if the commit message doesn't contain one of the IDs.

Py313 Notes: Uses structural pattern matching and pathlib.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ALLOWED_PREFIXES = ("T", "TX", "D", "Q")


def load_task_ids(repo_root: Path) -> set[str]:
    tasks_md = repo_root / "docs" / "tasks.md"
    if not tasks_md.exists():
        return set()

    ids: set[str] = set()
    pattern = re.compile(r"\b([A-Z]+[0-9](?:\.[0-9]+)?)\b")
    for line in tasks_md.read_text(encoding="utf-8").splitlines():
        m = pattern.search(line)
        if not m:
            continue
        candidate = m.group(1)
        if candidate.startswith(ALLOWED_PREFIXES):
            ids.add(candidate)
    return ids


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: commit_msg_task_guard.py <commit_msg_file>", file=sys.stderr)
        return 1

    commit_msg_path = Path(sys.argv[1])
    msg = commit_msg_path.read_text(encoding="utf-8")

    repo_root = Path(__file__).resolve().parents[3]
    allowed = load_task_ids(repo_root)
    if not allowed:
        # If no tasks are defined, allow the commit but print a hint.
        print("[guard] docs/tasks.md not found or empty; skipping Task ID enforcement.")
        return 0

    # Look for any allowed ID inside the message
    for task_id in sorted(allowed, key=len, reverse=True):
        if task_id in msg:
            return 0

    print(
        "[GUARD] Commit message must reference a task id from docs/tasks.md\n"
        f"[GUARD] Valid IDs: {' '.join(sorted(allowed))}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
