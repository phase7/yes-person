## REMOVED Requirements

### Requirement: PickPost Test Mock
The system MUST provide mock `dcapi-pickpost` endpoints for checking mock validity.

**Reason**: This was a test mock created solely to verify the `/check-endpoints` skill and is no longer needed in the project.
**Migration**: N/A - these mock test files are simply to be deleted.

#### Scenario: Requesting PickPost endpoints
- **WHEN** user requests `/v1/dcapi-pickpost/users` or any PickPost test endpoint
- **THEN** system MUST return a `404 Not Found` or the catch-all "stub_not_found" error payload.
