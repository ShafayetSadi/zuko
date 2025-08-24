"""Tests for API routes - core functionality only."""

from http import HTTPStatus
from tests.conftest import TestConstants, assert_successful_execution, assert_execution_error


class TestExecuteEndpoint:
    """Essential tests for the /api/v1/execute endpoint."""

    def test_successful_execution(self, client, valid_execution_request):
        """Test successful Python code execution."""
        response = client.post(TestConstants.EXECUTE_ENDPOINT, json=valid_execution_request)
        
        assert response.status_code == HTTPStatus.OK
        assert_successful_execution(response.json(), "Hello World")

    def test_execution_with_input(self, client):
        """Test code execution with input data."""
        request = {
            "language": "python",
            "code": "name = input()\nprint(f'Hello {name}')",
            "input_data": "Zuko"
        }
        response = client.post(TestConstants.EXECUTE_ENDPOINT, json=request)
        
        assert response.status_code == HTTPStatus.OK
        assert_successful_execution(response.json(), "Hello Zuko")

    def test_runtime_error(self, client):
        """Test runtime error handling."""
        request = {"language": "python", "code": "print(1/0)"}
        response = client.post(TestConstants.EXECUTE_ENDPOINT, json=request)
        
        assert response.status_code == HTTPStatus.OK
        assert_execution_error(response.json(), TestConstants.STATUS_RUNTIME_ERROR)

    def test_unsupported_language(self, client):
        """Test unsupported language error."""
        request = {"language": "javascript", "code": "console.log('test')"}
        response = client.post(TestConstants.EXECUTE_ENDPOINT, json=request)
        
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert_execution_error(data, TestConstants.STATUS_ERROR)
        assert "Unsupported language: javascript" in data["stderr"]

    def test_invalid_request(self, client):
        """Test request validation."""
        response = client.post(TestConstants.EXECUTE_ENDPOINT, json={"language": "python"})  # Missing code
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY