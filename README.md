# yes-person

A mock API server built with FastAPI. Given an OpenAPI spec, it replicates the described API's behavior with placeholder/stub responses — useful for integration testing before real backends are available.

## Quickstart

```bash
# Install dependencies
make install

# Start dev server (hot reload)
make dev
```

The server runs at `http://localhost:8000`. Hit `/health` to verify.

## Usage

1. Drop an OpenAPI spec into `specs/`
2. Generate routers, models, and stubs from it
3. Point your integration tests at the running server

## Commands

| Command | Purpose |
|---------|---------|
| `make dev` | Start dev server with reload |
| `make test` | Run tests |
| `make lint` | Lint |
| `make format` | Format |
| `make docker-up` | Run via Docker Compose |

## Stack

- Python 3.13, FastAPI, uv
- pytest + syrupy (snapshot testing)
