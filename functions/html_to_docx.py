"""
html_to_docx.py - HTML to DOCX conversion module

Converts HTML strings to Microsoft Word DOCX format using pypandoc,
returning base64-encoded binary data suitable for JSON transport.
"""

import base64
import os
import tempfile
from typing import Any


def handle_request(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Handle HTML to DOCX conversion request.

    Args:
        payload: Dict containing:
            - html (str): HTML content to convert

    Returns:
        Dict with keys:
            - status: 'ok' or 'error'
            - result: Dict with 'docx_base64' and 'size_bytes' (on success)
            - error: Error details (on failure)

    Raises:
        ValueError: If 'html' parameter is missing or empty
        RuntimeError: If pypandoc conversion fails
    """
    # Validate required parameter
    if "html" not in payload:
        raise ValueError("missing 'html' parameter")

    html_content = payload["html"]

    # Validate non-empty HTML
    if not html_content or not isinstance(html_content, str):
        raise ValueError("'html' parameter must be a non-empty string")

    # Convert HTML to DOCX
    try:
        docx_base64 = _html_to_docx_base64(html_content)
    except Exception as e:
        raise RuntimeError(f"DOCX conversion failed: {str(e)}") from e

    # Calculate size of base64 string (approximation of binary size)
    # Actual binary size = len(base64_string) * 3/4 (accounting for padding)
    size_bytes = len(docx_base64) * 3 // 4

    return {"status": "ok", "result": {"docx_base64": docx_base64, "size_bytes": size_bytes}}


def _html_to_docx_base64(html: str) -> str:
    """
    Convert HTML string to base64-encoded DOCX.

    Uses pypandoc to convert HTML to DOCX format via temporary file,
    then encodes the binary DOCX as base64 for JSON transport.

    Args:
        html: HTML content as string

    Returns:
        Base64-encoded DOCX file content

    Raises:
        RuntimeError: If pypandoc conversion fails
        OSError: If file operations fail
    """
    import pypandoc

    # Ensure pandoc is available (download if needed)
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        # Pandoc not found, download it
        pypandoc.download_pandoc(targetfolder="/tmp/pandoc")
        os.environ.setdefault("PYPANDOC_PANDOC", "/tmp/pandoc/pandoc")

    # Use temporary directory for file operations (auto-cleanup)
    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, "output.docx")

        # Convert HTML to DOCX using pypandoc
        pypandoc.convert_text(html, to="docx", format="html", outputfile=docx_path)

        # Read binary DOCX file
        with open(docx_path, "rb") as f:
            docx_bytes = f.read()

    # Encode as base64 string
    return base64.b64encode(docx_bytes).decode("utf-8")
