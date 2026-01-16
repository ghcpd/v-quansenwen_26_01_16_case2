# HTTP API

The FlagForge service is a stateless HTTP API for evaluating flags.
It does not write to disk.

## POST /evaluate

Request body:

```json
{
  "key": "new_checkout",
  "context": { "user_id": "u123", "country": "US" }
}
```

Responses:

- `200 OK` — returns the evaluation result under `result`
- `400 Bad Request` — malformed JSON, non-object body, or missing/invalid `key`/`context` (error codes: `invalid_json`, `invalid_body`, `invalid_params`)
- `404 Not Found` — any other path (error code: `not_found`)

Successful response example:

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

Notes:

- Unknown operators are treated as non-matches (no error); the response will have `match: false` and `reason: "conditions_not_met"`.
- Rollouts use `user_id` (or `id`) from the context when present; without an identifier, only `rollout: 100` rules can enable.

## GET /health

Returns plain text `ok`.

## Defaults

- Service listens on `127.0.0.1:9000` by default.
