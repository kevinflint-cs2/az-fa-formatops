"""
Endpoint tests for html_to_docx HTTP route.

Tests the full HTTP request/response cycle against the function app.
"""

import base64
import json

import pytest


@pytest.mark.endpoint
def test_convert_endpoint_success(function_client):
    """Test successful HTML to DOCX conversion via HTTP endpoint."""
    payload = {"html": "<html><body><h1>Test Document</h1><p>This is a test.</p></body></html>"}

    response = function_client.post(
        "/api/html_to_docx/convert", data=json.dumps(payload), content_type="application/json"
    )

    # Verify response status
    assert response.status_code == 200

    # Verify response structure
    data = response.get_json()
    assert data["status"] == "ok"
    assert "result" in data
    assert "docx_base64" in data["result"]
    assert "size_bytes" in data["result"]

    # Verify base64 encoding is valid
    docx_base64 = data["result"]["docx_base64"]
    assert isinstance(docx_base64, str)
    assert len(docx_base64) > 0

    # Verify can decode base64 without error
    decoded = base64.b64decode(docx_base64)
    assert len(decoded) > 0

    # Verify size_bytes is reasonable
    assert data["result"]["size_bytes"] > 0
    assert data["result"]["size_bytes"] < 1000000  # Less than 1MB


@pytest.mark.endpoint
def test_convert_endpoint_missing_html(function_client):
    """Test error response when 'html' parameter is missing."""
    payload = {}

    response = function_client.post(
        "/api/html_to_docx/convert", data=json.dumps(payload), content_type="application/json"
    )

    # Verify error response
    assert response.status_code == 400

    data = response.get_json()
    assert data["status"] == "error"
    assert "error" in data
    assert "msg" in data["error"]
    assert "missing 'html' parameter" in data["error"]["msg"]


@pytest.mark.endpoint
def test_convert_endpoint_empty_html(function_client):
    """Test error response when 'html' parameter is empty."""
    payload = {"html": ""}

    response = function_client.post(
        "/api/html_to_docx/convert", data=json.dumps(payload), content_type="application/json"
    )

    # Verify error response
    assert response.status_code == 400

    data = response.get_json()
    assert data["status"] == "error"
    assert "error" in data
    assert "non-empty string" in data["error"]["msg"]


@pytest.mark.endpoint
def test_convert_endpoint_invalid_json(function_client):
    """Test error response when request body is not valid JSON."""
    response = function_client.post(
        "/api/html_to_docx/convert", data="not valid json", content_type="application/json"
    )

    # Verify error response
    assert response.status_code == 400

    data = response.get_json()
    assert data["status"] == "error"
    assert "error" in data
    assert "Invalid JSON" in data["error"]["msg"]


@pytest.mark.endpoint
def test_convert_endpoint_empty_body(function_client):
    """Test error response when request body is empty."""
    response = function_client.post(
        "/api/html_to_docx/convert", data="", content_type="application/json"
    )

    # Verify error response
    assert response.status_code == 400

    data = response.get_json()
    assert data["status"] == "error"


@pytest.mark.endpoint
def test_convert_endpoint_complex_html(function_client):
    """Test conversion with more complex HTML structure."""
    payload = {
        "html": """
        <html>
        <head><title>Test Document</title></head>
        <body>
            <h1>Main Title</h1>
            <h2>Subtitle</h2>
            <p>This is a paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
            <table>
                <tr><th>Header 1</th><th>Header 2</th></tr>
                <tr><td>Data 1</td><td>Data 2</td></tr>
            </table>
        </body>
        </html>
        """
    }

    response = function_client.post(
        "/api/html_to_docx/convert", data=json.dumps(payload), content_type="application/json"
    )

    # Verify successful conversion
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "ok"
    assert "docx_base64" in data["result"]

    # More complex HTML should produce larger output
    assert data["result"]["size_bytes"] > 1000
