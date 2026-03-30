## 1. App Infrastructure

- [x] 1.1 Create `app/stubs/` directory with `__init__.py` containing a `load_stubs(server_name: str)` utility that reads and caches `app/stubs/{server_name}.json`
- [x] 1.2 Create `specs/` directory at project root with a `.gitkeep`

## 2. Skill Definition

- [x] 2.1 Create the `ingest-api-doc` skill `SKILL.md` in `.claude/skills/ingest-api-doc/` with the full prompt for: parsing input docs, generating routers/models/stubs, modifying `main.py`
- [x] 2.2 Mirror the skill to `.opencode/skills/ingest-api-doc/`
- [x] 2.3 Create slash command `.claude/commands/ingest.md` that invokes the skill
- [x] 2.4 Create slash command `.opencode/command/ingest.md` that invokes the skill

## 3. Skill Prompt Content

- [x] 3.1 Define doc parsing instructions: extract endpoints (path, method, request/response schemas) from OpenAPI 3.x, Swagger 2.x, or plain text/Markdown
- [x] 3.2 Define router generation template: `APIRouter(prefix="/{version}/{server_name}")`, one handler per endpoint, handler loads and returns stub data
- [x] 3.3 Define model generation template: Pydantic models from response schemas with appropriate field types
- [x] 3.4 Define stub generation template: JSON file keyed by `"{METHOD} {path}"` with schema-based fake data
- [x] 3.5 Define `main.py` modification instructions: import router, add `app.include_router(...)` before catch-all route
- [x] 3.6 Define input doc storage instructions: copy source file to `specs/{server-name}/`

## 4. Validation

- [x] 4.1 Create a sample OpenAPI spec (minimal petstore) at `tests/fixtures/sample-petstore.yaml` for manual testing
- [x] 4.2 Run the skill against the sample spec, verify all files are generated correctly
- [x] 4.3 Write snapshot tests for generated endpoints (`tests/test_generated_routes.py`)
- [x] 4.4 Run `make test` and `make lint` — fix any failures

## 5. Documentation

- [x] 5.1 Update `CLAUDE.md` with conventions for generated files and the ingest skill
