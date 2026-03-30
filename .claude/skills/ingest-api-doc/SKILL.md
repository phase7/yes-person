---
name: ingest-api-doc
description: Ingest API documentation and generate mock endpoints. Given a doc file (OpenAPI, Swagger, or plain text/Markdown), generates FastAPI router, Pydantic model, and JSON stub files under app/, then registers the router in main.py.
license: MIT
compatibility: yes-person project. Requires FastAPI app structure with app/routers/, app/models/, app/stubs/.
metadata:
  author: yes-person
  version: "1.0"
---

Ingest an API documentation file and generate working mock endpoints for the yes-person mock server.

**Input**: Path to an API documentation file (OpenAPI 3.x YAML/JSON, Swagger 2.x YAML/JSON, or plain text/Markdown). Optionally, the user may specify `server_name` and/or `version` overrides.

**Steps**

1. **Accept input**

   The user provides:
   - A file path to the API documentation (required)
   - `server_name=<name>` override (optional, kebab-case)
   - `version=<vX>` override (optional, e.g., `v1`, `v2`)

   If no file path is provided, ask:
   > "Please provide the path to your API documentation file (OpenAPI YAML/JSON, Swagger JSON, or Markdown/text)."

2. **Parse the documentation**

   Read the file and detect its format:

   **OpenAPI 3.x (YAML or JSON)**:
   - Extract `info.title` → derive `server_name` (kebab-case, e.g., "Pet Store" → "pet-store")
   - Extract `info.version` → derive `version` prefix (major only, e.g., "1.2.3" → "v1"; if no semver, use "v1")
   - Extract all paths from `paths`: each key is a path, each HTTP method under it is an endpoint
   - For each endpoint extract: method, path, operationId (or derive a function name), response schemas (200/201 response `$ref` or inline schema)
   - Extract `components/schemas` (or `definitions` for Swagger 2.x) for model generation

   **Swagger 2.x (JSON or YAML)**:
   - Same approach: `info.title`, `info.version`, `paths`, `definitions`

   **Plain text / Markdown**:
   - Use AI interpretation to identify:
     - HTTP methods and paths (e.g., `GET /users`, `POST /users/{id}`)
     - Response shapes (field names, types) described in the text
     - A logical API name (from headings or context)
   - If ambiguous, ask the user one focused clarifying question before proceeding

   **Derive final values** (applying user overrides last):
   - `server_name`: from doc metadata, then user override
   - `server_name_snake`: replace hyphens with underscores (for Python filenames, e.g., `pet_store`)
   - `version`: from doc metadata, then user override

3. **Store the input documentation**

   Copy or store the source file at:
   ```
   specs/{server_name}/{original_filename}
   ```
   Create the directory if it doesn't exist.

4. **Generate Pydantic models** (`app/models/{server_name_snake}.py`)

   For each schema in the doc's components/schemas (or definitions):
   - Create a Pydantic `BaseModel` class
   - Map OpenAPI types to Python types:
     - `string` → `str`
     - `integer` → `int`
     - `number` → `float`
     - `boolean` → `bool`
     - `array` → `list[<item_type>]`
     - `object` (inline) → `dict`
     - `$ref` → reference the corresponding model class name
   - Fields without `required` are `Optional[<type>] = None`

   **Example output** (`app/models/pet_store.py`):
   ```python
   from __future__ import annotations
   from typing import Optional
   from pydantic import BaseModel


   class Pet(BaseModel):
       id: int
       name: str
       status: Optional[str] = None


   class PetList(BaseModel):
       pets: list[Pet]
   ```

   If there are no schemas defined, create an empty models file with just the module docstring.

5. **Generate stub data** (`app/stubs/{server_name_snake}.json`)

   Create a JSON object keyed by `"{METHOD} {path}"` (uppercase method, path as-is from the spec).

   For each endpoint, generate realistic fake data based on the response schema:
   - `string` fields: use contextually appropriate placeholder (e.g., `name` → `"Fido"`, `email` → `"user@example.com"`, `id`-like → `"abc-123"`, generic → `"example"`)
   - `integer`/`number` fields: use small positive values (e.g., `id` → `1`, `count` → `42`, `price` → `9.99`)
   - `boolean` fields: `true`
   - `array` responses: include 2 example items
   - Endpoints with no defined response schema: `{"stub": true}`

   **Example** (`app/stubs/pet_store.json`):
   ```json
   {
     "GET /pets": [
       {"id": 1, "name": "Fido", "status": "available"},
       {"id": 2, "name": "Whiskers", "status": "pending"}
     ],
     "GET /pets/{petId}": {"id": 1, "name": "Fido", "status": "available"},
     "POST /pets": {"id": 3, "name": "Buddy", "status": "available"},
     "DELETE /pets/{petId}": {"deleted": true, "id": 1}
   }
   ```

