from __future__ import annotations

import os


def get_log_level() -> str:
    level = os.environ.get("FLAGFORGE_LOG_LEVEL", "info")
    level = level.strip().lower()
    if level not in {"debug", "info", "warn", "error"}:
        return "info"
    return level
