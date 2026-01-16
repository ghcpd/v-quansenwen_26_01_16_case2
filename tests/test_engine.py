import json
import os
import unittest

from flagforge.config import load_config
from flagforge.engine import FlagForge
from flagforge.store import FileConfigStore


class TestEngine(unittest.TestCase):
    def test_evaluate_true_when_condition_matches(self):
        cfg = load_config(os.path.join(os.path.dirname(__file__), "fixtures", "config.json"))
        engine = FlagForge(cfg)
        result = engine.evaluate("new_checkout", {"country": "US", "user_id": "u2"})
        self.assertTrue(result["result"]["enabled"])
        self.assertEqual(result["result"]["key"], "new_checkout")

    def test_evaluate_false_when_condition_not_match(self):
        cfg = load_config(os.path.join(os.path.dirname(__file__), "fixtures", "config.json"))
        engine = FlagForge(cfg)
        result = engine.evaluate("new_checkout", {"country": "CA", "user_id": "u2"})
        self.assertFalse(result["result"]["enabled"])

    def test_unknown_operator_is_not_error(self):
        cfg_path = os.path.join(os.path.dirname(__file__), "fixtures", "config.json")
        cfg = load_config(cfg_path)
        cfg["rules"][0]["conditions"].append({"field": "country", "op": "unknown", "value": "US"})
        engine = FlagForge(cfg)
        out = engine.evaluate("new_checkout", {"country": "US", "user_id": "u2"})
        self.assertIn("result", out)

    def test_store_reads_from_path(self):
        cfg_path = os.path.join(os.path.dirname(__file__), "fixtures", "config.json")
        store = FileConfigStore(cfg_path)
        cfg = store.get_config()
        self.assertIn("rules", cfg)


if __name__ == "__main__":
    unittest.main()
