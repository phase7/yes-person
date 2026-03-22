## Context

yes-person is a mock API server that mirrors a real API surface with stub responses. When a client requests a path that hasn't been stubbed yet, FastAPI returns a raw `404 Not Found`. This breaks the cooperative nature of the mock — clients receive a framework error instead of a server-shaped response, and developers get no actionable hint about what to implement next.

Three approaches were considered: a custom exception handler for 404s, Starlette middleware, and a catch-all route.

## Goals / Non-Goals

**Goals:**
- All unmatched requests return `200 OK` with a consistent stub-not-found JSON payload
- Payload includes `error`, `message`, `path`, and `method` to help developers identify missing stubs
- Applies to all HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Real routes are unaffected

**Non-Goals:**
- Intercepting or modifying responses from registered routes
- Logging or metrics for unmatched requests
- Configurable response shapes per route

## Decisions

### Catch-all route over exception handler

The catch-all route (`@app.api_route("/{path:path}", methods=[...])`) is registered last in `main.py`, after all real routes. FastAPI's routing tries registered routes in order — the catch-all only matches when nothing else does.

Alternatives considered:
- **Exception handler** (`@app.exception_handler(404)`): Catches framework 404s but is invisible in routing, doesn't appear in OpenAPI docs, and doesn't intercept 405 Method Not Allowed. More "magic" than explicit.
- **Starlette middleware** (`BaseHTTPMiddleware`): Operates at the HTTP layer, requires calling `call_next` and inspecting the response — more complex, harder to reason about, and mixes HTTP-layer concerns with business logic.

The catch-all route is explicit, visible, and fits the existing router pattern. It must always be registered last — a constraint enforced by code position in `main.py`.

### Payload shape

```json
{
  "error": "stub_not_found",
  "message": "GET /api/payments is not yet implemented in yes-person",
  "path": "/api/payments",
  "method": "GET"
}
```

`path` and `method` together uniquely identify what stub is missing. The `message` provides a human-readable hint. `error` is a stable machine-readable code.

## Risks / Trade-offs

- **Route ordering** → The catch-all must always be the last registered route. If a future router is included after the catch-all in `main.py`, it will never be reached. Mitigated by placing the catch-all at the very end of `main.py` with a comment.
- **Hides method mismatches** → A `POST /health` (registered as GET only) will hit the catch-all and return a stub-not-found response rather than a 405. For a mock server this is acceptable — real behavior divergence isn't the concern.
