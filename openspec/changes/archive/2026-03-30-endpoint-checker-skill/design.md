## Context

OpenCode / Claude skills are executed directly by the LLM via tool calls. They provide system-prompt-level workflow instructions to guide the model when certain operations are needed. For `yes-person` developers, we already have an ingest skill to generate mock endpoints. The next logical step is to verify them locally using the actual Docker setup.

## Goals / Non-Goals

**Goals:**
- Provide an LLM-actionable skill to start `docker compose up -d` in the background.
- Test that the `/health` endpoint is responsive.
- Query available routes (via reading router files, reading `app/stubs/` or `app/main.py`) to discover mocked endpoints.
- Auto-generate payloads for `POST`/`PUT` if necessary (relying on the LLM's logic, or using the stub data).
- Ensure endpoints respond with 20X codes and valid responses.
- Output a structured success/failure summary for the user.

**Non-Goals:**
- Do not build a standalone Python script to test endpoints. It should be a workflow instructed directly to the agent so that it tests and reports dynamically based on what it finds.

## Decisions

- **Discovery Mechanism:** The skill will instruct the agent to use `glob` and `read` tools to find the router and stub files, and hit those endpoints using `curl` or python script generated on the fly.
- **Docker Workflow:** The skill will advise running `docker compose up -d` using the `bash` tool, then running a sleep to allow it to initialize, then hitting `localhost:8000/health`.

## Risks / Trade-offs

- **Risk**: Docker may take a while to spin up on some machines, causing the health check to fail immediately.
- **Mitigation**: The skill will explicitly instruct the agent to retry the health check a few times with a `sleep` in between before failing.
