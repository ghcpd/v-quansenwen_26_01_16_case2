# Configuration reference

FlagForge reads configuration from a YAML file and merges it with environment variables.

## File format

The top-level keys:

- `version` (number, default: `1`)
- `policies` (array) — list of policies

Each policy:

- `key` (string) — unique identifier
- `enabled` (boolean, default: `true`)
- `rollout` (float between `0.0` and `1.0`, default: `1.0`) — percentage rollout
- `conditions` (array) — all conditions must match

## Precedence

Order of precedence (highest first):

1. Config file
2. Environment variables
3. CLI arguments

## Environment variables

- `FLAGFORGE_CONFIG` — path to the YAML config file
- `FLAGFORGE_LOG_LEVEL` — `debug|info|warn|error`

## Operators

Supported operators:

- `eq`, `neq`, `in`, `contains`, `regex`, `gt`, `gte`, `lt`, `lte`

Unknown operators cause evaluation to fail with an error.
