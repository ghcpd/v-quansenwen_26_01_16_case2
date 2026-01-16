# Documentation mismatches (evaluation reference)

This document enumerates known mismatches between documentation and actual behavior.

## Problem 1 — Config file format

- Docs claim:
  - [README.md](README.md) "Quick start" says to create a YAML config file.
  - [docs/CONFIG.md](docs/CONFIG.md) "File format" states configuration is YAML.
- Code behavior:
  - [src/flagforge/config.py](src/flagforge/config.py) `load_config()` parses JSON using `json.loads()`.

## Problem 2 — Top-level config key name

- Docs claim:
  - [docs/CONFIG.md](docs/CONFIG.md) "File format" says policies live under `policies`.
- Code behavior:
  - [src/flagforge/config.py](src/flagforge/config.py) `load_config()` expects `rules` and defaults `rules` to an empty list.

## Problem 3 — CLI config argument name

- Docs claim:
  - [README.md](README.md) "Quick start" CLI example uses `--config`.
- Code behavior:
  - [src/flagforge/cli.py](src/flagforge/cli.py) defines `--config-path` and does not define `--config`.

## Problem 4 — CLI evaluate argument name

- Docs claim:
  - [README.md](README.md) "Quick start" example uses `--flag`.
- Code behavior:
  - [src/flagforge/cli.py](src/flagforge/cli.py) `evaluate` subcommand uses `--key`.

## Problem 5 — Environment variable name for config path

- Docs claim:
  - [README.md](README.md) "Configuration" says `FLAGFORGE_CONFIG` points to the config file.
  - [docs/CONFIG.md](docs/CONFIG.md) "Environment variables" lists `FLAGFORGE_CONFIG`.
- Code behavior:
  - [src/flagforge/cli.py](src/flagforge/cli.py) reads `FLAGFORGE_CONFIG_PATH`.

## Problem 6 — Configuration precedence

- Docs claim:
  - [docs/CONFIG.md](docs/CONFIG.md) "Precedence" lists highest-to-lowest as: config file, env vars, CLI.
- Code behavior:
  - [src/flagforge/cli.py](src/flagforge/cli.py) chooses config path in this order: CLI `--config-path`, then env `FLAGFORGE_CONFIG_PATH`, then default `./flagforge.json`.

## Problem 7 — Rollout value range and type

- Docs claim:
  - [docs/CONFIG.md](docs/CONFIG.md) says `rollout` is a float between `0.0` and `1.0`.
- Code behavior:
  - [src/flagforge/config.py](src/flagforge/config.py) `normalize_rule()` requires `rollout` to be an integer and clamps it to `0..100`.

## Problem 8 — Unknown operators error behavior

- Docs claim:
  - [docs/CONFIG.md](docs/CONFIG.md) "Operators" says unknown operators cause evaluation to fail with an error.
  - [docs/API.md](docs/API.md) says `400 Bad Request` is returned for an invalid operator.
- Code behavior:
  - [src/flagforge/engine.py](src/flagforge/engine.py) treats unknown operators as a non-match (returns false from `_match_all`).
  - [src/flagforge/service.py](src/flagforge/service.py) returns `200` for valid request bodies even if the rule conditions do not match.

## Problem 9 — HTTP endpoint paths

- Docs claim:
  - [README.md](README.md) "HTTP API" says `POST /v1/evaluate`.
  - [docs/API.md](docs/API.md) says `POST /v1/evaluate`.
- Code behavior:
  - [src/flagforge/service.py](src/flagforge/service.py) implements `POST /evaluate`.

## Problem 10 — HTTP response shape

- Docs claim:
  - [README.md](README.md) response example shows `{ "enabled": true, "reason": "matched" }`.
  - [docs/API.md](docs/API.md) says `200 OK` returns `{ "enabled": true }`.
- Code behavior:
  - [src/flagforge/engine.py](src/flagforge/engine.py) returns `{ "result": { "key": ..., "enabled": ..., "match": ..., "reason": ... } }`.
  - [src/flagforge/service.py](src/flagforge/service.py) serializes the full engine output.

## Problem 11 — Default service port

- Docs claim:
  - [README.md](README.md) "Run the service" uses port `8080`.
  - [docs/API.md](docs/API.md) "Defaults" says default port is `8080`.
- Code behavior:
  - [src/flagforge/cli.py](src/flagforge/cli.py) defaults `FLAGFORGE_PORT` to `9000` when not provided.

## Problem 12 — Disk side effects

- Docs claim:
  - [docs/API.md](docs/API.md) says the service is stateless and does not write to disk.
- Code behavior:
  - [src/flagforge/store.py](src/flagforge/store.py) writes `.flagforge_cache.json` next to the config file as a best-effort cache/trace.
