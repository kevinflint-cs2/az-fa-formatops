# HTML to DOCX Conversion - curl Examples

This document provides practical examples for using the HTML to DOCX conversion endpoint with curl.

## Prerequisites

- Function app running locally or deployed to Azure
- `curl` command-line tool installed
- `base64` utility for decoding output

## Basic Examples

### Simple HTML Conversion

Convert basic HTML to DOCX:

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello World</h1><p>This is a test document.</p></body></html>"
  }'
```

**Expected Response:**

```json
{
  "status": "ok",
  "result": {
    "docx_base64": "UEsDBBQABgAIAAAAIQD...",
    "size_bytes": 4567
  }
}
```

### Complex HTML Document

Convert HTML with multiple elements:

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><head><title>Report</title></head><body><h1>Annual Report</h1><h2>Executive Summary</h2><p>This report summarizes <strong>key findings</strong> from the year.</p><ul><li>Revenue increased by 20%</li><li>Customer satisfaction improved</li><li>New markets entered</li></ul><h2>Details</h2><table><tr><th>Quarter</th><th>Revenue</th></tr><tr><td>Q1</td><td>$1M</td></tr><tr><td>Q2</td><td>$1.2M</td></tr></table></body></html>"
  }'
```

### HTML from File

Convert HTML content from a file:

```bash
# Create HTML file
cat > sample.html <<'EOF'
<html>
<head><title>Sample Document</title></head>
<body>
  <h1>Sample Document</h1>
  <p>This is a paragraph with <em>emphasis</em> and <strong>strong</strong> text.</p>
  <ol>
    <li>First item</li>
    <li>Second item</li>
    <li>Third item</li>
  </ol>
</body>
</html>
EOF

# Convert using jq to properly escape JSON
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg html "$(cat sample.html)" '{html: $html}')"
```

## Saving DOCX Output

### Extract and Decode Base64

Save the converted DOCX to a file:

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Test</h1></body></html>"}' \
  | jq -r '.result.docx_base64' \
  | base64 -d > output.docx
```

### One-Liner with Verification

Convert and verify the output file:

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>My Document</h1><p>Content here</p></body></html>"}' \
  | jq -r '.result.docx_base64' \
  | base64 -d > output.docx \
  && file output.docx \
  && ls -lh output.docx
```

**Expected Output:**

```
output.docx: Microsoft Word 2007+
-rw-r--r-- 1 user user 4.5K Nov 17 10:30 output.docx
```

## Error Handling Examples

### Missing HTML Parameter

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response (400):**

```json
{
  "status": "error",
  "error": {
    "msg": "missing 'html' parameter"
  }
}
```

### Empty HTML String

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": ""}'
```

**Response (400):**

```json
{
  "status": "error",
  "error": {
    "msg": "'html' parameter must be a non-empty string"
  }
}
```

### Invalid JSON

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d 'not valid json'
```

**Response (400):**

```json
{
  "status": "error",
  "error": {
    "msg": "Invalid JSON in request body"
  }
}
```

## Production Usage (Azure)

### Azure Functions Endpoint

```bash
curl -X POST https://your-app.azurewebsites.net/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Production Test</h1></body></html>"}'
```

### With Function Key (if required)

```bash
curl -X POST https://your-app.azurewebsites.net/api/html_to_docx/convert?code=YOUR_FUNCTION_KEY \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Secure Request</h1></body></html>"}'
```

## Advanced Examples

### Batch Processing Multiple Files

Convert multiple HTML files:

```bash
for file in *.html; do
  echo "Converting $file..."
  curl -X POST http://localhost:7071/api/html_to_docx/convert \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg html "$(cat "$file")" '{html: $html}')" \
    | jq -r '.result.docx_base64' \
    | base64 -d > "${file%.html}.docx"
done
```

### Check Response Status

```bash
response=$(curl -s -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Test</h1></body></html>"}')

status=$(echo "$response" | jq -r '.status')

if [ "$status" = "ok" ]; then
  echo "Success! Size: $(echo "$response" | jq -r '.result.size_bytes') bytes"
  echo "$response" | jq -r '.result.docx_base64' | base64 -d > output.docx
else
  echo "Error: $(echo "$response" | jq -r '.error.msg')"
fi
```

### Verbose Output with Timing

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Test</h1></body></html>"}' \
  -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -o response.json

cat response.json | jq .
```

## Troubleshooting

### Check if Endpoint is Available

```bash
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body>test</body></html>"}' \
  -w "\nHTTP Status: %{http_code}\n"
```

### Validate DOCX Output

```bash
# Convert and validate
curl -X POST http://localhost:7071/api/html_to_docx/convert \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Validation Test</h1></body></html>"}' \
  | jq -r '.result.docx_base64' \
  | base64 -d > test.docx

# Check file type
file test.docx

# Check file size
ls -lh test.docx

# Try to open (macOS)
open test.docx

# Try to open (Linux)
libreoffice test.docx
```

## Notes

- All examples use `http://localhost:7071` for local testing. Replace with your Azure Function URL for production.
- The `jq` tool is used for JSON processing. Install with `apt-get install jq` (Linux) or `brew install jq` (macOS).
- Base64 decoding may differ slightly between systems. Use `base64 -D` on macOS instead of `base64 -d`.
- Ensure Pandoc is installed in your runtime environment for conversions to work.

## Related Documentation

- [Module Reference](../modules/html_to_docx.md)
- [Implementation Notes](../implementation/html_to_docx.md)
