.PHONY: install test format lint type-check build

install:
	uv sync --all-groups --all-extras

test: install
	uv run pytest

format:
	uv run ruff format .

lint:
	uv run ruff check .

type-check:
	uv run mypy doculingo

build:
	uv build
