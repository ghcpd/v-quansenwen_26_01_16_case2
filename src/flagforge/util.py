from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_percent(bucket_key: str, *, salt: str = "") -> int:
    """Return a deterministic integer 0..99 for a given key."""
    digest = hashlib.sha256((salt + "|" + bucket_key).encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 100


def json_loads_bytes(data: bytes) -> Any:
    if not data:
        return None
    return json.loads(data.decode("utf-8"))
