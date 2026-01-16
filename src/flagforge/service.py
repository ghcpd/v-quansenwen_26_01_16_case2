from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Tuple

from .engine import FlagForge
from .util import json_loads_bytes


class App:
    def __init__(self, store: Any):
        self._store = store

    def handle(self, method: str, path: str, headers: Dict[str, str], body: bytes) -> Tuple[int, Dict[str, str], bytes]:
        if method == "GET" and path == "/health":
            return 200, {"content-type": "text/plain"}, b"ok"

        if method == "POST" and path == "/evaluate":
            try:
                payload = json_loads_bytes(body)
            except json.JSONDecodeError:
                return 400, {"content-type": "application/json"}, b"{\"error\":\"invalid_json\"}"

            if not isinstance(payload, dict):
                return 400, {"content-type": "application/json"}, b"{\"error\":\"invalid_body\"}"

            key = payload.get("key")
            context = payload.get("context")
            if not isinstance(key, str) or not isinstance(context, dict):
                return 400, {"content-type": "application/json"}, b"{\"error\":\"invalid_params\"}"

            cfg = self._store.get_config()
            engine = FlagForge(cfg)
            out = engine.evaluate(key, context)
            return 200, {"content-type": "application/json"}, json.dumps(out).encode("utf-8")

        return 404, {"content-type": "application/json"}, b"{\"error\":\"not_found\"}"


def create_app(store: Any) -> App:
    return App(store)


def serve(*, host: str, port: int, store: Any) -> None:
    app = create_app(store)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            status, resp_headers, body = app.handle("GET", self.path, self._headers_dict(), b"")
            self._send(status, resp_headers, body)

        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("content-length", "0") or "0")
            data = self.rfile.read(length) if length else b""
            status, resp_headers, body = app.handle("POST", self.path, self._headers_dict(), data)
            self._send(status, resp_headers, body)

        def log_message(self, fmt: str, *args: Any) -> None:
            return

        def _headers_dict(self) -> Dict[str, str]:
            return {k.lower(): v for k, v in self.headers.items()}

        def _send(self, status: int, headers: Dict[str, str], body: bytes) -> None:
            self.send_response(status)
            for k, v in headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

    httpd = HTTPServer((host, port), Handler)
    httpd.serve_forever()
