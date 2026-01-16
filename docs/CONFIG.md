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
- `salt` (string, default: `""`) — optional salt for rollout bucketing

## Precedence

Order of precedence (highest first):

1. CLI arguments
2. Environment variables
3. Default values

## Environment variables

- `FLAGFORGE_CONFIG_PATH` — path to the JSON config file
- `FLAGFORGE_HOST` — host to bind (default: `127.0.0.1`)
- `FLAGFORGE_PORT` — port to bind (default: `9000`)

## Operators

Supported operators:

- `eq`, `neq`, `in`, `contains`, `regex`, `gt`, `gte`, `lt`, `lte`

Unknown operators cause the condition to evaluate as non-matching.
