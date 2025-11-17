# HTML to DOCX Module

## Overview

The `html_to_docx` module provides functionality to convert HTML content into Microsoft Word DOCX format, returning the result as a base64-encoded string suitable for JSON transport.

## HTTP Endpoint

**Route:** `/api/html_to_docx/convert`  
**Method:** `POST`  
**Content-Type:** `application/json`

## Request Format

```json
{
  "html": "<html><body><h1>Title</h1><p>Content goes here</p></body></html>"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `html` | string | Yes | HTML content to convert to DOCX format |

## Response Format

### Success Response (200)

```json
{
  "status": "ok",
  "result": {
    "docx_base64": "UEsDBBQABgAIAAAAIQD...",
    "size_bytes": 4567
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Always "ok" for successful conversions |
| `result.docx_base64` | string | Base64-encoded DOCX file content |
| `result.size_bytes` | integer | Approximate size of the DOCX file in bytes |

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
| `status` | string | Always "error" for failed conversions |
| `error.msg` | string | Human-readable error message |

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Conversion successful |
| 400 | Invalid or missing input (e.g., missing `html` parameter) |
| 500 | Internal server error (e.g., pypandoc/Pandoc failure) |

## Functions

### `handle_request(payload: Dict[str, Any]) -> Dict[str, Any]`

Main entry point for HTML to DOCX conversion.

**Parameters:**
- `payload` (dict): Dictionary containing the `html` key with HTML content

**Returns:**
- Dictionary with `status`, `result` or `error` keys

**Raises:**
- `ValueError`: If `html` parameter is missing or invalid
- `RuntimeError`: If pypandoc conversion fails

**Example:**

```python
from functions import html_to_docx

payload = {"html": "<html><body><h1>Test</h1></body></html>"}
result = html_to_docx.handle_request(payload)

print(result["result"]["docx_base64"])  # Base64-encoded DOCX
print(result["result"]["size_bytes"])    # File size
```

### `_html_to_docx_base64(html: str) -> str`

Internal function to convert HTML to base64-encoded DOCX.

**Parameters:**
- `html` (str): HTML content as string

**Returns:**
- Base64-encoded DOCX file content

**Raises:**
- `RuntimeError`: If pypandoc conversion fails
- `OSError`: If file operations fail

## Dependencies

**Python Packages:**
- `pypandoc>=1.13` - Python wrapper for Pandoc

**System Requirements:**
- Pandoc binary must be installed in the runtime environment
  - Local: `apt-get install pandoc` (Linux) or `brew install pandoc` (macOS)
  - Azure: Requires custom runtime with Pandoc pre-installed

## Usage Examples

See [html_to_docx-curl.md](../examples/html_to_docx-curl.md) for complete curl examples.

### Basic Conversion

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Hello World</h1></body></html>"}'
```

### Decoding Base64 Output

```bash
# Save base64 output to file
echo "UEsDBBQABgAI..." | base64 -d > output.docx
```

## Error Handling

The module implements comprehensive error handling:

1. **Input Validation:** Checks for missing or empty `html` parameter
2. **Type Validation:** Ensures `html` is a string
3. **Conversion Errors:** Catches and reports pypandoc/Pandoc failures
4. **Resource Cleanup:** Automatically cleans up temporary files

## Security Considerations

- **Input Validation:** Validates all input parameters
- **Resource Management:** Uses temporary files with automatic cleanup
- **Error Sanitization:** Doesn't expose internal file paths in errors

## Limitations

- Requires Pandoc binary in runtime environment
- File I/O adds latency (~100-500ms per conversion)
- Currently supports only HTML input format
- No caching implemented

## Future Enhancements

- Add input size limits to prevent abuse
- Support additional input formats (Markdown, plain text)
- Support additional output formats (PDF, ODT)
- Implement conversion caching
- Add custom styling options

## Related Documentation

- [Implementation Notes](../implementation/html_to_docx.md)
- [Usage Examples](../examples/html_to_docx-curl.md)
