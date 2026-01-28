# YAML Checker Implementation

## Overview

The YAML checker provides an HTTP endpoint that validates YAML content strings using ruamel.yaml. It returns a simple JSON result indicating validity and, on failure, the first parser issue with a 1-based line number.

## Feature Description

- **Module:** `functions/yaml_checker.py`
- **Endpoint:** `/api/yaml/validate`
- **Purpose:** Quickly assess whether provided YAML is syntactically valid and surface the first issue when invalid.

## Implementation Details

### Module: `functions/yaml_checker.py`

**Key Function:**
- `handle_request(payload: dict[str, Any]) -> dict[str, Any]` — validates YAML content and returns `valid` plus `issues` list.

**Input Schema:**
```json
{
  "yaml": "foo: bar\nlist:\n  - one"
}
```

**Output Schema (valid):**
```json
{
  "valid": true,
  "issues": []
}
```

**Output Schema (invalid):**
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

### HTTP Route: `/api/yaml/validate`

**Method:** POST  
**Content-Type:** application/json

**Error Handling:**
- `400 Bad Request` — invalid JSON, missing `yaml`, or empty string
- `200 OK` — validation result (both valid and invalid YAML)
- `500 Internal Server Error` — unexpected errors

### Design Decisions

1. **Safe Loader:** Use `YAML(typ="safe")` to avoid executing arbitrary YAML tags.
2. **First Error Only (MVP):** Return the first parser error with 1-based line number for quick feedback.
3. **Consistent Response:** Always return `valid`/`issues` on successful request parsing; reserve 400 for malformed requests.

### Dependencies

- `ruamel.yaml` for parsing and error metadata.

### Security Considerations

- Safe loading prevents execution of arbitrary YAML tags.
- No external network calls; validation is local to the function runtime.

### Testing Strategy

**Unit Tests (`tests/test_yaml_checker.py`, marker `mock`):**
- Valid YAML returns `valid: true`
- Invalid YAML returns `valid: false` with line number
- Missing/empty/non-string `yaml` raises `ValueError`

**Endpoint Tests (`tests/test_yaml_checker_endpoint.py`, marker `endpoint`):**
- Valid payload returns 200 with `valid: true`
- Invalid YAML returns 200 with `valid: false` and issue details
- Missing `yaml` or bad JSON returns 400

### Known Limitations

- Reports only the first parse error (no multi-issue aggregation)
- Does not perform schema validation
- Column numbers are not included

## Implementation Date

January 28, 2026

## Author

GitHub Copilot (AI Agent)
