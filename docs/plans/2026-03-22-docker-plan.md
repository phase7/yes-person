# Docker Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a multi-stage Dockerfile, dev compose setup, .dockerignore, and Makefile targets to run yes-person in Docker.

**Architecture:** Multi-stage build — a `builder` stage installs deps via uv, a lean `runtime` stage copies only the venv and app source. `docker-compose.yml` bind-mounts `./app` and enables `--reload` for dev. Production uses `docker build` directly.

**Tech Stack:** Python 3.13-slim, uv (binary copied from `ghcr.io/astral-sh/uv:latest`), uvicorn, Docker Compose v2.

---

### Task 1: Add .dockerignore

**Files:**
- Create: `.dockerignore`

**Step 1: Create the file**

```
.venv/
__pycache__/
*.pyc
.git/
tests/
docs/
.ruff_cache/
*.egg-info/
dist/
.claude/
openspec/
mise.toml
```

**Step 2: Verify build context is clean**

Run: `docker build --no-cache -t yes-person . 2>&1 | head -5`

This will fail (no Dockerfile yet) — that's fine. We're just confirming Docker picks up the ignore file without error on the context-sending step.

**Step 3: Commit**

```bash
git add .dockerignore
git commit -m "chore: add .dockerignore"
```

---

### Task 2: Write the Dockerfile

**Files:**
- Create: `Dockerfile`

**Step 1: Create the Dockerfile**

```dockerfile
# Stage 1: builder — installs dependencies using uv
FROM python:3.13-slim AS builder

WORKDIR /app

# Copy uv binary from official image (no pip install needed)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency manifest and lock file
COPY pyproject.toml uv.lock ./

# Install production deps only into the project venv
RUN uv sync --no-dev --frozen

# Stage 2: runtime — lean image with only what's needed to run
FROM python:3.13-slim AS runtime

WORKDIR /app

# Non-root user for security
RUN useradd --create-home appuser

# Copy venv from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy app source
COPY --chown=appuser:appuser app/ /app/app/

USER appuser

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Step 2: Build the image**

Run: `docker build -t yes-person .`

Expected: Build completes successfully. Two stages visible in output. No errors.

**Step 3: Verify the container starts and serves the health endpoint**

Run: `docker run --rm -d -p 8000:8000 --name yp-test yes-person && sleep 2 && curl -s http://localhost:8000/health && docker stop yp-test`

Expected output: `{"status":"ok"}`

**Step 4: Commit**

```bash
git add Dockerfile
git commit -m "feat: add multi-stage Dockerfile"
```

---

### Task 3: Add docker-compose.yml for dev

**Files:**
- Create: `docker-compose.yml`

**Step 1: Create the file**

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Step 2: Verify dev compose starts**

Run: `docker compose up --build -d && sleep 3 && curl -s http://localhost:8000/health && docker compose down`

Expected output: `{"status":"ok"}`

**Step 3: Verify live reload works**

Run: `docker compose up -d`

Then open `app/main.py`, add a comment, save. Watch logs with `docker compose logs -f app` — uvicorn should log "Detected file change" and reload.

Run: `docker compose down`

**Step 4: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: add docker-compose.yml for dev"
```

---

### Task 4: Add Makefile targets

**Files:**
- Modify: `Makefile`

**Step 1: Add targets**

Add to `.PHONY` line: `docker-build docker-up`

Add after the existing `install` target:

```makefile
docker-build:
	docker build -t yes-person .

docker-up:
	docker compose up
```

**Step 2: Verify targets work**

Run: `make docker-build`
Expected: Image builds successfully, tagged `yes-person`.

Run: `make docker-up &` then `sleep 3 && curl -s http://localhost:8000/health && docker compose down`
Expected: `{"status":"ok"}`

**Step 3: Commit**

```bash
git add Makefile
git commit -m "chore: add docker-build and docker-up Makefile targets"
```
