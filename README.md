# FlagForge

FlagForge is a lightweight, configuration-driven feature-flag service and SDK.
It can be embedded as a library, used via a CLI, or run as a small HTTP service.

## Quick start

1) Create a JSON config file:

```json
{
  "version": 1,
  "rules": [
    {
      "key": "new_checkout",
      "enabled": true,
      "rollout": 25,
      "conditions": [
        { "field": "country", "op": "eq", "value": "US" }
      ]
    }
  ]
}
```

2) Evaluate a flag using the CLI:

```bash
python -m flagforge evaluate --config-path ./flagforge.json --key new_checkout --context '{"country":"US","user_id":"u123"}'
```

3) Run the service:

```bash
python -m flagforge serve --port 9000 --config-path ./flagforge.json
```

## Configuration

- Config files are JSON.
- Config path resolution: `--config-path` > `FLAGFORGE_CONFIG_PATH` > `./flagforge.json`.
- Host/port resolution when serving: CLI args override `FLAGFORGE_HOST` / `FLAGFORGE_PORT`, which fall back to `127.0.0.1:9000`.

See [docs/CONFIG.md](docs/CONFIG.md) for the full configuration reference.

## HTTP API

The service exposes:

- `POST /evaluate` — evaluate a rule for a given context

Response example:

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

See [docs/API.md](docs/API.md) for details.

## Development

Run tests:

```bash
python -m unittest -q
```
