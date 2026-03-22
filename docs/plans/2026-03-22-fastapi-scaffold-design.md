# FastAPI Project Scaffold Design

**Date:** 2026-03-22
**Status:** Approved

## Goal

Initialize yes-person as a FastAPI project with uv, Makefile-based workflow, and pytest + syrupy snapshot testing.

## Decisions

- **Python 3.13**, managed by uv
- **FastAPI CLI** (`fastapi dev`) as the dev server runner
- **Flat module structure** (`app/` at repo root, not `src/` layout)
- **pytest + syrupy** for snapshot testing, **httpx** for test client
- **ruff** for linting and formatting
- **Makefile** for short command workflow

## Project Structure

```
app/
  __init__.py
  main.py              # FastAPI instance, health route, router mounting
  routers/
    __init__.py        # empty, ready for future route modules
  models/
    __init__.py        # empty, ready for future Pydantic models
tests/
  __snapshots__/       # syrupy snapshot files (auto-generated)
  conftest.py          # shared fixtures (TestClient)
  test_health.py       # snapshot test for GET /health
pyproject.toml         # Python 3.13, fastapi[standard], dev deps
Makefile               # workflow shortcuts
```

## Dependencies

**Runtime:**
- `fastapi[standard]`

**Dev:**
- `pytest`
- `syrupy`
- `httpx` (TestClient)
- `ruff`

## Makefile Targets

| Target | Command | Purpose |
|--------|---------|---------|
| `dev` | `uv run fastapi dev app/main.py` | Start dev server with reload |
| `test` | `uv run pytest` | Run all tests |
| `test-update` | `uv run pytest --snapshot-update` | Update syrupy snapshots |
| `lint` | `uv run ruff check .` | Lint check |
| `format` | `uv run ruff format .` | Auto-format |
| `install` | `uv sync` | Install/sync dependencies |

## Testing Pattern

- `httpx.TestClient` wraps the FastAPI app for synchronous test requests
- syrupy captures JSON response bodies as snapshots
- `conftest.py` provides a shared `client` fixture
- Initial test: `GET /health` returns `{"status": "ok"}`, verified via snapshot

## Health Route

```
GET /health -> {"status": "ok"}
```

Serves as proof that the scaffold works end-to-end (server, tests, snapshots).
