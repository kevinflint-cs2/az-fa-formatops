# HTML to DOCX Conversion Implementation

## Overview

This document describes the implementation of the HTML-to-DOCX conversion endpoint for the Azure Functions app.

## Feature Description

The `html_to_docx` module provides an HTTP endpoint that accepts HTML content and converts it to a Microsoft Word DOCX format, returning the result as a base64-encoded string.

## Implementation Details

### Module: `functions/html_to_docx.py`

**Purpose:** Convert HTML strings to DOCX format using pypandoc.

**Key Functions:**
- `handle_request(payload: Dict[str, Any]) -> Dict[str, Any]` - Main entry point for request handling
- `_html_to_docx_base64(html: str) -> str` - Internal conversion function using pypandoc

**Input Schema:**
```json
{
  "html": "<html><body><h1>Title</h1><p>Content</p></body></html>"
}
```

**Output Schema:**
```json
{
  "status": "ok",
  "result": {
    "docx_base64": "UEsDBBQABgAIAAAA...",
    "size_bytes": 4567
  }
}
```

### HTTP Route: `/api/html_to_docx/convert`

**Method:** POST  
**Content-Type:** application/json

**Error Handling:**
- `400 Bad Request` - Missing or invalid HTML input
- `500 Internal Server Error` - Conversion failure or pypandoc errors

### Design Decisions

1. **Base64 Encoding:** DOCX files are binary; base64 encoding allows JSON transport
2. **Temporary Files:** pypandoc requires file I/O; using `tempfile.TemporaryDirectory()` ensures automatic cleanup
3. **POST-only:** HTML content can be large; POST body is more appropriate than query parameters
4. **Size Metadata:** Return file size to help clients validate conversion

### Dependencies

**Python Packages:**
- `pypandoc>=1.13` - Python wrapper for Pandoc document converter

**System Dependencies:**
- Pandoc binary (required by pypandoc)
  - Local development: Install via package manager (`apt-get install pandoc`, `brew install pandoc`)
  - Azure deployment: Requires custom runtime or container with Pandoc pre-installed

### Security Considerations

**Input Validation:**
- Reject missing `html` field
- Reject empty HTML strings
- Future enhancement: Add HTML size limits to prevent abuse

**Resource Management:**
- Temporary files automatically cleaned up via context manager
- Pypandoc timeout prevents hanging conversions

**Error Sanitization:**
- Exception messages don't expose internal file paths
- Generic error messages for unexpected failures

### Testing Strategy

**Unit Tests (`test_html_to_docx.py`):**
- Mock pypandoc to avoid file I/O during tests
- Test valid HTML conversion
- Test missing/empty HTML validation
- Test pypandoc error propagation
- Marker: `@pytest.mark.mock`

**Endpoint Tests (`test_html_to_docx_endpoint.py`):**
- Integration tests against running function app
- Test full HTTP request/response cycle
- Test error responses (400, 500)
- Marker: `@pytest.mark.endpoint`

### Deployment Requirements

**Local Development:**
1. Install Pandoc: `apt-get install pandoc` (Linux) or `brew install pandoc` (macOS)
2. Install Python dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest -m mock -vv`

**Azure Deployment:**
1. Requires Azure Functions runtime with Pandoc installed
2. Options:
   - Custom Docker container with Pandoc
   - Azure Functions Premium plan with custom runtime
   - Manual installation via Kudu console (not recommended for production)

### Known Limitations

1. **Pandoc Dependency:** Not available in default Azure Functions runtime
2. **File I/O Overhead:** Temporary file creation adds latency (~100-500ms)
3. **Format Support:** Currently only HTML → DOCX; could be extended to other formats

### Future Enhancements

- Add input size limits (e.g., max 5MB HTML)
- Support additional input formats (Markdown, plain text)
- Support additional output formats (PDF, ODT)
- Add conversion options (page size, margins, fonts)
- Implement caching for repeated conversions

## Implementation Date

November 17, 2025

## Author

GitHub Copilot (AI Agent)
