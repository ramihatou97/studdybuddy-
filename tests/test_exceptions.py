"""Test exception hierarchy"""
import pytest
from utils.exceptions import *


def test_database_connection_error():
    """Test database connection error"""
    error = DatabaseConnectionError(context={'host': 'localhost'})

    assert error.error_code == ErrorCode.DB_CONNECTION_FAILED
    assert 'localhost' in str(error)

    error_dict = error.to_dict()
    assert error_dict['error_code'] == 'DB_001'
    assert error_dict['context']['host'] == 'localhost'


def test_validation_error_with_context():
    """Test validation error includes context"""
    error = InvalidFormatError('email', 'user@domain.com', 'invalid')

    assert 'email' in str(error)
    assert error.context['field'] == 'email'
    assert error.context['expected'] == 'user@domain.com'


def test_exception_preserves_original():
    """Test that original exception is preserved"""
    original = ValueError("Original error")
    error = DatabaseConnectionError(original=original)

    assert error.original_exception is original
    assert 'Original error' in str(error.to_dict()['original_error'])


def test_all_error_codes_unique():
    """Ensure all error codes are unique"""
    codes = [code.value for code in ErrorCode]
    assert len(codes) == len(set(codes)), "Duplicate error codes found!"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
