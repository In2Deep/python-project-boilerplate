# Project Structure

This template uses a simple, conventional layout:

```
boilerplate/
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── README.md
├── mypy.ini
├── pyproject.toml
├── pytest.ini
├── ruff.toml
├── docs/
│   ├── project_structure.md
│   └── tasks.md
├── scripts/
│   └── ci/
│       ├── check_python_version.py
│       └── commit_msg_task_guard.py
├── src/
│   └── app/
│       ├── __init__.py
│       └── example.py
└── tests/
    └── test_example.py
```

- `src/app/`: Your application package.
- `tests/`: Pytest test modules.
- `scripts/ci/`: Local CI helpers used by pre-commit.
- `docs/`: Project docs and task list (IDs are enforced in commit messages).
