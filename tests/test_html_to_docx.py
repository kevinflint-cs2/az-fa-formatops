"""
Unit tests for html_to_docx module.

Tests business logic in isolation with mocked pypandoc calls.
"""

from unittest.mock import mock_open, patch

import pytest

from functions import html_to_docx


@pytest.mark.mock
def test_handle_request_success():
    """Test successful HTML to DOCX conversion."""
    payload = {"html": "<html><body><h1>Test</h1></body></html>"}

    with patch("functions.html_to_docx._html_to_docx_base64") as mock_convert:
        # Mock base64 output (simulated DOCX)
        mock_convert.return_value = "UEsDBBQABgAIAAAAIQA="

        result = html_to_docx.handle_request(payload)

        # Verify response structure
        assert result["status"] == "ok"
        assert "result" in result
        assert "docx_base64" in result["result"]
        assert "size_bytes" in result["result"]
        assert result["result"]["docx_base64"] == "UEsDBBQABgAIAAAAIQA="
        assert result["result"]["size_bytes"] > 0

        # Verify conversion was called with correct HTML
        mock_convert.assert_called_once_with("<html><body><h1>Test</h1></body></html>")


@pytest.mark.mock
def test_handle_request_missing_html():
    """Test validation when 'html' parameter is missing."""
    payload = {}

    with pytest.raises(ValueError, match="missing 'html' parameter"):
        html_to_docx.handle_request(payload)


@pytest.mark.mock
def test_handle_request_empty_html():
    """Test validation when 'html' parameter is empty."""
    payload = {"html": ""}

    with pytest.raises(ValueError, match="'html' parameter must be a non-empty string"):
        html_to_docx.handle_request(payload)


@pytest.mark.mock
def test_handle_request_invalid_html_type():
    """Test validation when 'html' parameter is not a string."""
    payload = {"html": 123}

    with pytest.raises(ValueError, match="'html' parameter must be a non-empty string"):
        html_to_docx.handle_request(payload)


@pytest.mark.mock
def test_handle_request_conversion_failure():
    """Test error handling when pypandoc conversion fails."""
    payload = {"html": "<html><body><h1>Test</h1></body></html>"}

    with patch("functions.html_to_docx._html_to_docx_base64") as mock_convert:
        # Simulate pypandoc failure
        mock_convert.side_effect = RuntimeError("Pandoc not found")

        with pytest.raises(RuntimeError, match="DOCX conversion failed"):
            html_to_docx.handle_request(payload)


@pytest.mark.mock
def test_html_to_docx_base64_success():
    """Test internal conversion function with mocked pypandoc."""
    html = "<html><body><p>Test content</p></body></html>"

    with (
        patch("pypandoc.get_pandoc_version", return_value="3.1.0"),
        patch("pypandoc.convert_text") as mock_pypandoc,
        patch("builtins.open", mock_open(read_data=b"DOCX_BINARY_DATA")),
        patch("tempfile.TemporaryDirectory") as mock_tmpdir,
    ):
        # Mock temporary directory
        mock_tmpdir.return_value.__enter__.return_value = "/tmp/test"

        result = html_to_docx._html_to_docx_base64(html)

        # Verify pypandoc was called correctly
        mock_pypandoc.assert_called_once()
        call_kwargs = mock_pypandoc.call_args[1]
        assert call_kwargs["to"] == "docx"
        assert call_kwargs["format"] == "html"
        assert "outputfile" in call_kwargs

        # Verify result is base64 encoded
        assert isinstance(result, str)
        assert len(result) > 0

        # Verify it's valid base64 (can decode without error)
        import base64

        decoded = base64.b64decode(result)
        assert decoded == b"DOCX_BINARY_DATA"


@pytest.mark.mock
def test_html_to_docx_base64_pypandoc_error():
    """Test error handling when pypandoc raises an exception."""
    html = "<html><body><p>Test</p></body></html>"

    with (
        patch("pypandoc.get_pandoc_version", return_value="3.1.0"),
        patch("pypandoc.convert_text") as mock_pypandoc,
        patch("tempfile.TemporaryDirectory") as mock_tmpdir,
    ):
        mock_tmpdir.return_value.__enter__.return_value = "/tmp/test"
        mock_pypandoc.side_effect = RuntimeError("Pandoc binary not found")

        with pytest.raises(RuntimeError, match="Pandoc binary not found"):
            html_to_docx._html_to_docx_base64(html)
