.PHONY: dev test test-update lint format install

dev:
	uv run fastapi dev app/main.py

test:
	uv run pytest

test-update:
	uv run pytest --snapshot-update

lint:
	uv run ruff check .

format:
	uv run ruff format .

install:
	uv sync
