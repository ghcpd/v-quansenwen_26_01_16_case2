from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional

from .config import load_config


class FileConfigStore:
    def __init__(self, config_path: str, *, cache_path: Optional[str] = None):
        self._config_path = config_path
        self._cache_path = cache_path or os.path.join(os.path.dirname(config_path), ".flagforge_cache.json")
        self._last_mtime: Optional[float] = None
        self._config: Optional[Dict[str, Any]] = None

    @property
    def config_path(self) -> str:
        return self._config_path

    def get_config(self) -> Dict[str, Any]:
        mtime = os.path.getmtime(self._config_path)
        if self._config is None or self._last_mtime != mtime:
            self._config = load_config(self._config_path)
            self._last_mtime = mtime
            self._write_cache(self._config)
        return self._config

    def _write_cache(self, cfg: Dict[str, Any]) -> None:
        payload = {"loaded_at": int(time.time()), "config_path": self._config_path, "config": cfg}
        try:
            with open(self._cache_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, sort_keys=True)
        except OSError:
            # Best-effort only.
            pass
