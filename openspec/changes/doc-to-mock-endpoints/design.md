## Context

yes-person is a mock API server that returns stub responses for integration testing. Currently it has only a health check and a catch-all `stub_not_found` route. The entire code-generation pipeline — from API doc to working mock endpoints — does not yet exist. The `app/routers/`, `app/models/` directories are empty, `app/stubs/` and `specs/` don't exist yet.

The user wants a Claude/OpenCode skill (build-time, not runtime) that accepts any API documentation format, generates FastAPI code following project conventions, and serves mock endpoints under `/{version}/{server-name}/{path}` with schema-based fake responses.

## Goals / Non-Goals

**Goals:**
- Support OpenAPI 3.x and Swagger 2.x as primary structured input formats
- Best-effort support for plain text/Markdown API descriptions via AI interpretation
- Generate readable, editable FastAPI router/model/stub code
- Namespaced URL pattern: `/{version}/{server-name}/{path}` with defaults from doc metadata, overridable by user
- Schema-based fake response data derived from the doc's response schemas
- Generated code passes `make lint` and `make test`

**Non-Goals:**
- Runtime dynamic route creation (no uploading docs to the running server)
- Authentication/authorization simulation
- Request body validation against schemas (mock server is cooperative — accepts anything)
- GraphQL or gRPC support
- Stateful mock behavior (e.g., POST creates an item, subsequent GET returns it)

## Decisions

### 1. Skill-based code generation over runtime dynamic routing

**Decision**: Ingestion is a Claude/OpenCode skill that generates static Python files.

**Rationale**: Static files are inspectable, editable, testable, and version-controllable. The skill approach leverages AI to handle ambiguous or non-standard doc formats that a deterministic parser could not.

**Alternatives considered**:
- Runtime ASGI middleware that parses specs on startup — rejected (no code review, harder to test, can't handle non-standard docs)
- Standalone CLI code generator — rejected (AI-powered skill handles more formats and produces higher-quality stubs)

### 2. File layout conventions

**Decision**:
```
specs/{server-name}/               # Input doc storage (original file)
app/routers/{server_name}.py       # Generated router (underscored for Python import)
app/models/{server_name}.py        # Generated Pydantic models
app/stubs/{server_name}.json       # Stub response data (JSON fixture)
```

One file per layer per server. Server name is kebab-case in URLs/directories, snake_case in Python filenames.

**Rationale**: One file per server is simple. Mock servers don't need the complexity of split modules — readability of individual endpoints matters more than file organization at scale.

**Alternatives considered**:
- Directory-per-server with split files (`app/routers/pets/users.py`, `payments.py`) — rejected as premature complexity

### 3. Router prefix pattern

**Decision**: Each generated router uses `APIRouter(prefix="/{version}/{server_name}")`. Defaults:
- `version`: major version from `info.version` (e.g., `"2.1.0"` → `"v2"`), fallback `"v1"`
- `server_name`: kebab-case of `info.title`, fallback to filename stem

Both overridable when invoking the skill.

**Rationale**: Matches the requested `base-url/v1/server-name/endpoint` pattern. Deriving defaults reduces manual input; overrides give flexibility.

### 4. Explicit router registration in main.py

**Decision**: The skill adds `app.include_router(...)` calls to `app/main.py`, inserted before the catch-all route. Each ingested API gets one import + one `include_router` call.

**Rationale**: Explicit is better than implicit. The catch-all must remain last (hard constraint from CLAUDE.md), so the skill must insert before it.

**Alternatives considered**:
- Auto-discovery via `importlib` scanning `app/routers/` — rejected (implicit, ordering fragile, harder to debug)

### 5. Stub data: JSON fixtures loaded at import time

**Decision**: Generate a JSON file per server (`app/stubs/{server_name}.json`) keyed by `"{METHOD} {path}"`. A small loader utility in `app/stubs/__init__.py` reads and caches the JSON. Router handlers return the corresponding entry.

**Rationale**: JSON fixtures are inspectable, diffable, and editable. Separating data from routing logic keeps routers clean. Cache-on-import avoids repeated file reads.

**Alternatives considered**:
- `faker` library for dynamic generation — rejected (adds dependency, non-deterministic, bad for snapshot tests)
- Inline dict literals in routers — rejected (clutters routing code)

## Risks / Trade-offs

- **[Large specs → large files]** → Acceptable for a mock server. Can split later if needed.
- **[Plain text docs may be misinterpreted by AI]** → Mitigated by: generated code is reviewable/editable, and the skill can ask clarifying questions.
- **[main.py modification could conflict with manual edits]** → Skill reads current state and inserts cleanly before catch-all. Standard pattern reduces risk.
- **[No request validation]** → By design. Mock server is cooperative — validates nothing, returns stubs for anything.

## Open Questions

- Should the skill support re-running on an updated spec (regenerate in place vs. additive)?
- Should generated routers include request body type hints (for `/docs` UI) even though we don't validate bodies?
