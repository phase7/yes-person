# FastAPI Scaffold Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Initialize the yes-person repo as a working FastAPI project with uv, Makefile workflow, and pytest + syrupy snapshot testing.

**Architecture:** Flat module layout with `app/` at repo root. `app/main.py` creates the FastAPI instance and includes a health route. Tests use `httpx.TestClient` with syrupy snapshots. Makefile wraps all `uv run` commands.

**Tech Stack:** Python 3.13, FastAPI, uv, pytest, syrupy, httpx, ruff

---

### Task 1: Initialize uv project with pyproject.toml

**Files:**
- Create: `pyproject.toml`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "yes-person"
version = "0.1.0"
description = "Mock API server driven by OpenAPI specs"
requires-python = ">=3.13"
dependencies = [
    "fastapi[standard]",
]

[dependency-groups]
dev = [
    "pytest",
    "syrupy",
    "httpx",
    "ruff",
]
```

**Step 2: Pin Python version**

Run: `uv python pin 3.13`
Expected: Creates/updates `.python-version` to `3.13`

**Step 3: Install dependencies**

Run: `uv sync`
Expected: Creates `uv.lock`, installs all deps into `.venv/`. Output includes `fastapi`, `pytest`, `syrupy`, `httpx`, `ruff`.

**Step 4: Verify installation**

Run: `uv run python -c "import fastapi; print(fastapi.__version__)"`
Expected: Prints a version number (e.g., `0.115.x` or similar)

**Step 5: Commit**

```bash
git add pyproject.toml uv.lock .python-version
git commit -m "chore: initialize uv project with fastapi and dev dependencies"
```

---

### Task 2: Create FastAPI app with health route

**Files:**
- Create: `app/__init__.py`
- Create: `app/main.py`
- Create: `app/routers/__init__.py`
- Create: `app/models/__init__.py`

**Step 1: Create empty package files**

Create these three empty files (zero bytes):
- `app/__init__.py`
- `app/routers/__init__.py`
- `app/models/__init__.py`

**Step 2: Create app/main.py**

```python
from fastapi import FastAPI

app = FastAPI(title="yes-person", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}
```

**Step 3: Verify the server starts**

Run: `uv run fastapi dev app/main.py &`
Then: `curl -s http://127.0.0.1:8000/health`
Expected: `{"status":"ok"}`
Then: kill the background process.

**Step 4: Commit**

```bash
git add app/
git commit -m "feat: add FastAPI app with health endpoint"
```

---

### Task 3: Add test infrastructure and health snapshot test

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_health.py`

**Step 1: Create tests/__init__.py**

Empty file (zero bytes).

**Step 2: Create tests/conftest.py**

```python
import pytest
from httpx import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
```

Note: `httpx.TestClient` is a drop-in replacement that works with FastAPI (re-exported from `starlette.testclient` under the hood, but importing from `httpx` is the modern approach — if it fails, fall back to `from starlette.testclient import TestClient`).

**Step 3: Write the snapshot test in tests/test_health.py**

```python
def test_health_returns_ok(client, snapshot):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == snapshot
```

**Step 4: Run test — expect snapshot missing**

Run: `uv run pytest tests/test_health.py -v`
Expected: FAIL — syrupy reports 1 missing snapshot.

**Step 5: Update snapshots**

Run: `uv run pytest tests/test_health.py -v --snapshot-update`
Expected: PASS — syrupy creates `tests/__snapshots__/test_health.ambr` with the snapshot `{"status": "ok"}`.

**Step 6: Run tests again to confirm green**

Run: `uv run pytest tests/test_health.py -v`
Expected: PASS — snapshot now matches.

**Step 7: Commit**

```bash
git add tests/
git commit -m "test: add snapshot test for health endpoint"
```

---

### Task 4: Create Makefile

**Files:**
- Create: `Makefile`

**Step 1: Create Makefile**

```makefile
.PHONY: dev test test-update lint format install

dev:
	uv run fastapi dev app/main.py

test:
	uv run pytest

test-update:
	uv run pytest --snapshot-update

lint:
	uv run ruff check .

format:
	uv run ruff format .

install:
	uv sync
```

**Important:** Each indented line under a target MUST use a real tab character, not spaces.

**Step 2: Verify make test works**

Run: `make test`
Expected: Runs pytest, all tests pass (1 passed).

**Step 3: Verify make lint works**

Run: `make lint`
Expected: ruff check passes with no errors (or reports issues to fix).

**Step 4: Commit**

```bash
git add Makefile
git commit -m "chore: add Makefile with dev workflow shortcuts"
```

---

### Task 5: Add .gitignore and final verification

**Files:**
- Create: `.gitignore`

**Step 1: Create .gitignore**

```gitignore
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/
.ruff_cache/
```

**Step 2: Run full verification**

Run these in sequence:
```bash
make install
make lint
make test
```

Expected: All three commands succeed. Tests show 1 passed.

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore"
```

---

### Task 6: Update CLAUDE.md with actual commands

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update the Development Commands section**

Replace the Development Commands section to include Makefile targets alongside the raw commands:

```markdown
## Development Commands

```bash
# Install dependencies
make install    # or: uv sync

# Run the dev server
make dev        # or: uv run fastapi dev app/main.py

# Run tests
make test       # or: uv run pytest

# Run a single test
uv run pytest tests/test_foo.py::test_name -v

# Update syrupy snapshots
make test-update  # or: uv run pytest --snapshot-update

# Lint / format
make lint       # or: uv run ruff check .
make format     # or: uv run ruff format .
```
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with Makefile commands"
```
