"""
md_to_pptx.py - Markdown to PPTX conversion module.

Converts Markdown strings to PowerPoint PPTX format using pypandoc,
returning base64-encoded binary data suitable for JSON transport.
"""

from __future__ import annotations

import base64
import os
import tempfile
from typing import Any


def handle_request(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Handle Markdown to PPTX conversion request.

    Args:
        payload: Dict containing:
            - markdown (str): Markdown content to convert.

    Returns:
        Dict with keys:
            - status: 'ok' or 'error'
            - result: Dict with 'pptx_base64' and 'size_bytes' (on success)
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
        pptx_base64 = _markdown_to_pptx_base64(markdown_content)
    except Exception as exc:
        raise RuntimeError(f"PPTX conversion failed: {str(exc)}") from exc

    size_bytes = len(pptx_base64) * 3 // 4

    return {"status": "ok", "result": {"pptx_base64": pptx_base64, "size_bytes": size_bytes}}


def _markdown_to_pptx_base64(markdown: str) -> str:
    """
    Convert Markdown string to base64-encoded PPTX.

    Uses pypandoc to convert Markdown to PPTX via temporary file, then
    reads the binary output and encodes it as base64.

    Args:
        markdown: Markdown content as string.

    Returns:
        Base64-encoded PPTX file content.

    Raises:
        RuntimeError: If pypandoc conversion fails.
        OSError: If file operations fail.
    """

    import pypandoc

    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc(targetfolder="/tmp/pandoc")
        os.environ.setdefault("PYPANDOC_PANDOC", "/tmp/pandoc/pandoc")

    with tempfile.TemporaryDirectory() as tmpdir:
        pptx_path = os.path.join(tmpdir, "output.pptx")

        pypandoc.convert_text(markdown, to="pptx", format="md", outputfile=pptx_path)

        with open(pptx_path, "rb") as pptx_file:
            pptx_bytes = pptx_file.read()

    return base64.b64encode(pptx_bytes).decode("utf-8")
