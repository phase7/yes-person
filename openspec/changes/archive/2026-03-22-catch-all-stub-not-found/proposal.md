## Why

yes-person is a mock API server — clients making requests against unregistered routes would receive a raw 404, which breaks the illusion of a cooperative stub server and gives no actionable feedback to developers.

## What Changes

- Any HTTP request to an unregistered path now returns `200 OK` with a JSON payload identifying the missing stub
- The payload includes `error`, `message`, `path`, and `method` fields so developers know exactly what to implement next
- Applies to all HTTP methods: GET, POST, PUT, PATCH, DELETE

## Capabilities

### New Capabilities

- `stub-not-found`: Catch-all route that intercepts unmatched requests and returns a consistent 200 response with a stub-not-found payload

### Modified Capabilities

## Impact

- `app/main.py` — new catch-all route registered last, after all real routes
- `tests/test_catch_all.py` — new test file with snapshot tests for GET, POST, DELETE against unregistered paths
