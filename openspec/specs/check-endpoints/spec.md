## ADDED Requirements

### Requirement: Skill Definition
The `check-endpoints` skill MUST define a workflow for the LLM agent to validate all running mock endpoints against the Docker container.

#### Scenario: Running the skill
- **WHEN** the user invokes the `/check-endpoints` command or requests endpoint validation
- **THEN** the skill should guide the agent to perform the following steps:
  1. Ensure the `yes-person` server is running locally (e.g. `docker compose up -d`).
  2. Wait until the `/health` endpoint returns a 200 OK.
  3. Scan the `app/routers/` or `app/stubs/` directory to discover the current available mock endpoints.
  4. Perform test `curl` requests against the discovered endpoints.
  5. Validate that each endpoint returns a successful status code (200 or 201) and a JSON payload that matches expected structure (or simply succeeds without error).
  6. Present a clean summary of passed/failed endpoints to the user.
