# Markdown to PPTX - curl Examples

## Prerequisites

- Function app running locally (`func start`) or deployed
- `curl` installed

## Basic Examples

### Valid Markdown

```bash
curl -X POST http://localhost:7071/api/md_to_pptx/convert \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Title\nBody text"
  }'
```

**Expected Response (200):**

```json
{
  "status": "ok",
  "result": {
    "pptx_base64": "UEsDBBQABgAIAAAAIQD...",
    "size_bytes": 4567
  }
}
```

### Missing Parameter

```bash
curl -X POST http://localhost:7071/api/md_to_pptx/convert \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response (400):**

```json
{
  "status": "error",
  "error": { "msg": "missing 'markdown' parameter" }
}
```

### Invalid JSON

```bash
curl -X POST http://localhost:7071/api/md_to_pptx/convert \
  -H "Content-Type: application/json" \
  -d 'not json'
```

**Response (400):**

```json
{
  "status": "error",
  "error": { "msg": "Invalid JSON in request body" }
}
```

## Production Usage (Azure)

```bash
curl -X POST https://your-app.azurewebsites.net/api/md_to_pptx/convert \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Title"}'
```

### With Function Key

```bash
curl -X POST "https://your-app.azurewebsites.net/api/md_to_pptx/convert?code=YOUR_FUNCTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Title"}'
```

## Notes

- Response always returns `status` and either `result` or `error`.
- PPTX content is base64-encoded; decode to save a file.
- Pandoc must be available in the runtime environment.

## Related Documentation

- [Module Reference](../modules/md_to_pptx.md)
- [Implementation Notes](../implementation/md_to_pptx.md)
