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

- `200 OK` — returns `{ "result": { "key": "...", "enabled": true, "match": true, "reason": "matched" } }`
- `400 Bad Request` — invalid params, or malformed JSON

## GET /health

Returns plain text `ok`.

## Defaults

- Service listens on port `9000` by default.
