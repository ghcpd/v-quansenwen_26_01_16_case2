import json
import os
import unittest

from flagforge.service import create_app
from flagforge.store import FileConfigStore


class TestService(unittest.TestCase):
    def test_health(self):
        cfg_path = os.path.join(os.path.dirname(__file__), "fixtures", "config.json")
        app = create_app(FileConfigStore(cfg_path))
        status, headers, body = app.handle("GET", "/health", {}, b"")
        self.assertEqual(status, 200)
        self.assertIn(b"ok", body)

    def test_evaluate_endpoint(self):
        cfg_path = os.path.join(os.path.dirname(__file__), "fixtures", "config.json")
        app = create_app(FileConfigStore(cfg_path))
        payload = {"key": "new_checkout", "context": {"country": "US", "user_id": "u2"}}
        status, headers, body = app.handle(
            "POST",
            "/evaluate",
            {"content-type": "application/json"},
            json.dumps(payload).encode("utf-8"),
        )
        self.assertEqual(status, 200)
        data = json.loads(body.decode("utf-8"))
        self.assertTrue(data["result"]["enabled"])


if __name__ == "__main__":
    unittest.main()
