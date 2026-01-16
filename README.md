# FlagForge

FlagForge is a lightweight, configuration-driven feature-flag service and SDK.
It can be embedded as a library, used via a CLI, or run as a small HTTP service.

## Quick start

1) Create a JSON config file (e.g., `flagforge.json`):

```json
{
  "version": 1,
  "rules": [
    {
      "key": "new_checkout",
      "enabled": true,
      "rollout": 25,
      "conditions": [
        {"field": "country", "op": "eq", "value": "US"}
      ]
    }
  ]
}
```

2) Evaluate a flag using the CLI:

```bash
python -m flagforge evaluate \
  --config-path ./flagforge.json \
  --key new_checkout \
  --context '{"country":"US","user_id":"u123"}'
```

Sample output:

```json
{"result":{"key":"new_checkout","enabled":true,"match":true,"reason":"matched"}}
```

3) Run the service:

```bash
python -m flagforge serve --config-path ./flagforge.json --port 9000 --host 127.0.0.1
```

Then call:

```bash
curl -s -X POST http://127.0.0.1:9000/evaluate \
  -H "content-type: application/json" \
  -d '{"key":"new_checkout","context":{"country":"US","user_id":"u123"}}'
```

Returns (example):

```json
{"result":{"key":"new_checkout","enabled":true,"match":true,"reason":"matched"}}
```

## Configuration

- Config files are **JSON** (not YAML). See [docs/CONFIG.md](docs/CONFIG.md) for the full reference.
- CLI arguments override environment variables; environment variables are used only for config-path/host/port defaults.
- Defaults:
  - Config path: `./flagforge.json`
  - Host: `127.0.0.1`
  - Port: `9000`
- Environment variables:
  - `FLAGFORGE_CONFIG_PATH` — override config path used by the CLI
  - `FLAGFORGE_HOST` / `FLAGFORGE_PORT` — defaults for `serve`
  - `FLAGFORGE_LOG_LEVEL` — `debug|info|warn|error` (used by `flagforge.logging.get_log_level()`)

## HTTP API

The service exposes:

- `POST /evaluate` — evaluate a rule for a given context. Body: `{ "key": "...", "context": { ... } }`
- `GET /health` — returns plain text `ok`

Response shape on success:

```json
{
  "result": {
    "key": "new_checkout",
    "enabled": true,
    "match": true,
    "reason": "matched"
  }
}
```

Possible `reason` values: `missing_rule`, `disabled`, `conditions_not_met`, `matched`, `rollout_excluded`.

See [docs/API.md](docs/API.md) for details and error codes.

## Development

Run tests (ensure `src` is on `PYTHONPATH`):

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
# PowerShell:
# $env:PYTHONPATH="src"; python -m unittest discover -s tests -v
```
