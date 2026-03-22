### Requirement: Unmatched routes return 200 with stub-not-found payload
The server SHALL respond to any request whose path does not match a registered route with HTTP status 200 and a JSON payload containing `error`, `message`, `path`, and `method` fields.

#### Scenario: GET request to unregistered path
- **WHEN** a client sends `GET /api/does-not-exist`
- **THEN** the server returns `200 OK` with `{"error": "stub_not_found", "message": "GET /api/does-not-exist is not yet implemented in yes-person", "path": "/api/does-not-exist", "method": "GET"}`

#### Scenario: POST request to unregistered path
- **WHEN** a client sends `POST /api/payments/submit`
- **THEN** the server returns `200 OK` with `{"error": "stub_not_found", "message": "POST /api/payments/submit is not yet implemented in yes-person", "path": "/api/payments/submit", "method": "POST"}`

#### Scenario: DELETE request to unregistered path
- **WHEN** a client sends `DELETE /api/users/42`
- **THEN** the server returns `200 OK` with `{"error": "stub_not_found", "message": "DELETE /api/users/42 is not yet implemented in yes-person", "path": "/api/users/42", "method": "DELETE"}`

### Requirement: Registered routes are unaffected
The catch-all route SHALL NOT intercept requests that match a registered route.

#### Scenario: Registered route still responds correctly
- **WHEN** a client sends `GET /health`
- **THEN** the server returns `200 OK` with `{"status": "ok"}` (not the stub-not-found payload)
