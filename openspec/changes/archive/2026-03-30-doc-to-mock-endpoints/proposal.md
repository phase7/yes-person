## Why

yes-person is designed to mock any API from its documentation, but currently has no mechanism to ingest API docs and generate mock endpoints. The only routes are `/health` and the catch-all stub. To fulfill its core purpose — providing a working API surface for integration testing — it needs a way to take an API doc (OpenAPI, structured docs, or plain text) and produce functional mock endpoints with realistic fake responses.

## What Changes

- New Claude/OpenCode skill (`ingest-api-doc`) that parses API documentation and generates FastAPI router, model, and stub files at build time
- App infrastructure for namespaced routers under `/{version}/{server-name}/` prefixes
- Explicit router registration in `app/main.py` (before catch-all)
- Schema-based fake response data generated from the doc's response schemas
- Input doc storage under `specs/{server-name}/`

## Capabilities

### New Capabilities
- `doc-to-mock`: End-to-end pipeline for ingesting API documentation (OpenAPI, structured docs, or plain text) and generating mock endpoints with namespaced routing (`/{version}/{server-name}/{path}`) and schema-based fake responses

### Modified Capabilities
_(none — existing stub-not-found behavior is unchanged; the catch-all still handles any routes not covered by generated mocks)_

## Impact

- `app/main.py` — router registration logic (include_router calls inserted before catch-all)
- `app/routers/` — generated router modules per ingested API
- `app/models/` — generated Pydantic models per ingested API
- `app/stubs/` — new directory for stub response data (JSON fixtures)
- `specs/` — new root directory for storing input API documentation
- `.claude/skills/` and `.opencode/skills/` — new `ingest-api-doc` skill
- `.claude/commands/` and `.opencode/command/` — new slash command to invoke the skill
