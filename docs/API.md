# HTTP API

The FlagForge service evaluates rules from a JSON config file over HTTP. It caches the config in memory and best-effort writes `.flagforge_cache.json` alongside the config file; it is **not strictly stateless**.

## POST /evaluate

Request body:

```json
{
  "key": "new_checkout",
  "context": { "user_id": "u123", "country": "US" }
}
```

Response (`200 OK` on success):

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

`reason` values:
- `missing_rule` — no rule with that key
- `disabled` — rule is disabled
- `conditions_not_met` — conditions failed or were invalid/unknown operator
- `matched` — conditions matched and rollout included the bucket
- `rollout_excluded` — conditions matched but bucket fell outside rollout

Error responses:
- `400` with `{ "error": "invalid_json" }` — malformed JSON
- `400` with `{ "error": "invalid_body" }` — body is not a JSON object
- `400` with `{ "error": "invalid_params" }` — `key` not a string or `context` not an object
- `404` with `{ "error": "not_found" }` — unknown path

> Unknown operators and invalid regex patterns do **not** return `400`; they simply cause the rule to not match, yielding `conditions_not_met` with `200 OK`.
> Config/IO errors are not caught by the handler and will surface as server errors.

## GET /health

Returns plain text `ok`.

## Defaults

- Service binds to `127.0.0.1:9000` by default (override via `--host`, `--port`, or `FLAGFORGE_HOST`/`FLAGFORGE_PORT`).
