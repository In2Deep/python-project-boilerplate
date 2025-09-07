# Python Project Boilerplate

A ready-to-clone template with strict quality gates and a smooth DX:

- Pre-commit hooks (Ruff lint/format, whitespace, YAML, merge conflicts)
- Ruff configuration (modern Python rules, excludes for CI helpers)
- Pytest configured
- Mypy configuration (strict-ish)
- Task-ID commit guard (enforces commit messages like `T5: message`)
- Docs: `docs/tasks.md` and `docs/project_structure.md`
- CI helper scripts under `scripts/ci/`
- VS Code tasks and Makefile

## Quick start

```
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip pre-commit ruff pytest mypy
pre-commit install
pre-commit run --all-files
```

## Commit convention (Task IDs)
- All commit messages must include a valid Task ID from `docs/tasks.md`, e.g. `T1: initial scaffold`.
- This is enforced by a `commit-msg` hook.

## Make targets
- `make setup`
- `make lint`
- `make fmt`
- `make typecheck`
- `make test`
- `make precommit`

## Structure
See `docs/project_structure.md`.
