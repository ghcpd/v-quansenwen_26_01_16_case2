# Configuration reference

FlagForge reads configuration from a JSON file and merges it with environment variables.

## File format

The top-level keys:

- `version` (number, default: `1`)
- `rules` (array) — list of rules

Each rule:

- `key` (string) — unique identifier
- `enabled` (boolean, default: `true`)
- `rollout` (integer between `0` and `100`, default: `100`) — percentage rollout
- `conditions` (array) — all conditions must match
- `salt` (string, default: `""`) — salt for deterministic bucketing

## Precedence

Order of precedence (highest first):

1. CLI arguments
2. Environment variables
3. Config file defaults

## Environment variables

- `FLAGFORGE_CONFIG_PATH` — path to the JSON config file
- `FLAGFORGE_LOG_LEVEL` — `debug|info|warn|error`
- `FLAGFORGE_HOST` — host address for the service (default: `127.0.0.1`)
- `FLAGFORGE_PORT` — port for the service (default: `9000`)

## Operators

Supported operators:

- `eq`, `neq`, `in`, `contains`, `regex`, `gt`, `gte`, `lt`, `lte`

Unknown operators cause the condition to not match (evaluation continues without error).
