"""Test configuration and shared fixtures - minimal setup."""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any
from main import app


class TestConstants:
    """Essential test constants."""
    SUPPORTED_LANGUAGE = "python"
    UNSUPPORTED_LANGUAGE = "javascript"
    DEFAULT_TIMEOUT = 3
    
    # Execution statuses
    STATUS_OK = "OK"
    STATUS_ERROR = "ERROR"
    STATUS_RUNTIME_ERROR = "RUNTIME_ERROR"
    
    # API endpoint
    EXECUTE_ENDPOINT = "/api/v1/execute"
    
    # Required response fields
    REQUIRED_RESPONSE_FIELDS = ["status", "stdout", "stderr", "exit_code", "time_used", "memory_used"]


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def valid_execution_request() -> Dict[str, Any]:
    """Basic valid execution request."""
    return {
        "language": TestConstants.SUPPORTED_LANGUAGE,
        "code": "print('Hello World')",
        "input_data": "",
    }


def assert_valid_execution_result(response_data: Dict[str, Any]) -> None:
    """Assert valid execution result structure."""
    for field in TestConstants.REQUIRED_RESPONSE_FIELDS:
        assert field in response_data, f"Missing required field: {field}"
    
    assert isinstance(response_data["exit_code"], int)
    assert isinstance(response_data["time_used"], (int, float))
    assert isinstance(response_data["memory_used"], int)


def assert_successful_execution(response_data: Dict[str, Any], expected_output: str = None) -> None:
    """Assert successful code execution."""
    assert_valid_execution_result(response_data)
    assert response_data["status"] == TestConstants.STATUS_OK
    assert response_data["exit_code"] == 0
    
    if expected_output:
        assert expected_output in response_data["stdout"]


def assert_execution_error(response_data: Dict[str, Any], expected_status: str = None) -> None:
    """Assert execution error."""
    assert_valid_execution_result(response_data)
    
    if expected_status:
        assert response_data["status"] == expected_status
    else:
        assert response_data["status"] in {TestConstants.STATUS_ERROR, TestConstants.STATUS_RUNTIME_ERROR}