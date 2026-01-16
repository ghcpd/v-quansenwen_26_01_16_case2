from __future__ import annotations

import json
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    """Load a FlagForge config from disk.

    The config file is expected to be JSON.
    """
    with open(path, "rb") as f:
        raw = f.read()

    cfg = json.loads(raw.decode("utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError("config root must be an object")

    cfg.setdefault("version", 1)
    cfg.setdefault("rules", [])
    if not isinstance(cfg["rules"], list):
        raise ValueError("rules must be an array")

    return cfg


def normalize_rule(rule: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(rule)
    out.setdefault("enabled", True)
    out.setdefault("rollout", 100)
    out.setdefault("conditions", [])
    out.setdefault("salt", "")

    if not isinstance(out.get("key"), str) or not out["key"]:
        raise ValueError("rule.key must be a non-empty string")

    rollout = out.get("rollout")
    if not isinstance(rollout, int):
        raise ValueError("rule.rollout must be an int")
    if rollout < 0:
        out["rollout"] = 0
    if rollout > 100:
        out["rollout"] = 100

    if not isinstance(out["conditions"], list):
        raise ValueError("rule.conditions must be an array")

    return out
