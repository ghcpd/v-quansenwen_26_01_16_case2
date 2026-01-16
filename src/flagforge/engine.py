from __future__ import annotations

from typing import Any, Dict, Optional

from .config import normalize_rule
from .operators import OPS
from .util import stable_percent


class FlagForge:
    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._rules_by_key: Dict[str, Dict[str, Any]] = {}
        for rule in config.get("rules", []):
            norm = normalize_rule(rule)
            self._rules_by_key[norm["key"]] = norm

    def evaluate(self, key: str, context: Dict[str, Any]) -> Dict[str, Any]:
        rule = self._rules_by_key.get(key)
        if not rule:
            return {
                "result": {
                    "key": key,
                    "enabled": False,
                    "match": False,
                    "reason": "missing_rule",
                }
            }

        if not rule.get("enabled", True):
            return {
                "result": {
                    "key": key,
                    "enabled": False,
                    "match": False,
                    "reason": "disabled",
                }
            }

        matched = self._match_all(rule.get("conditions", []), context)
        if not matched:
            return {
                "result": {
                    "key": key,
                    "enabled": False,
                    "match": False,
                    "reason": "conditions_not_met",
                }
            }

        rollout = int(rule.get("rollout", 100))
        bucket_key = str(context.get("user_id") or context.get("id") or "")
        if not bucket_key:
            # Without a stable identifier, treat as not eligible for partial rollout.
            eligible = rollout >= 100
        else:
            percent = stable_percent(bucket_key, salt=str(rule.get("salt", "")))
            eligible = percent < rollout

        return {
            "result": {
                "key": key,
                "enabled": bool(eligible),
                "match": bool(eligible),
                "reason": "matched" if eligible else "rollout_excluded",
            }
        }

    def _match_all(self, conditions: Any, context: Dict[str, Any]) -> bool:
        if not isinstance(conditions, list):
            return False

        for cond in conditions:
            if not isinstance(cond, dict):
                return False

            field = cond.get("field")
            op = cond.get("op")
            value = cond.get("value")

            if not isinstance(field, str) or not isinstance(op, str):
                return False

            left = context.get(field)
            fn = OPS.get(op)
            if fn is None:
                # Unknown operators are treated as non-match.
                return False

            if not fn(left, value):
                return False

        return True
