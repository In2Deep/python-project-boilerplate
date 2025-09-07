# Simple developer workflow

.PHONY: setup lint fmt typecheck test precommit hooks install

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip pre-commit ruff pytest mypy
	pre-commit install

lint:
	ruff check .

fmt:
	ruff format .

typecheck:
	mypy .

test:
	pytest

precommit:
	pre-commit run --all-files
