# Configuration reference

FlagForge loads configuration from a **JSON** file. Rule data is **not merged** from environment variables; env vars only influence CLI defaults (config path/host/port) and logging level.

## File format

Top-level keys:

- `version` (number, default `1`)
- `rules` (array, default `[]`) — list of rules

Each rule:

- `key` (string, required, non-empty)
- `enabled` (boolean, default `true`)
- `rollout` (int percentage `0`–`100`, default `100`; values outside range are clipped; non-int raises `ValueError`)
- `conditions` (array, default `[]`)
- `salt` (string, default `""`)

> Empty `conditions` means the rule matches. Invalid condition structures (non-dict, missing `field`/`op`, non-string `field`/`op`) cause the rule **not** to match, without raising.

### Bucketing & rollout

- A deterministic bucket `0..99` is computed via `stable_percent` using `context.user_id` or `context.id` (stringified) plus optional `salt`.
- If neither `user_id` nor `id` is present, partial rollouts (`rollout < 100`) are treated as not eligible; full rollout (`>= 100`) always passes after conditions.

## Reloading & caching

`FileConfigStore` reloads when the config file mtime changes, caches in memory, and best-effort writes a cache file `.flagforge_cache.json` alongside the config path (errors are ignored).

## Precedence (CLI defaults)

Highest precedence first for **CLI defaults** only:

1. CLI arguments (`--config-path`, `--host`, `--port`)
2. Environment variables
3. Built-in defaults (`./flagforge.json`, `127.0.0.1`, `9000`)

Rule contents come solely from the JSON file.

## Environment variables

- `FLAGFORGE_CONFIG_PATH` — path to the JSON config file (used by CLI)
- `FLAGFORGE_HOST` — default host for `serve`
- `FLAGFORGE_PORT` — default port for `serve`
- `FLAGFORGE_LOG_LEVEL` — one of `debug|info|warn|error` (used by `flagforge.logging.get_log_level()`)

## Operators

Supported operators:

- `eq`, `neq`, `in`, `contains`, `regex`, `gt`, `gte`, `lt`, `lte`

Operator behavior:

- `in`: `right` must be a list/tuple/set; otherwise returns `False`
- `contains`: supports substring for strings and membership for list/tuple/set
- `regex`: invalid regex patterns return `False` (no exception)
- `gt/gte/lt/lte`: `TypeError` is caught and returns `False`
- Unknown operators cause the rule to **not match** (no exception is raised)
