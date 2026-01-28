# Markdown to DOCX Implementation

## Overview

Provides an HTTP endpoint that converts Markdown content to DOCX using pypandoc. Returns base64-encoded output with size metadata.

## Details

- **Module:** `functions/md_to_docx.py`
- **Endpoint:** `/api/md_to_docx/convert`
- **Method:** POST (`application/json`)

### Input Schema

```json
{
  "markdown": "# Title\nBody text"
}
```

### Output Schema (success)

```json
{
  "status": "ok",
  "result": {
    "docx_base64": "UEsDBBQABgAIAAAAIQD...",
    "size_bytes": 4567
  }
}
```

### Error Handling

- 400: Missing or empty `markdown`, invalid JSON
- 500: Conversion/runtime errors

### Design Decisions

1. **Pypandoc + Pandoc binary** for consistent conversions (aligns with html_to_docx).
2. **Temporary file output** to capture binary DOCX then base64-encode.
3. **First-class validation**: non-empty string required for `markdown`.
4. **Size hint**: `size_bytes` approximated from base64 length.

### Dependencies

- `pypandoc` (Pandoc binary required)

### Security Considerations

- Conversion is local; no external calls.
- Input treated as text; ensure upstream callers trust content.

### Testing

- Unit tests (`tests/test_md_to_docx.py`, marker `mock`): validation, success path, conversion error.
- Endpoint tests (`tests/test_md_to_docx_endpoint.py`, marker `endpoint`): success, missing field, invalid JSON.

### Known Limitations

- Requires Pandoc binary in runtime.
- No custom template/theme support in MVP.

## Implementation Date

January 28, 2026

## Author

GitHub Copilot (AI Agent)
