## 1. Skill Creation

- [x] 1.1 Create the skill definition file at `.claude/skills/check-endpoints/SKILL.md` (and `.opencode/skills/check-endpoints/SKILL.md` mirroring it).
- [x] 1.2 Include frontmatter: `name: check-endpoints`, `description: Validates running mock server endpoints locally`.

## 2. Command Aliases

- [x] 2.1 Add `/check` or `/endpoints` alias in `.claude/commands/check.md` and `.opencode/command/check.md` pointing to the skill execution.

## 3. Skill Content Verification

- [x] 3.1 Validate the prompt instructs the agent to run `docker compose up -d`
- [x] 3.2 Validate the prompt instructs the agent to check `/health` with retries.
- [x] 3.3 Validate the prompt instructs the agent to read stub JSON payloads to construct curl calls to generated endpoints.
- [x] 3.4 Validate the prompt requires a concluding summary for the user of passed vs failed endpoints.
