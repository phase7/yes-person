## Why

During the implementation of the `check-endpoints` skill, we added a mock PickPost API to verify the skill worked correctly. Now that the skill has been successfully verified, we need to remove these test endpoints to keep the `yes-person` API clean and focused.

## What Changes

- Remove the `app/routers/dcapi_pickpost.py` file.
- Remove the `app/models/dcapi_pickpost.py` file.
- Remove the `app/stubs/dcapi_pickpost.json` file.
- Remove the `specs/dcapi-pickpost/pickpost.yaml` file.
- Remove the `tests/test_pickpost_routes.py` file.
- **BREAKING**: Unregister the router from `app/main.py`. This will remove the endpoints from the server.
- Update test snapshots as required.

## Capabilities

### New Capabilities
*(None)*

### Modified Capabilities
- `remove-test-endpoints`: Removing the test endpoints added for checking the endpoint-checker skill.

## Impact

- The `dcapi-pickpost` endpoints will no longer be available. This is intentional as they were for testing only.
