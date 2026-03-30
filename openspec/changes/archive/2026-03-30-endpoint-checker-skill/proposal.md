## Why

Currently, testing the mock endpoints involves manually starting the server, remembering curl commands, and manually parsing JSON. An OpenCode/Claude skill to autonomously spin up the Docker container, ensure it's healthy, and automatically hit all generated endpoints would streamline the validation phase of adding new mocks to the `yes-person` API.

## What Changes

- Create a new skill named `check-endpoints`.
- The skill will be able to run `docker compose up -d`.
- The skill will check if the server is healthy by hitting the `/health` endpoint.
- The skill will read the available mock routes from the application (or from an OpenAPI spec/stub file) and hit them to ensure they return a `200` or `201` status code and valid JSON.
- The skill will gracefully shut down the docker container after testing if it was responsible for starting it (or can be left running depending on the user's preference).

## Capabilities

### New Capabilities
- `check-endpoints`: A skill that validates a running mock server by exercising all its defined endpoints.

### Modified Capabilities
*(None)*

## Impact

- Adds new skill definitions in `.claude/skills/check-endpoints/SKILL.md` and `.opencode/skills/check-endpoints/SKILL.md`.
- No application code will be modified.
