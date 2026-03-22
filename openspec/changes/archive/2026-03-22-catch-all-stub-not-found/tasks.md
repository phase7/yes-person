## 1. Tests (Red)

- [x] 1.1 Create `tests/test_catch_all.py` with failing tests for GET, POST, and DELETE against unregistered paths
- [x] 1.2 Verify all 3 tests fail with `404 == 200`

## 2. Implementation (Green)

- [x] 2.1 Add catch-all route to `app/main.py` after all real routes, handling GET, POST, PUT, PATCH, DELETE
- [x] 2.2 Return `{"error": "stub_not_found", "message": "...", "path": "...", "method": "..."}` from the catch-all handler

## 3. Verification

- [x] 3.1 Run `make test-update` to generate snapshots for all 3 catch-all test cases
- [x] 3.2 Run `make test` and confirm all 4 tests pass clean
