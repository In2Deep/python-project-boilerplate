# Agent Governance Rules (Hardened v3.1)

This document is the single source of truth for agent behavior. Its goal is to enforce a professional engineering workflow, producing code that is robust, modern, and maintainable.

## 1. VERSION TARGETING — "WRITTEN FOR" PYTHON 3.13.7
When this rule is in use, ouput "Rule 1 in use"
This codebase must feel like it was born in 2025, not ported to it.
- **MUST** use modern constructs native to Python 3.13+ (including JIT compilation).
- **Typing**: Use built-ins (list[int], dict[str, Any], X | None).
- **Type Aliases**: Use the type statement (e.g., type UserID = int).
- **Data Classes**: Use dataclasses with slots=True.
- **Imports**: A module's docstring MUST be the first statement in the file. The from __future__ import annotations statement MUST immediately follow the docstring, before any other code or imports
- **Filesystem**: Use pathlib.Path, not os.path. Use tomllib for reading .toml files.
- **Control Flow**: Use structural pattern matching (match/case) when it genuinely improves clarity over if/elif chains.
- **MUST** include a "Py313 Notes:" line in the module docstring of any new module, explaining at least one design choice that leverages modern Python.
- **HARD BANS** (Forbidden unless explicitly justified in the module docstring):
  - Legacy typing imports (from typing import List, Dict, Optional, Tuple, Set).
  - typing.TypeAlias (use the type keyword).
  - os.path (use pathlib).



## 2. KNOWLEDGE GRAPH (SINGLE SOURCE OF TRUTH)
When this rule is in use, ouput "Rule 2 in use"
**Knowledge Graph needs to be updated after every change with the status and what has been done.**
**Imports**: A module's docstring MUST be the first statement in the file. The from __future__ import annotations statement MUST immediately follow the docstring, before any other code or imports
The agent must treat the docs/ directory as its authoritative instruction set.
- **Structure**: ${workspaceFolder}/docs/project_structure.md
- **Tasks**: ${workspaceFolder}/docs/tasks.md
- **MUST** use a file/directory if and only if it is defined in project_structure.md.
- If a needed file/directory is NOT defined, **MUST STOP** and request explicit user approval. Do not create ad-hoc files.
- If a task requires adding new files, the updates to project_structure.md that authorize them **MUST** be in the same commit.

## 3. TESTING QUALITY (NO CHEATING)
When this rule is in use, ouput "Rule 3 in use"
**Knowledge Graph needs to be updated after every change with the status and what has been done.**
Tests must be robust, isolated, and reproducible. A green test suite must be a strong guarantee of correctness.
- **Unit Tests**: **MUST** be fully isolated. No external state, network, or filesystem access (use tmp_path, monkeypatch, and mocks).
- **Integration/E2E Tests**: Allowed to hit external services only when run with a specific e2e marker. The default pytest run must remain offline.
- Every function added or significantly changed **MUST** have new or updated tests covering both a success case and at least one failure case (pytest.raises).
- **Test Coverage**: Code changes must be accompanied by tests that maintain or increase project test coverage. This prevents adding untested logic.
- **Mandatory Coverage Enforcement**: All test runs must include coverage gates:
  - `pytest --cov --cov-fail-under=100` must be executed at least once in the workflow.
  - The suite **MUST** fail immediately if coverage drops below 100%.
- **Full Suite Re-run**: After quality gates and module-level tests complete, the entire test suite must be re-run to confirm no regressions in previously passing tests.
- **Workflow Guarantee**: The agent is not permitted to skip or bypass tests. Passing means *all tests pass together with enforced coverage*, not just a subset.
- **No Untested Code Creation**: The agent is strictly forbidden from creating new code until *all existing code is fully tested* and passing, except when using the explicit escape hatch for online API connections or other narrowly defined exceptions.



## 4. TASK & COMMIT WORKFLOW (VS CODE TASKS ONLY)
When this rule is in use, ouput "Rule 4 in use"
**Knowledge Graph needs to be updated after every change with the status and what has been done.**
**Imports**: A module's docstring MUST be the first statement in the file. The from __future__ import annotations statement MUST immediately follow the docstring, before any other code or imports
All work must follow this prescribed, automated workflow.
- **Select Task**: Choose the topmost unchecked task from tasks.md.
- **Verify Environment**: Ensure the agent is inside ${workspaceFolder}/3137_venv and python3 --version contains 3.13.7. If not, STOP.
- **Code & Test**: Implement the feature. All code changes **MUST** be accompanied by high-quality tests as defined in Rule 3.
- **Local Quality Gates** (Order is critical): Run these commands and resolve any issues. STOP on the first failure and report which gate failed.
  - ruff check . --fix
  - ruff format .
  - mypy .
  - pytest
  - pytest --cov (Fail if test coverage decreases).
- **Commit** (Via authorized VS Code tasks only):
  - The commit message **MUST** include a valid task ID (e.g., T5, TX1).
  - Code changes require corresponding test changes, unless the commit message contains the explicit escape hatch: NO-TEST: <short reason>.
  - Updates to tasks.md (checking the box, adding a summary) **MUST** be included in the same commit as the associated code change.

## 5. IMMEDIATE STOP CONDITIONS
When this rule is in use, ouput "Rule 5 in use"
Drop everything and report if any of the following occur:
- python3 is not 3.13.7.
- Not operating inside the 3137_venv virtual environment.
- A required command is missing from .vscode/tasks.json.
- A target file/directory is not defined in project_structure.md (and no user approval has been given).
- Any local quality gate from Rule 4 fails.
- The NO-TEST escape hatch is used without a reason.

## 6. DEBUGGING & TROUBLESHOOTING HEURISTICS
When this rule is in use, ouput "Rule 6 in use"
When a quality gate or command fails repeatedly with the same error, the agent is likely stuck in a logic loop. It MUST STOP its current approach and re-evaluate using the following steps.

- **Pre-Commit Loop Detection**: If a `git commit` fails due to a `pre-commit` hook, the agent MUST NOT simply re-run the commit. It must explicitly perform the following recovery sequence:
    1.  **Verify File is Saved**: Ensure the file mentioned in the error message is saved with the intended fixes.
    2.  **Stage the Correction**: Run `git add <file_that_failed>` to update Git's **Staging Area**. This is the most critical step. The `pre-commit` hook runs against the staged version of the file, not the saved version in the editor.
    3.  **Re-Commit**: Attempt the `git commit` command again *only after* the corrected file has been staged.

- **General Loop Prevention**: If any command or action fails twice in a row with the identical error message, the agent MUST state the problem, list the last 3 actions it took, and ask for user guidance before proceeding. This prevents wasting time on repetitive, non-productive cycles.
