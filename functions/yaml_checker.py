"""
yaml_checker.py - Validate YAML content strings.

Validates provided YAML text using ruamel.yaml and reports whether the
content is valid. On parse failures, returns the first issue with a
1-based line number to help users quickly locate the problem.
"""

from __future__ import annotations

from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


def handle_request(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Validate a YAML string and return issues if parsing fails.

    Args:
        payload: Dict containing:
            - yaml (str): YAML content to validate.

    Returns:
        Dict with keys:
            - valid: True when the YAML is syntactically valid, else False.
            - issues: List of issue dictionaries with keys 'line' and 'issue'.

    Raises:
        ValueError: If the required 'yaml' parameter is missing or empty.
    """

    if "yaml" not in payload:
        raise ValueError("missing 'yaml' parameter")

    yaml_text = payload["yaml"]
    if not isinstance(yaml_text, str) or not yaml_text.strip():
        raise ValueError("'yaml' parameter must be a non-empty string")

    parser = YAML(typ="safe")

    try:
        parser.load(yaml_text)
    except YAMLError as exc:  # YAML syntax error encountered
        issue = _parse_yaml_error(exc)
        return {"valid": False, "issues": [issue]}

    return {"valid": True, "issues": []}


def _parse_yaml_error(error: YAMLError) -> dict[str, Any]:
    """Extract line number and message from a ruamel.yaml error."""

    line_number = None
    message = str(error)

    mark = getattr(error, "problem_mark", None)
    if mark is not None and getattr(mark, "line", None) is not None:
        # Convert 0-based line to 1-based line for user clarity
        line_number = int(mark.line) + 1

    problem = getattr(error, "problem", None)
    if isinstance(problem, str) and problem:
        message = problem

    return {
        "line": line_number if line_number is not None else 1,
        "issue": message,
    }
