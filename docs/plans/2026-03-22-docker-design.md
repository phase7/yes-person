# Docker Design

**Date:** 2026-03-22
**Status:** Approved

## Goal

Add Docker support to yes-person: a production-ready image and a dev compose setup for local convenience.

## Approach

Single multi-stage `Dockerfile` + `docker-compose.yml`. One file to maintain, clean prod image, dev convenience via bind-mount and `--reload`.

## Dockerfile (multi-stage)

**Stage 1 — builder**
- Base: `python:3.13-slim`
- Install uv, copy `pyproject.toml` + `uv.lock`
- Run `uv sync --no-dev` to install prod deps only into `.venv`

**Stage 2 — runtime**
- Base: `python:3.13-slim`
- Copy `.venv` from builder (no uv in final image)
- Copy `app/` source
- Run as non-root user
- Expose port 8000
- `CMD`: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

Final image size target: ~150MB.

## docker-compose.yml

Single compose file for dev use:
- Builds from the Dockerfile
- Bind-mounts `./app` for live reload
- Overrides CMD with `--reload`
- Exposes `8000:8000`

Production deployments use `docker build` directly, not compose.

## .dockerignore

Excludes: `.venv/`, `__pycache__/`, `tests/`, `.git/`, `docs/`, `*.pyc`

## Makefile additions

- `make docker-build` → `docker build -t yes-person .`
- `make docker-up` → `docker compose up`

## What's not included

- No env var / config management (deferred)
- No test stage in Docker (tests stay local)
- No multi-service compose (stateless mock, no dependencies)
