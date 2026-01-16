# HTTP API

The FlagForge service is a stateless HTTP API for evaluating flags.
It does not write to disk.

## POST /v1/evaluate

Request body:

```json
{
  "flag": "new_checkout",
  "context": { "user_id": "u123", "country": "US" }
}
```

Responses:

- `200 OK` — returns `{ "enabled": true }`
- `400 Bad Request` — invalid operator, invalid config, or malformed JSON

## GET /health

Returns plain text `ok`.

## Defaults

- Service listens on port `8080` by default.
