"""
Endpoint tests for YAML validation route.
"""

import json

import pytest


@pytest.mark.endpoint
def test_yaml_validate_success(function_client):
    payload = {"yaml": "foo: bar\nlist:\n  - one"}

    response = function_client.post(
        "/api/yaml/validate", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["valid"] is True
    assert data["issues"] == []


@pytest.mark.endpoint
def test_yaml_validate_invalid_yaml(function_client):
    payload = {"yaml": "foo: bar: baz"}

    response = function_client.post(
        "/api/yaml/validate", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["valid"] is False
    assert len(data["issues"]) == 1
    issue = data["issues"][0]
    assert issue["line"] == 1
    assert isinstance(issue["issue"], str)


@pytest.mark.endpoint
def test_yaml_validate_missing_payload(function_client):
    payload = {}

    response = function_client.post(
        "/api/yaml/validate", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "missing 'yaml'" in data["error"]["msg"]


@pytest.mark.endpoint
def test_yaml_validate_invalid_json(function_client):
    response = function_client.post(
        "/api/yaml/validate", data="not json", content_type="application/json"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "Invalid JSON" in data["error"]["msg"]
