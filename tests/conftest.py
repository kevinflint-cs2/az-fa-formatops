"""Pytest configuration and fixtures for testing."""

import pytest


def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "mock: Unit tests with mocked dependencies (fast)")
    config.addinivalue_line("markers", "endpoint: HTTP endpoint integration tests")
    config.addinivalue_line("markers", "live: Live API tests (requires credentials)")


@pytest.fixture
def function_client():
    """
    Provide a test client for Azure Functions endpoint testing.

    Note: This fixture requires the function app to be running.
    Start with: func start
    """
    import requests

    class FunctionClient:
        """Simple client for testing Azure Functions endpoints."""

        def __init__(self, base_url="http://localhost:7071"):
            self.base_url = base_url

        def post(self, path, data=None, content_type="application/json"):
            """Make POST request to function endpoint."""
            url = f"{self.base_url}{path}"
            headers = {"Content-Type": content_type} if content_type else {}

            response = requests.post(url, data=data, headers=headers, timeout=30)

            # Create response object that mimics Flask test client
            class Response:
                def __init__(self, resp):
                    self.status_code = resp.status_code
                    self._response = resp

                def get_json(self):
                    return self._response.json()

            return Response(response)

    return FunctionClient()
