.PHONY: all check lint format typecheck test clean

# Default target
all: check

# Run all checks (lint, format, typecheck)
check: lint format typecheck

# Run linter
lint:
	uvx ruff check --extend-select I .

# Run formatter
format:
	uvx ruff format .

# Run type checker
typecheck:
	uvx mypy . --namespace-packages --explicit-package-bases

# Run tests
test:
	uv run pytest

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete