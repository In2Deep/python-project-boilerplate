#!/usr/bin/env python3
"""Check that the active Python is at least a configured version.

Py313 Notes: Uses sys.version_info pattern matching.
"""
from __future__ import annotations

import sys
from typing import Any

REQUIRED_MAJOR: int = 3
REQUIRED_MINOR: int = 13


def main() -> int:
    vi = sys.version_info
    match (vi.major, vi.minor):
        case (m, n) if (m, n) >= (REQUIRED_MAJOR, REQUIRED_MINOR):
            return 0
        case _:
            print(
                f"Python {REQUIRED_MAJOR}.{REQUIRED_MINOR}+ required; found {vi.major}.{vi.minor}",
                file=sys.stderr,
            )
            return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
