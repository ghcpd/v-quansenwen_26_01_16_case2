from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict

from .engine import FlagForge
from .store import FileConfigStore
from .service import serve


def _env(name: str) -> str | None:
    v = os.environ.get(name)
    return v if v else None


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="flagforge")
    p.add_argument("--config-path", default=None, help="Path to JSON config file")
    p.add_argument("--log-level", default=None, help="debug|info|warn|error")

    sub = p.add_subparsers(dest="cmd", required=True)

    ev = sub.add_parser("evaluate", help="Evaluate a rule")
    ev.add_argument("--key", required=True, help="Rule key")
    ev.add_argument("--context", required=True, help="Context as JSON object")

    sv = sub.add_parser("serve", help="Run HTTP service")
    sv.add_argument("--host", default=None)
    sv.add_argument("--port", type=int, default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config_path = (
        args.config_path
        or _env("FLAGFORGE_CONFIG_PATH")
        or os.path.join(os.getcwd(), "flagforge.json")
    )

    if args.cmd == "evaluate":
        store = FileConfigStore(config_path)
        engine = FlagForge(store.get_config())

        try:
            ctx = json.loads(args.context)
        except json.JSONDecodeError:
            print(json.dumps({"error": "invalid_context_json"}))
            return 2

        if not isinstance(ctx, dict):
            print(json.dumps({"error": "context_must_be_object"}))
            return 2

        out = engine.evaluate(args.key, ctx)
        print(json.dumps(out))
        return 0

    if args.cmd == "serve":
        host = args.host or _env("FLAGFORGE_HOST") or "127.0.0.1"
        port = args.port or int(_env("FLAGFORGE_PORT") or "9000")
        store = FileConfigStore(config_path)
        serve(host=host, port=port, store=store)
        return 0

    return 2
