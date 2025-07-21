# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## must

git branch をきって開発とテストを行い、その後 make check と make test で確認をして, ok であれば git add, commit して。ただし、commit 名は一文かつ、claude という文字は絶対に入れないで。

## Development Workflow

1. Create a git branch for development and testing
2. Run `make check` and `make test` before committing
3. Commit with a single-line message (must NOT include the word "claude")

## Common Commands

```bash
# Code quality checks
make lint       # Run ruff linter with import sorting
make format     # Auto-format code with ruff
make typecheck  # Run mypy type checking
make check      # Run all checks (lint, format, typecheck)

# Testing
make test       # Run pytest tests
uv run pytest   # Alternative way to run tests

# Cleanup
make clean      # Remove cache files (__pycache__, .mypy_cache, etc.)
```

## Architecture Overview

This is a RAG (Retrieval-Augmented Generation) backend following Clean Architecture principles:

### Layer Structure

1. **Domain Layer** (`src/domain/`)

   - Core business entities (Document, Query)
   - Repository interfaces (abstract contracts)
   - Service interfaces (RAG strategies)
   - No external dependencies

2. **Infrastructure Layer** (`src/infrastructure/`)

   - External service integrations (Azure OpenAI, Azure Cognitive Search)
   - Repository implementations
   - RAG algorithm implementations
   - Configuration management

3. **Use Case Layer** (`src/usecase/`)

   - Business logic orchestration
   - Document management (upload, delete, list)
   - RAG execution logic

4. **Presentation Layer** (`src/presentation/`)
   - FastAPI application
   - REST API endpoints
   - Request/Response schemas
   - Dependency injection

### Key Design Patterns

- **Repository Pattern**: Abstract data access through interfaces in domain layer
- **Strategy Pattern**: Different RAG implementations via `rag_strategy.py` interface
- **Dependency Injection**: Dependencies resolved in `presentation/api/dependencies.py`
- **Clean Architecture**: Dependencies flow inward (presentation → use case → domain)

## Development Guidelines

- Python 3.12+ required (see `.python-version`)
- Package manager: `uv` (not pip)
- Strict type checking enabled (mypy strict mode)
- Follow existing code style enforced by ruff
- All new code must have proper type annotations
