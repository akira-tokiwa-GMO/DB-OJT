# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Japanese new graduate training project focused on **PostgreSQL, Transaction Control, Clean Architecture, and GitHub CI/CD**. The project involves building a simple "Task Management API" with a 4-layer Clean Architecture implementation: domain ↔ usecase ↔ interface ↔ infrastructure.

## Development Commands

Based on the README.md, the following commands are expected to be available:

```bash
# Setup and Python environment
uv sync                       # Setup Python virtual environment and dependencies
docker compose up -d          # Start development containers
uv run alembic upgrade head   # Run database migrations

# Code quality checks
uv run ruff check .           # Run linter
uv run ruff format .          # Run formatter
uv run ruff format --check .  # Check formatting without modifying files

# Testing
uv run pytest --cov=src tests/unit/  # Run unit tests with coverage
uv run pytest tests/integration/     # Run integration tests with DB containers
uv run pytest --cov=src              # Run complete test suite
make test                             # Alternative: run tests via Make
make integration                      # Alternative: run integration tests via Make
make ci                               # Alternative: run complete CI pipeline

# Running the application
uv run uvicorn src.interface.api.main:app --reload --host 0.0.0.0 --port 8080
make run                     # Alternative: Start API server (localhost:8080)
make docs                    # Generate and start Swagger UI at http://localhost:8080/docs
```

## Architecture Structure

The codebase follows Clean Architecture with this expected structure:

```
src/
├── domain/        # Entities, value objects, repository interfaces
├── usecase/       # Use cases & ports  
├── interface/     # FastAPI handlers, REST API, Presenters
└── infrastructure/# SQLAlchemy, external APIs, Logger, Alembic Migration
```

## Technology Stack

- **Language**: Python 3.12+
- **Package Manager**: uv (fast Python package installer and resolver)
- **Linter/Formatter**: Ruff (extremely fast Python linter and code formatter)
- **Web Framework**: FastAPI
- **Database**: PostgreSQL 16.x (runs in Docker containers)
- **ORM**: SQLAlchemy 2.x
- **Migration Tool**: Alembic
- **Testing Framework**: pytest + pytest-cov for coverage
- **Mocking**: unittest.mock
- **Target Coverage**: 80%+

## Key Implementation Patterns

### Transaction Management
- Repository methods should accept SQLAlchemy `Session` parameter
- UseCase layer controls transactions holistically using `session.begin()`
- Include tests for exception scenarios → rollback verification
- Use SQLAlchemy's context managers for proper transaction handling

### Testing Strategy
- **Unit Tests**: Use pytest + unittest.mock to mock dependencies, test business logic
- **Integration Tests**: Use docker-compose with real PostgreSQL, pytest fixtures
- **E2E Tests**: Full FastAPI REST API flow validation with TestClient

### Database Setup
- PostgreSQL runs in containers via `docker compose`
- Connection settings in `src/infrastructure/database`
- SQLAlchemy models and engine configuration
- Migration scripts managed by Alembic in `alembic/` directory

## Learning Objectives
1. PostgreSQL basics (DDL/DML, indexes, transaction isolation)
2. Transaction control and rollback/recovery procedures  
3. GitHub Flow & CI/CD with Pull Requests
4. Testing techniques with repository mocking and use case testing
5. Clean Architecture 4-layer structure with dependency inversion

## Development Notes
- Implement incrementally by layer (domain → usecase → interface → infrastructure)
- Focus on explicit interfaces over large implementations
- CI pipeline includes: Ruff Lint → Ruff Format Check → UnitTest → IntegrationTest
- Use Ruff for consistent code formatting and linting
- Main branch is protected; all changes via Pull Requests
- Always run `uv run ruff check .` and `uv run ruff format .` before committing