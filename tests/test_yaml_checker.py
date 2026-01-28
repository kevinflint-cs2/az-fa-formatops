"""
Unit tests for yaml_checker module.

Tests business logic without HTTP routing.
"""

import pytest

from functions import yaml_checker


@pytest.mark.mock
def test_handle_request_valid_yaml():
    payload = {"yaml": "foo: bar\nitems:\n  - one\n  - two"}

    result = yaml_checker.handle_request(payload)

    assert result["valid"] is True
    assert result["issues"] == []


@pytest.mark.mock
def test_handle_request_invalid_yaml_reports_line():
    payload = {"yaml": "foo: bar: baz"}

    result = yaml_checker.handle_request(payload)

    assert result["valid"] is False
    assert len(result["issues"]) == 1
    issue = result["issues"][0]
    assert issue["line"] == 1
    assert isinstance(issue["issue"], str)
    assert len(issue["issue"]) > 0


@pytest.mark.mock
def test_handle_request_missing_yaml():
    payload = {}

    with pytest.raises(ValueError, match="missing 'yaml' parameter"):
        yaml_checker.handle_request(payload)


@pytest.mark.mock
def test_handle_request_empty_yaml():
    payload = {"yaml": "   "}

    with pytest.raises(ValueError, match="non-empty string"):
        yaml_checker.handle_request(payload)


@pytest.mark.mock
def test_handle_request_non_string_yaml():
    payload = {"yaml": 123}

    with pytest.raises(ValueError, match="non-empty string"):
        yaml_checker.handle_request(payload)
