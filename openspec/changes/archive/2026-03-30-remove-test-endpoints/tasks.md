## 1. Clean Up Files

- [x] 1.1 Delete `app/routers/dcapi_pickpost.py`
- [x] 1.2 Delete `app/models/dcapi_pickpost.py`
- [x] 1.3 Delete `app/stubs/dcapi_pickpost.json`
- [x] 1.4 Delete `specs/dcapi-pickpost/pickpost.yaml` and the directory
- [x] 1.5 Delete `tests/test_pickpost_routes.py`

## 2. Server Integration

- [x] 2.1 Remove `dcapi_pickpost_router` import and registration from `app/main.py`

## 3. Validation

- [x] 3.1 Run `make test-update` to remove old snapshot files.
- [x] 3.2 Run `make test` to ensure all tests pass.
