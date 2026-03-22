# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

**yes-person** is a mock API server built with FastAPI. Given an OpenAPI (or similar) spec, it replicates the described API's behavior with placeholder/stub responses. The goal is to provide a working API surface for integration testing against live systems before real backends are available.

## Tech Stack

- **Python 3.13+** with **FastAPI**, managed by **uv**
- **OpenSpec** workflow for planning and implementing changes (see `openspec/` and `.claude/skills/`)

## Development Commands

All workflow commands are in the `Makefile`. Run `make <target>`:

| Target | Purpose |
|--------|---------|
| `make install` | Install/sync dependencies |
| `make dev` | Start dev server with reload |
| `make test` | Run all tests |
| `make test-update` | Update syrupy snapshots |
| `make lint` | Lint with ruff |
| `make format` | Auto-format with ruff |

To run a single test: `uv run pytest tests/test_foo.py::test_name -v`

## Architecture

- **`app/main.py`** — FastAPI app entry point, mounts routers
- **`app/routers/`** — Route modules generated from OpenAPI spec sections
- **`app/models/`** — Pydantic models matching the OpenAPI schemas
- **`app/stubs/`** — Placeholder response data (JSON fixtures or factory functions)
- **`specs/`** — Source OpenAPI/spec files that define the target API surface
- **`tests/`** — Pytest tests validating routes match the spec contract

## Testing Strategy

Tests use **pytest** with **syrupy** for snapshot testing and **starlette.testclient.TestClient** for HTTP requests.

### How it works

1. `tests/conftest.py` provides a shared `client` fixture wrapping the FastAPI app
2. Tests make requests via `client` and assert `response.json() == snapshot`
3. Syrupy captures response bodies as snapshots in `tests/__snapshots__/`

### Writing a new test

```python
def test_my_endpoint(client, snapshot):
    response = client.get("/my-endpoint")

    assert response.status_code == 200
    assert response.json() == snapshot
```

Then run `make test` — it will fail with a missing snapshot. Run `make test-update` to generate the snapshot, then `make test` again to confirm it passes.

### When snapshots break

If a test fails because the response changed intentionally, run `make test-update` to accept the new snapshot. Review the diff in `tests/__snapshots__/` before committing.

## Key Design Decisions

- Routes and models are derived from OpenAPI specs — the spec is the source of truth
- All responses are placeholder/stub data, not live — the purpose is integration scaffolding
- When adding a new spec, generate corresponding routers, models, and stub responses
- Use `uv` as the package manager (not pip or poetry)
