# Markdown to PPTX Module

## Overview

The `md_to_pptx` module converts Markdown content into PowerPoint PPTX format and returns the result as a base64-encoded string suitable for JSON transport.

## HTTP Endpoint

**Route:** `/api/md_to_pptx/convert`  
**Method:** `POST`  
**Content-Type:** `application/json`

## Request Format

```json
{
  "markdown": "# Title\nBody text"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `markdown` | string | Yes | Markdown content to convert to PPTX |

## Response Format

### Success Response (200)

```json
{
  "status": "ok",
  "result": {
    "pptx_base64": "UEsDBBQABgAIAAAAIQD...",
    "size_bytes": 4567
  }
}
```

### Error Response (400, 500)

```json
{
  "status": "error",
  "error": {
    "msg": "Error description"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "ok" on success, "error" on failure |
| `result.pptx_base64` | string | Base64-encoded PPTX file content |
| `result.size_bytes` | integer | Approximate size of the PPTX file in bytes |
| `error.msg` | string | Human-readable error message |

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Conversion successful |
| 400 | Invalid or missing input (e.g., missing `markdown`) |
| 500 | Internal server error (e.g., pandoc failure) |

## Functions

### `handle_request(payload: dict[str, Any]) -> dict[str, Any]`

Validates input and performs Markdown to PPTX conversion.

**Raises:**
- `ValueError`: Missing or empty `markdown` parameter.
- `RuntimeError`: Conversion failure.

## Dependencies

- `pypandoc` (requires Pandoc binary available at runtime)

## Usage Examples

See [md_to_pptx-curl.md](../examples/md_to_pptx-curl.md) for curl examples.

## Error Handling

- Input validation for missing or empty `markdown`.
- Conversion errors surfaced as `RuntimeError` and mapped to HTTP 500 in the route.

## Security Considerations

- No external network calls beyond pandoc binary; conversion is local.
- Input is treated as plain text; ensure upstream callers trust the content.

## Limitations

- Requires Pandoc binary in the runtime environment.
- Does not apply custom templates/themes (future enhancement).

## Related Documentation

- [Implementation Notes](../implementation/md_to_pptx.md)
- [Usage Examples](../examples/md_to_pptx-curl.md)
