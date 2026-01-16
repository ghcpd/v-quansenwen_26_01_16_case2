# FlagForge

FlagForge is a lightweight, configuration-driven feature-flag service and SDK.
It can be embedded as a library, used via a CLI, or run as a small HTTP service.

## Quick start

1) Create a YAML config file:

```yaml
version: 1
policies:
  - key: "new_checkout"
    enabled: true
    rollout: 0.25
    conditions:
      - field: "country"
        op: "eq"
        value: "US"
```

2) Evaluate a flag using the CLI:

```bash
python -m flagforge evaluate --config ./flagforge.yaml --flag new_checkout --context '{"country":"US","user_id":"u123"}'
```

3) Run the service:

```bash
python -m flagforge serve --port 8080 --config ./flagforge.yaml
```

## Configuration

- Config files are YAML.
- CLI flags override environment variables, and environment variables override the config file.
- `FLAGFORGE_CONFIG` points to the config file path.

See [docs/CONFIG.md](docs/CONFIG.md) for full configuration reference.

## HTTP API

The service exposes:

- `POST /v1/evaluate` — evaluate a flag for a given context

Response example:

```json
{ "enabled": true, "reason": "matched" }
```

See [docs/API.md](docs/API.md) for details.

## Development

Run tests:

```bash
python -m unittest -q
```
