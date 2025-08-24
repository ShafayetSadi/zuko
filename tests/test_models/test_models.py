"""Tests for Pydantic models - minimal essential tests only."""

import pytest
from pydantic import ValidationError
from zuko.models.execution import ExecutionResult
from zuko.models.request import CodeRequest


class TestModels:
    """Minimal test suite for our models."""

    def test_execution_result_creation(self):
        """Test ExecutionResult can be created with valid data."""
        result = ExecutionResult(
            status="OK",
            stdout="Hello",
            stderr="",
            exit_code=0,
            time_used=123.45,
            memory_used=2048,
        )
        assert result.status == "OK"
        assert result.time_used == 123.45

    def test_code_request_creation(self):
        """Test CodeRequest can be created with defaults."""
        request = CodeRequest(language="python", code="print('test')")
        assert request.language == "python"
        assert request.input_data == ""  # Default
        assert request.timeout == 3  # Default

    def test_validation_errors(self):
        """Test that invalid data raises ValidationError."""
        with pytest.raises(ValidationError):
            ExecutionResult(status="OK")  # Missing required fields
            
        with pytest.raises(ValidationError):
            CodeRequest(language="python")  # Missing code field