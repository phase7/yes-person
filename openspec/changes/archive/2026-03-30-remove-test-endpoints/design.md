## Context

The `dcapi-pickpost` endpoints were added solely to test the `endpoint-checker-skill`. This served its purpose, but the endpoints should not remain in the codebase to prevent bloating the API with unnecessary mocks.

## Goals / Non-Goals

**Goals:**
- Completely remove all traces of the `dcapi-pickpost` test endpoints.
- Ensure the server starts successfully without these endpoints.
- Ensure the tests continue to pass (and that the snapshot tests related to `dcapi-pickpost` are removed/updated).

**Non-Goals:**
- Do not modify or remove the actual `endpoint-checker-skill`. It should remain functional for checking any valid endpoints in the future.

## Decisions

- **Code Removal:** We will simply delete the related Python files (`app/models/dcapi_pickpost.py`, `app/routers/dcapi_pickpost.py`, `tests/test_pickpost_routes.py`), the JSON stub `app/stubs/dcapi_pickpost.json`, and the YAML file `specs/dcapi-pickpost/pickpost.yaml`.
- **Router Unregistration:** We will remove the line `app.include_router(dcapi_pickpost_router)` in `app/main.py`.

## Risks / Trade-offs

- **Risk**: Deleting tests may leave hanging snapshot files.
- **Mitigation**: We will run `make test-update` (which runs pytest with snapshot update flag) to clean up old syrupy snapshots and then confirm the test suite remains green.
