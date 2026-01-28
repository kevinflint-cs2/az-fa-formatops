# YAML Checker - curl Examples

This document provides curl examples for validating YAML content via the `/api/yaml/validate` endpoint.

## Prerequisites

- Function app running locally (`func start`) or deployed to Azure
- `curl` installed

## Basic Examples

### Valid YAML

```bash
curl -X POST http://localhost:7071/api/yaml/validate \
  -H "Content-Type: application/json" \
  -d '{
    "yaml": "foo: bar\nlist:\n  - one\n  - two"
  }'
```

**Expected Response (200):**

```json
{
  "valid": true,
  "issues": []
}
```

### Invalid YAML

```bash
curl -X POST http://localhost:7071/api/yaml/validate \
  -H "Content-Type: application/json" \
  -d '{
    "yaml": "foo: bar: baz"
  }'
```

**Expected Response (200):**

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

### Missing Parameter

```bash
curl -X POST http://localhost:7071/api/yaml/validate \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response (400):**

```json
{
  "status": "error",
  "error": {
    "msg": "missing 'yaml' parameter"
  }
}
```

## Production Usage (Azure)

```bash
curl -X POST https://your-app.azurewebsites.net/api/yaml/validate \
  -H "Content-Type: application/json" \
  -d '{"yaml": "foo: bar"}'
```

### With Function Key (if required)

```bash
curl -X POST "https://your-app.azurewebsites.net/api/yaml/validate?code=YOUR_FUNCTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"yaml": "foo: bar"}'
```

## Notes

- Endpoint always returns HTTP 200 for validation results; request parsing errors return 400.
- Replace `localhost:7071` with your function URL when deployed.
- The response reports the first parser error only (MVP).

## Related Documentation

- [Module Reference](../modules/yaml_checker.md)
- [Implementation Notes](../implementation/yaml_checker.md)
