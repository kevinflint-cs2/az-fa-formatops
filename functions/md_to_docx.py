"""
md_to_docx.py - Markdown to DOCX conversion module.

Converts Markdown strings to Microsoft Word DOCX format using pypandoc,
returning base64-encoded binary data suitable for JSON transport.
"""

from __future__ import annotations

import base64
import os
import tempfile
from typing import Any


def handle_request(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Handle Markdown to DOCX conversion request.

    Args:
        payload: Dict containing:
            - markdown (str): Markdown content to convert.

    Returns:
        Dict with keys:
            - status: 'ok' or 'error'
            - result: Dict with 'docx_base64' and 'size_bytes' (on success)
            - error: Error details (on failure)

    Raises:
        ValueError: If 'markdown' parameter is missing or empty.
        RuntimeError: If pypandoc conversion fails.
    """

    if "markdown" not in payload:
        raise ValueError("missing 'markdown' parameter")

    markdown_content = payload["markdown"]

    if not markdown_content or not isinstance(markdown_content, str):
        raise ValueError("'markdown' parameter must be a non-empty string")

    try:
        docx_base64 = _markdown_to_docx_base64(markdown_content)
    except Exception as exc:
        raise RuntimeError(f"DOCX conversion failed: {str(exc)}") from exc

    size_bytes = len(docx_base64) * 3 // 4

    return {"status": "ok", "result": {"docx_base64": docx_base64, "size_bytes": size_bytes}}


def _markdown_to_docx_base64(markdown: str) -> str:
    """
    Convert Markdown string to base64-encoded DOCX.

    Uses pypandoc to convert Markdown to DOCX via temporary file, then
    reads the binary output and encodes it as base64.

    Args:
        markdown: Markdown content as string.

    Returns:
        Base64-encoded DOCX file content.

    Raises:
        RuntimeError: If pypandoc conversion fails.
        OSError: If file operations fail.
    """

    import pypandoc

    _ensure_pandoc_available()

    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, "output.docx")

        pypandoc.convert_text(markdown, to="docx", format="md", outputfile=docx_path)

        with open(docx_path, "rb") as docx_file:
            docx_bytes = docx_file.read()

    return base64.b64encode(docx_bytes).decode("utf-8")


def _ensure_pandoc_available() -> None:
    """Ensure pandoc is available without attempting to download at runtime."""

    import pypandoc

    pandoc_path = os.getenv("PYPANDOC_PANDOC")
    if pandoc_path and os.path.exists(pandoc_path):
        return

    try:
        pypandoc.get_pandoc_version()
    except OSError as exc:
        raise RuntimeError(
            "Pandoc binary not found; set PYPANDOC_PANDOC to the installed pandoc path"
        ) from exc
