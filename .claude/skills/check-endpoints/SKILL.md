---
name: check-endpoints
description: Validates running mock server endpoints locally
---

# Skill: check-endpoints

This skill instructs the AI agent on how to validate all mock endpoints in the `yes-person` API by running them locally with Docker.

**When to use:**
When the user asks to "check endpoints", "test endpoints", or invokes the `/check` command.

**Execution Steps:**

1. **Start the Docker container:**
   - Use the `bash` tool to run `docker compose up -d`
   - Alternatively, you can run `uv run uvicorn app.main:app --port 8000 &` if the user prefers not to use Docker, but Docker is the default.

2. **Wait for Health Check:**
   - The server may take a moment to start.
   - Use the `bash` tool to loop and `curl -s http://localhost:8000/health`.
   - Retry a few times with a `sleep 2` in between until it returns a 200 OK with `{"status": "ok"}`.
   - If it fails after 5 attempts, halt the skill and report the failure to the user.

3. **Discover Endpoints:**
   - Use `glob` and `read` tools to scan `app/routers/` or `app/stubs/` to discover the available mock endpoints.
   - Read the stub JSON files (e.g. `app/stubs/*.json`) to find out the exact `"{METHOD} {path}"` keys that are currently mocked and the expected payload shapes.

4. **Test Endpoints:**
   - Iterate through the discovered endpoints.
   - For `GET` endpoints, construct a simple `curl` request.
   - For `POST`/`PUT`/`PATCH` endpoints, look at the stub data or models to construct a valid (or minimal) JSON payload.
   - Execute the `curl` commands using the `bash` tool.
   - Verify that the response status code is `200` or `201` and that a valid JSON body is returned.

5. **Summarize Results:**
   - Present a clean, structured summary to the user.
   - Show how many endpoints were tested.
   - List the **Passed** endpoints.
   - List any **Failed** endpoints along with the error or unexpected status code.
   - Ask the user if they'd like you to shut down the server (e.g., `docker compose down`).
