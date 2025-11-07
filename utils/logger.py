"""
Structured logging with context preservation
Implements Neurocore Lesson 5: Proper error tracking
"""

import logging
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging

    Benefits:
    - Machine-parseable logs
    - Preserves context
    - Easy to search/filter
    - Integrates with log aggregation tools
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""

        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }

        # Add custom context if present
        if hasattr(record, 'context'):
            log_data['context'] = record.context

        # Add request ID if present (for request tracking)
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id

        # Add user ID if present
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """
    Human-readable text formatter for development

    Format: [TIMESTAMP] LEVEL: message (module:function:line)
    """

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        location = f"{record.module}:{record.funcName}:{record.lineno}"

        message = f"[{timestamp}] {record.levelname}: {record.getMessage()} ({location})"

        # Add exception if present
        if record.exc_info:
            message += "\n" + self.formatException(record.exc_info)

        # Add context if present
        if hasattr(record, 'context'):
            message += f"\n  Context: {record.context}"

        return message


def get_logger(
    name: str,
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Get configured logger instance

    Args:
        name: Logger name (usually __name__)
        log_level: Override log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format type (json or text)
        log_file: Optional log file path

    Returns:
        Configured logger

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Starting process", extra={'context': {'user_id': 123}})
    """
    # Get or create logger
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if logger.handlers:
        return logger

    # Determine log level
    if log_level is None:
        import os
        log_level = os.getenv('LOG_LEVEL', 'INFO')

    logger.setLevel(getattr(logging, log_level.upper()))

    # Determine format
    if log_format is None:
        import os
        log_format = os.getenv('LOG_FORMAT', 'text').lower()

    formatter = StructuredFormatter() if log_format == 'json' else TextFormatter()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # Check environment for file
        import os
        env_log_file = os.getenv('LOG_FILE')
        if env_log_file:
            # Ensure directory exists
            Path(env_log_file).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(env_log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


class LoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that adds context to all log messages

    Useful for adding request_id, user_id, or other contextual info
    to all logs in a scope.

    Example:
        >>> base_logger = get_logger(__name__)
        >>> logger = LoggerAdapter(base_logger, {'request_id': '123'})
        >>> logger.info("Processing request")
        # Log will include request_id automatically
    """

    def process(self, msg, kwargs):
        """Add extra context to log record"""
        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        # Merge adapter context with any extra context
        if hasattr(self, 'extra'):
            kwargs['extra'].update(self.extra)

        return msg, kwargs
