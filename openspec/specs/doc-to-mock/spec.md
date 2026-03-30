## ADDED Requirements

### Requirement: Skill generates router from OpenAPI spec
The ingest-api-doc skill SHALL accept an OpenAPI 3.x or Swagger 2.x specification file and generate a FastAPI router module at `app/routers/{server_name}.py` with route handlers for each endpoint defined in the spec.

#### Scenario: OpenAPI 3.0 spec with multiple endpoints
- **WHEN** the skill is given an OpenAPI 3.0 YAML file describing a "pets" API with `GET /pets` and `GET /pets/{id}` endpoints
- **THEN** it generates `app/routers/pets.py` containing a route handler function for each endpoint

#### Scenario: Swagger 2.0 JSON spec
- **WHEN** the skill is given a Swagger 2.0 JSON file describing a "users" API with `POST /users` and `GET /users/{id}`
- **THEN** it generates `app/routers/users.py` with corresponding route handlers

### Requirement: Generated routes use namespaced URL prefix
Generated routers SHALL mount under the prefix `/{version}/{server_name}`, where version and server_name default to values extracted from the doc's info section but can be overridden by the user.

#### Scenario: Default prefix derived from doc metadata
- **WHEN** the skill processes a spec with `info.title: "Pet Store"` and `info.version: "1.0.0"`
- **THEN** the generated router uses prefix `/v1/pet-store`

#### Scenario: User overrides server name and version
- **WHEN** the skill is given a spec and the user specifies `server_name=animals` and `version=v2`
- **THEN** the generated router uses prefix `/v2/animals`

### Requirement: Skill generates Pydantic models from response schemas
The skill SHALL generate Pydantic model classes at `app/models/{server_name}.py` for response schemas defined in the API documentation.

#### Scenario: Spec with a defined schema
- **WHEN** the spec defines a `Pet` schema with fields `id` (integer), `name` (string), `status` (string)
- **THEN** `app/models/{server_name}.py` contains a `Pet` Pydantic model with matching fields and types

### Requirement: Skill generates schema-based stub responses
The skill SHALL generate a JSON stub file at `app/stubs/{server_name}.json` containing fake response data derived from the spec's response schemas, keyed by `"{METHOD} {path}"`.

#### Scenario: Endpoint returning a list of objects
- **WHEN** the spec defines `GET /pets` returning an array of Pet objects with fields id, name, status
- **THEN** the stub file contains an entry for `"GET /pets"` with an array of Pet objects populated with realistic placeholder values

#### Scenario: Endpoint returning a single object
- **WHEN** the spec defines `GET /pets/{id}` returning a single Pet object
- **THEN** the stub file contains an entry for `"GET /pets/{id}"` with a single Pet object populated with placeholder values

### Requirement: Skill registers router in main.py
The skill SHALL add an import and `app.include_router(...)` call to `app/main.py` for the generated router, positioned before the catch-all route.

#### Scenario: First API ingested into empty app
- **WHEN** the skill generates a router for "pets" and no other generated routers exist in main.py
- **THEN** `app/main.py` contains an import of the pets router and an `app.include_router(...)` call before the catch-all route

#### Scenario: Additional API ingested alongside existing
- **WHEN** a "users" router is generated and "pets" router is already registered
- **THEN** `app/main.py` contains import and include_router calls for both, both positioned before catch-all

### Requirement: Skill stores input documentation
The skill SHALL copy or store the input documentation file at `specs/{server_name}/` for reference.

#### Scenario: OpenAPI YAML file ingested
- **WHEN** the skill processes a file `petstore.yaml` with derived server name "pets"
- **THEN** the original file is stored at `specs/pets/petstore.yaml`

### Requirement: Skill supports plain text and Markdown documentation
The skill SHALL accept plain text or Markdown API documentation and use AI interpretation to extract endpoints, HTTP methods, and response shapes.

#### Scenario: Markdown doc describing endpoints
- **WHEN** the skill is given a Markdown file describing `POST /users` (creates a user, returns user object with id/name/email) and `GET /users/{id}` (returns a user by id)
- **THEN** it generates router, model, and stub files equivalent to processing a structured spec with those endpoints

### Requirement: Generated endpoints return stub data with HTTP 200
Each generated route handler SHALL return the corresponding stub data from the JSON fixture file with HTTP status 200.

#### Scenario: GET request to a generated endpoint
- **WHEN** a client sends `GET /v1/pet-store/pets` and that endpoint was generated from a spec
- **THEN** the server returns `200 OK` with the fake pet list data from the stub file

#### Scenario: Ungenerated path still hits catch-all
- **WHEN** a client sends `GET /v1/pet-store/unknown-path` and that path was NOT in the spec
- **THEN** the server returns `200 OK` with the `stub_not_found` payload (existing catch-all behavior)