6. **Generate the FastAPI router** (`app/routers/{server_name_snake}.py`)

   Structure:
   ```python
   from __future__ import annotations
   from fastapi import APIRouter
   from app.stubs import load_stubs

   router = APIRouter(prefix="/{version}/{server_name}", tags=["{server_name}"])
   _stubs = load_stubs("{server_name_snake}")


   @router.{method}("{path}")
   def {function_name}(...path_params...):
       return _stubs.get("{METHOD} {path}", {})
   ```

   Rules:
   - `prefix` uses the kebab-case `server_name` and the `version` string (e.g., `prefix="/v1/pet-store"`)
   - One handler function per endpoint
   - Function name: snake_case derived from operationId if available, otherwise `{method}_{path_snake}` (e.g., `get_pets`, `get_pets_by_pet_id`)
   - Path parameters appear as typed function args: `petId: int` for integer params, `petId: str` otherwise (derive from parameter schema if defined, default to `str`)
   - Return value: `_stubs.get("{METHOD} {path}", {})`
   - No request body validation (accept anything, return stub)

   **Example output** (`app/routers/pet_store.py`):
   ```python
   from __future__ import annotations
   from fastapi import APIRouter
   from app.stubs import load_stubs

   router = APIRouter(prefix="/v1/pet-store", tags=["pet-store"])
   _stubs = load_stubs("pet_store")


   @router.get("/pets")
   def get_pets():
       return _stubs.get("GET /pets", {})


   @router.get("/pets/{petId}")
   def get_pet_by_id(petId: int):
       return _stubs.get("GET /pets/{petId}", {})


   @router.post("/pets")
   def create_pet():
       return _stubs.get("POST /pets", {})


   @router.delete("/pets/{petId}")
   def delete_pet(petId: int):
       return _stubs.get("DELETE /pets/{petId}", {})
   ```

7. **Register the router in `app/main.py`**

   Read the current `app/main.py`. Insert before the catch-all route:
   - Import line: `from app.routers.{server_name_snake} import router as {server_name_snake}_router`
   - Registration line: `app.include_router({server_name_snake}_router)`

   The catch-all route is identified by its `@app.api_route("/{path:path}", ...)` decorator. All imports and `include_router` calls MUST appear before it.

   If the router is already registered (import already present), skip silently — do not duplicate.

   **Example result** in `app/main.py`:
   ```python
   from fastapi import FastAPI, Request
   from app.routers.pet_store import router as pet_store_router

   app = FastAPI(title="yes-person", version="0.1.0")

   app.include_router(pet_store_router)


   @app.get("/health")
   def health():
       return {"status": "ok"}


   @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
   async def catch_all(path: str, request: Request):
       ...
   ```

8. **Report what was created**

   After all files are written, summarize:
   ```
   ## Ingestion complete: {server_name}

   **Prefix:** /{version}/{server_name}
   **Endpoints:** N routes registered

   ### Files created
   - specs/{server_name}/{filename}          (original doc)
   - app/models/{server_name_snake}.py       (Pydantic models)
   - app/stubs/{server_name_snake}.json      (stub data)
   - app/routers/{server_name_snake}.py      (FastAPI router)

   ### Updated
   - app/main.py                             (router registered)

   ### Endpoints
   - GET    /{version}/{server_name}/...
   - POST   /{version}/{server_name}/...
   (list all generated routes)

   Start the server with `make dev` and test at http://localhost:8000/{version}/{server_name}/...
   ```

**Guardrails**
- ALWAYS place the catch-all route last in `main.py` — never insert after it
- If the server already has a router registered for this `server_name`, warn the user and ask before overwriting
- Keep generated code clean and passing `make lint` (ruff-compatible: type annotations, no unused imports)
- Do not add dependencies beyond what is already in `pyproject.toml`
- Path parameters in stubs use the exact string from the spec (e.g., `{petId}` not `{pet_id}`)
- Function names must be valid Python identifiers (replace `{`, `}`, `/`, `-` with `_`, strip leading/trailing `_`)
- If the doc has no response schemas at all, generate minimal stubs with `{"stub": true}` and empty models file
- For re-ingestion of an existing server: overwrite router, models, and stubs; do not add duplicate import/include_router to main.py
