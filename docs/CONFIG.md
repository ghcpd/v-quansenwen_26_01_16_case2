# Configuration reference

FlagForge reads configuration from a JSON file. The file contents are used as-is; environment variables only influence which file is loaded and (when serving) the bind host/port.

## File format

The top-level keys:

- `version` (number, default: `1`)
- `rules` (array, default: `[]`) — list of rules

Each rule:

- `key` (string, required) — unique identifier
- `enabled` (boolean, default: `true`)
- `rollout` (integer 0–100, default: `100`) — percentage of traffic allowed; values outside the range are clamped
- `conditions` (array, default: `[]`) — all conditions must match; non-array values raise an error at load time
- `salt` (string, default: `""`) — included in the rollout hash

## Precedence

Config path resolution (highest precedence first):

1. CLI: `--config-path`
2. Env: `FLAGFORGE_CONFIG_PATH`
3. Default: `./flagforge.json`

## Environment variables

- `FLAGFORGE_CONFIG_PATH` — path to the JSON config file
- `FLAGFORGE_HOST` / `FLAGFORGE_PORT` — defaults to `127.0.0.1` and `9000` when serving
- `FLAGFORGE_LOG_LEVEL` — `debug|info|warn|error` (currently only normalized via `flagforge.logging.get_log_level`)

## Operators

Supported operators:

- `eq`, `neq`, `in`, `contains`, `regex`, `gt`, `gte`, `lt`, `lte`

Unknown operators are treated as non-matches during evaluation (no exception is raised).
