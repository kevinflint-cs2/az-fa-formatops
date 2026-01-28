# YAML Checker Module

## Overview

The `yaml_checker` module validates YAML content strings using ruamel.yaml and returns whether the document is syntactically valid. When invalid, it reports the first issue with a 1-based line number for quick debugging.

## HTTP Endpoint

**Route:** `/api/yaml/validate`  
**Method:** `POST`  
**Content-Type:** `application/json`

## Request Format

```json
{
  "yaml": "foo: bar\nlist:\n  - one"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `yaml` | string | Yes | YAML content to validate |

## Response Format

### Success Response (200, valid YAML)

```json
{
  "valid": true,
  "issues": []
}
```

### Success Response (200, invalid YAML)

```json
{
  "valid": false,
  "issues": [
    {
      "line": 1,
      "issue": "mapping values are not allowed here"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `valid` | boolean | `true` when YAML parsed successfully; otherwise `false` |
| `issues` | array | List of issues (first parser error) with `line` and `issue` |

### Error Response (400)

```json
{
  "status": "error",
  "error": {
    "msg": "missing 'yaml' parameter"
  }
}
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Validation completed; result in `valid`/`issues` |
| 400 | Invalid request body (missing/empty `yaml`, invalid JSON) |
| 500 | Unexpected server error |

## Functions

### `handle_request(payload: dict[str, Any]) -> dict[str, Any]`

Validates YAML content and returns a result indicating validity and issues.

**Parameters:**
- `payload` (dict): Contains the `yaml` string to validate

**Returns:**
- Dict with `valid` and `issues`

**Raises:**
- `ValueError`: If `yaml` parameter is missing or empty

**Example:**

```python
from functions import yaml_checker

payload = {"yaml": "foo: bar\nlist:\n  - one"}
result = yaml_checker.handle_request(payload)

print(result["valid"])   # True or False
print(result["issues"])  # [] or list of issues
```

## Dependencies

- `ruamel.yaml` - YAML parser used for safe validation

## Usage Examples

See [yaml_checker-curl.md](../examples/yaml_checker-curl.md) for curl examples.

## Error Handling

- Input validation for missing or empty `yaml` field
- Returns first parser error with 1-based line number for clarity
- Wraps request parsing errors in HTTP layer as 400 responses

## Security Considerations

- Uses safe loader (`typ="safe"`) to avoid executing arbitrary YAML tags
- No external network calls; validation happens in-process

## Limitations

- Reports only the first parse error (MVP scope)
- Does not perform schema validation

## Future Enhancements

- Collect multiple issues instead of first error only
- Optional schema validation support
- Include column numbers in issue details

## Related Documentation

- [Implementation Notes](../implementation/yaml_checker.md)
- [Usage Examples](../examples/yaml_checker-curl.md)
