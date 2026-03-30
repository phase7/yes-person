---
name: "Ingest API Doc"
description: Ingest an API documentation file and generate mock endpoints for yes-person
category: Workflow
tags: [mock, codegen, openapi, swagger]
---

Ingest an API documentation file and generate working mock endpoints.

**Input**: The argument after `/ingest` is the path to an API documentation file (OpenAPI 3.x YAML/JSON, Swagger 2.x YAML/JSON, or plain text/Markdown). Optionally append `server_name=<name>` and/or `version=<vX>` overrides.

**Examples**:
- `/ingest specs/pets/petstore.yaml`
- `/ingest docs/payments-api.md server_name=payments version=v2`

Load the `ingest-api-doc` skill and follow its steps to:
1. Parse the documentation file
2. Store the original doc under `specs/{server_name}/`
3. Generate `app/models/{server_name_snake}.py` (Pydantic models)
4. Generate `app/stubs/{server_name_snake}.json` (fake response data)
5. Generate `app/routers/{server_name_snake}.py` (FastAPI router)
6. Register the router in `app/main.py` before the catch-all route
7. Report all created files and the list of mock endpoints
