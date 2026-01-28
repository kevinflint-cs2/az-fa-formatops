"""
Unit tests for md_to_pptx module.

Tests business logic in isolation with mocked pypandoc calls.
"""

from unittest.mock import mock_open, patch

import pytest

from functions import md_to_pptx


@pytest.mark.mock
def test_handle_request_success():
    payload = {"markdown": "# Title\nBody"}

    with patch("functions.md_to_pptx._markdown_to_pptx_base64") as mock_convert:
        mock_convert.return_value = "UEsDBBQABgAIAAAAIQA="

        result = md_to_pptx.handle_request(payload)

        assert result["status"] == "ok"
        assert result["result"]["pptx_base64"] == "UEsDBBQABgAIAAAAIQA="
        assert result["result"]["size_bytes"] > 0
        mock_convert.assert_called_once_with("# Title\nBody")


@pytest.mark.mock
def test_handle_request_missing_markdown():
    payload = {}

    with pytest.raises(ValueError, match="missing 'markdown' parameter"):
        md_to_pptx.handle_request(payload)


@pytest.mark.mock
def test_handle_request_empty_markdown():
    payload = {"markdown": ""}

    with pytest.raises(ValueError, match="non-empty string"):
        md_to_pptx.handle_request(payload)


@pytest.mark.mock
def test_handle_request_non_string_markdown():
    payload = {"markdown": 123}

    with pytest.raises(ValueError, match="non-empty string"):
        md_to_pptx.handle_request(payload)


@pytest.mark.mock
def test_handle_request_conversion_failure():
    payload = {"markdown": "# Title"}

    with patch("functions.md_to_pptx._markdown_to_pptx_base64") as mock_convert:
        mock_convert.side_effect = RuntimeError("Pandoc not found")

        with pytest.raises(RuntimeError, match="PPTX conversion failed"):
            md_to_pptx.handle_request(payload)


@pytest.mark.mock
def test_markdown_to_pptx_base64_success():
    markdown = "# Title\nBody"

    with (
        patch("pypandoc.get_pandoc_version", return_value="3.1.0"),
        patch("pypandoc.convert_text") as mock_convert,
        patch("builtins.open", mock_open(read_data=b"PPTX_DATA")),
        patch("tempfile.TemporaryDirectory") as mock_tmpdir,
    ):
        mock_tmpdir.return_value.__enter__.return_value = "/tmp/test"

        result = md_to_pptx._markdown_to_pptx_base64(markdown)

        mock_convert.assert_called_once()
        kwargs = mock_convert.call_args.kwargs
        assert kwargs["to"] == "pptx"
        assert kwargs["format"] == "md"
        assert "outputfile" in kwargs

        import base64

        decoded = base64.b64decode(result)
        assert decoded == b"PPTX_DATA"


@pytest.mark.mock
def test_markdown_to_pptx_base64_pandoc_error():
    markdown = "# Title"

    with (
        patch("pypandoc.get_pandoc_version", return_value="3.1.0"),
        patch("pypandoc.convert_text") as mock_convert,
        patch("tempfile.TemporaryDirectory") as mock_tmpdir,
    ):
        mock_tmpdir.return_value.__enter__.return_value = "/tmp/test"
        mock_convert.side_effect = RuntimeError("Pandoc missing")

        with pytest.raises(RuntimeError, match="Pandoc missing"):
            md_to_pptx._markdown_to_pptx_base64(markdown)
