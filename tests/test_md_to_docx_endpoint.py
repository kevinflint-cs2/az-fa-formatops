"""
Endpoint tests for md_to_docx HTTP route.
"""

import base64
import json

import pytest


@pytest.mark.endpoint
def test_md_to_docx_success(function_client):
    payload = {"markdown": "# Title\nBody"}

    response = function_client.post(
        "/api/md_to_docx/convert", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "docx_base64" in data["result"]
    assert "size_bytes" in data["result"]

    decoded = base64.b64decode(data["result"]["docx_base64"])
    assert len(decoded) > 0
    assert data["result"]["size_bytes"] > 0


@pytest.mark.endpoint
def test_md_to_docx_missing_markdown(function_client):
    payload = {}

    response = function_client.post(
        "/api/md_to_docx/convert", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "missing 'markdown'" in data["error"]["msg"]


@pytest.mark.endpoint
def test_md_to_docx_invalid_json(function_client):
    response = function_client.post(
        "/api/md_to_docx/convert", data="not json", content_type="application/json"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "Invalid JSON" in data["error"]["msg"]
