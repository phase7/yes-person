## 1. App Infrastructure

- [ ] 1.1 Create `app/stubs/` directory with `__init__.py` containing a `load_stubs(server_name: str)` utility that reads and caches `app/stubs/{server_name}.json`
- [ ] 1.2 Create `specs/` directory at project root with a `.gitkeep`

## 2. Skill Definition

- [ ] 2.1 Create the `ingest-api-doc` skill `SKILL.md` in `.claude/skills/ingest-api-doc/` with the full prompt for: parsing input docs, generating routers/models/stubs, modifying `main.py`
- [ ] 2.2 Mirror the skill to `.opencode/skills/ingest-api-doc/`
- [ ] 2.3 Create slash command `.claude/commands/ingest.md` that invokes the skill
- [ ] 2.4 Create slash command `.opencode/command/ingest.md` that invokes the skill

## 3. Skill Prompt Content

- [ ] 3.1 Define doc parsing instructions: extract endpoints (path, method, request/response schemas) from OpenAPI 3.x, Swagger 2.x, or plain text/Markdown
- [ ] 3.2 Define router generation template: `APIRouter(prefix="/{version}/{server_name}")`, one handler per endpoint, handler loads and returns stub data
- [ ] 3.3 Define model generation template: Pydantic models from response schemas with appropriate field types
- [ ] 3.4 Define stub generation template: JSON file keyed by `"{METHOD} {path}"` with schema-based fake data
- [ ] 3.5 Define `main.py` modification instructions: import router, add `app.include_router(...)` before catch-all route
- [ ] 3.6 Define input doc storage instructions: copy source file to `specs/{server-name}/`

## 4. Validation

- [ ] 4.1 Create a sample OpenAPI spec (minimal petstore) at `tests/fixtures/sample-petstore.yaml` for manual testing
- [ ] 4.2 Run the skill against the sample spec, verify all files are generated correctly
- [ ] 4.3 Write snapshot tests for generated endpoints (`tests/test_generated_routes.py`)
- [ ] 4.4 Run `make test` and `make lint` — fix any failures

## 5. Documentation

- [ ] 5.1 Update `CLAUDE.md` with conventions for generated files and the ingest skill
