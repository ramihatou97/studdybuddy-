"""Test logging utilities"""
import pytest
import logging
import json
from io import StringIO
from utils.logger import get_logger, StructuredFormatter, TextFormatter


def test_get_logger_creates_logger():
    """Test logger creation"""
    logger = get_logger("test_logger")

    assert logger is not None
    assert logger.name == "test_logger"
    assert len(logger.handlers) > 0


def test_json_formatter():
    """Test JSON formatting"""
    formatter = StructuredFormatter()

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None
    )
    record.module = "test_module"
    record.funcName = "test_function"

    formatted = formatter.format(record)

    # Should be valid JSON
    log_data = json.loads(formatted)

    assert log_data['level'] == 'INFO'
    assert log_data['message'] == 'Test message'
    assert log_data['module'] == 'test_module'
    assert 'timestamp' in log_data


def test_json_formatter_with_context():
    """Test JSON formatter preserves context"""
    formatter = StructuredFormatter()

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test with context",
        args=(),
        exc_info=None
    )
    record.context = {'user_id': 123, 'action': 'test'}

    formatted = formatter.format(record)
    log_data = json.loads(formatted)

    assert 'context' in log_data
    assert log_data['context']['user_id'] == 123


def test_text_formatter():
    """Test text formatting"""
    formatter = TextFormatter()

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None
    )
    record.module = "test_module"
    record.funcName = "test_function"

    formatted = formatter.format(record)

    assert 'INFO' in formatted
    assert 'Test message' in formatted
    assert 'test_module:test_function:10' in formatted


def test_logger_with_context():
    """Test logging with context"""
    import logging
    from io import StringIO

    # Capture log output
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(StructuredFormatter())

    logger = logging.getLogger("test_context")
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Log with context
    logger.info("Test", extra={'context': {'key': 'value'}})

    output = stream.getvalue()
    log_data = json.loads(output)

    assert log_data['context']['key'] == 'value'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
