"""Stub loader utility for yes-person mock server.

Reads JSON fixture files from app/stubs/{server_name}.json and caches them
in memory. Each fixture is a dict keyed by "{METHOD} {path}".
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_STUBS_DIR = Path(__file__).parent


@lru_cache(maxsize=None)
def load_stubs(server_name: str) -> dict:
    """Load and cache stub data for the given server name.

    Args:
        server_name: Snake-case name matching the stub JSON filename
                     (e.g., "pet_store" loads app/stubs/pet_store.json).

    Returns:
        Dict keyed by "{METHOD} {path}" (e.g., "GET /pets").
        Returns an empty dict if the file does not exist.
    """
    stub_file = _STUBS_DIR / f"{server_name}.json"
    if not stub_file.exists():
        return {}
    return json.loads(stub_file.read_text(encoding="utf-8"))
