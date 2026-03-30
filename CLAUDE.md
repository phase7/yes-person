# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

**yes-person** is a mock API server built with FastAPI. Given an OpenAPI (or similar) spec, it replicates the described API's behavior with placeholder/stub responses. The goal is to provide a working API surface for integration testing against live systems before real backends are available.

Unmatched routes return `200 OK` with a `stub_not_found` JSON payload (path + method) instead of a 404, keeping the mock cooperative.

## Tech Stack

- **Python 3.13+** with **FastAPI**, managed by **uv**
- **OpenSpec** workflow for planning and implementing changes (see `openspec/` and `.claude/skills/`)

## Development Commands

All workflow commands are in the `Makefile` — run `make <target>` to see available targets. To run a single test: `uv run pytest tests/test_foo.py::test_name -v`

## Architecture

- **`app/main.py`** — FastAPI app entry point; mounts routers, catch-all fallback route registered last
- **`app/routers/`** — Route modules generated from OpenAPI spec sections
- **`app/models/`** — Pydantic models matching the OpenAPI schemas
- **`app/stubs/`** — Placeholder response data (JSON fixtures or factory functions)
- **`specs/`** — Source OpenAPI/spec files that define the target API surface
- **`tests/`** — Pytest tests validating routes match the spec contract

## Docker

Multi-stage Dockerfile: builder installs deps via `uv sync --no-dev --frozen`, runtime uses a lean non-root image on port 8000. `docker-compose.yml` mounts `./app` with `--reload` for local dev.

## Testing Strategy

Tests use **pytest** + **syrupy** (snapshot testing) + `starlette.testclient.TestClient`.

```python
def test_my_endpoint(client, snapshot):
    response = client.get("/my-endpoint")
    assert response.status_code == 200
    assert response.json() == snapshot
```

New tests fail until you run `make test-update` to generate the snapshot. If a snapshot breaks intentionally, re-run `make test-update` and review the diff in `tests/__snapshots__/` before committing.

## Commit Style

Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`, `test:`), one logical unit per commit, grouped by layer: tooling → dependencies → app code → tests → docs/config.

## Ingesting API Documentation

Use the `ingest-api-doc` skill (`.claude/skills/ingest-api-doc/SKILL.md`) to generate mock endpoints from an API doc:

```
/ingest specs/my-api/openapi.yaml
/ingest docs/api.md server_name=my-api version=v2
```

The skill supports OpenAPI 3.x, Swagger 2.x, and plain text/Markdown. It generates:

| File | Convention |
|------|------------|
| `specs/{server-name}/{filename}` | Original doc stored for reference |
| `app/routers/{server_name}.py` | FastAPI router with `prefix="/v{N}/{server-name}"` |
| `app/models/{server_name}.py` | Pydantic models from response schemas |
| `app/stubs/{server_name}.json` | Fake response data keyed by `"{METHOD} {path}"` |

- `server_name` in URLs/dirs is kebab-case; in Python filenames it is snake_case
- Stubs are loaded via `app.stubs.load_stubs(server_name)` — a cached JSON reader
- After generating, run `make test-update` to generate snapshots, then `make test`

## Key Design Decisions

- Routes and models are derived from OpenAPI specs — the spec is the source of truth
- All responses are placeholder/stub data, not live — the purpose is integration scaffolding
- When adding a new spec, use `/ingest` or follow the `ingest-api-doc` skill to generate routers, models, and stubs
- Use `uv` as the package manager (not pip or poetry)
- The catch-all route must always be registered last in `main.py` (after all `include_router` calls)
