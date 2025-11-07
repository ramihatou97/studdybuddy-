"""
Custom exception hierarchy with error codes
Implements Neurocore Lesson 5: Structured Exception Handling
"""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(str, Enum):
    """Enumeration of all error codes for type safety"""

    # Database errors (DB_xxx)
    DB_CONNECTION_FAILED = "DB_001"
    DB_RECORD_NOT_FOUND = "DB_002"
    DB_CONSTRAINT_VIOLATION = "DB_003"
    DB_QUERY_ERROR = "DB_004"

    # Validation errors (VAL_xxx)
    VAL_MISSING_FIELD = "VAL_001"
    VAL_INVALID_FORMAT = "VAL_002"
    VAL_INVALID_RANGE = "VAL_003"
    VAL_PATH_TRAVERSAL = "VAL_004"

    # External API errors (API_xxx)
    API_OPENAI_ERROR = "API_001"
    API_PUBMED_ERROR = "API_002"
    API_ANTHROPIC_ERROR = "API_003"
    API_RATE_LIMITED = "API_004"
    API_TIMEOUT = "API_005"

    # File processing errors (FILE_xxx)
    FILE_NOT_FOUND = "FILE_001"
    FILE_READ_ERROR = "FILE_002"
    FILE_CORRUPT = "FILE_003"
    FILE_TOO_LARGE = "FILE_004"

    # Timeout errors (TIMEOUT_xxx)
    TIMEOUT_OPERATION = "TIMEOUT_001"
    TIMEOUT_AI_GENERATION = "TIMEOUT_002"
    TIMEOUT_SEARCH = "TIMEOUT_003"


class NeurosurgicalKBException(Exception):
    """
    Base exception for all system errors

    Features:
    - Error codes for machine-readable identification
    - Context dict for debugging information
    - Serializable for logging and API responses
    """

    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        context: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.original_exception = original_exception

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging/API responses"""
        result = {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code.value,
            'context': self.context
        }

        if self.original_exception:
            result['original_error'] = str(self.original_exception)

        return result

    def __str__(self) -> str:
        """Human-readable error message"""
        parts = [f"[{self.error_code.value}] {self.message}"]
        if self.context:
            parts.append(f"Context: {self.context}")
        return " | ".join(parts)


# =============================================================================
# Database Errors
# =============================================================================

class DatabaseError(NeurosurgicalKBException):
    """Base class for all database-related errors"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Failed to connect to database"""

    def __init__(self, context: Optional[Dict] = None, original: Optional[Exception] = None):
        super().__init__(
            message="Failed to connect to database",
            error_code=ErrorCode.DB_CONNECTION_FAILED,
            context=context,
            original_exception=original
        )


class RecordNotFoundError(DatabaseError):
    """Database record not found"""

    def __init__(self, resource: str, resource_id: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"{resource} not found: {resource_id}",
            error_code=ErrorCode.DB_RECORD_NOT_FOUND,
            context={'resource': resource, 'id': resource_id, **(context or {})}
        )


class DatabaseConstraintViolation(DatabaseError):
    """Database constraint violation (unique, foreign key, etc.)"""

    def __init__(self, constraint: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"Database constraint violated: {constraint}",
            error_code=ErrorCode.DB_CONSTRAINT_VIOLATION,
            context={'constraint': constraint, **(context or {})}
        )


# =============================================================================
# Validation Errors
# =============================================================================

class ValidationError(NeurosurgicalKBException):
    """Base class for validation errors"""
    pass


class MissingFieldError(ValidationError):
    """Required field is missing"""

    def __init__(self, field: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"Required field missing: {field}",
            error_code=ErrorCode.VAL_MISSING_FIELD,
            context={'field': field, **(context or {})}
        )


class InvalidFormatError(ValidationError):
    """Field format is invalid"""

    def __init__(self, field: str, expected: str, actual: str = None, context: Optional[Dict] = None):
        super().__init__(
            message=f"Invalid format for {field}: expected {expected}",
            error_code=ErrorCode.VAL_INVALID_FORMAT,
            context={
                'field': field,
                'expected': expected,
                'actual': actual,
                **(context or {})
            }
        )


class InvalidRangeError(ValidationError):
    """Value is outside acceptable range"""

    def __init__(self, field: str, value: Any, min_val: Any = None, max_val: Any = None):
        range_str = f"[{min_val}, {max_val}]"
        super().__init__(
            message=f"Value for {field} ({value}) is outside acceptable range {range_str}",
            error_code=ErrorCode.VAL_INVALID_RANGE,
            context={'field': field, 'value': value, 'min': min_val, 'max': max_val}
        )


class PathTraversalError(ValidationError):
    """Path traversal attempt detected"""

    def __init__(self, path: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"Path traversal detected: {path}",
            error_code=ErrorCode.VAL_PATH_TRAVERSAL,
            context={'path': path, **(context or {})}
        )


# =============================================================================
# External API Errors
# =============================================================================

class ExternalAPIError(NeurosurgicalKBException):
    """Base class for external API errors"""
    pass


class OpenAIAPIError(ExternalAPIError):
    """OpenAI API error"""

    def __init__(self, message: str, context: Optional[Dict] = None, original: Optional[Exception] = None):
        super().__init__(
            message=f"OpenAI API error: {message}",
            error_code=ErrorCode.API_OPENAI_ERROR,
            context=context,
            original_exception=original
        )


class PubMedAPIError(ExternalAPIError):
    """PubMed API error"""

    def __init__(self, message: str, context: Optional[Dict] = None, original: Optional[Exception] = None):
        super().__init__(
            message=f"PubMed API error: {message}",
            error_code=ErrorCode.API_PUBMED_ERROR,
            context=context,
            original_exception=original
        )


class AnthropicAPIError(ExternalAPIError):
    """Anthropic API error"""

    def __init__(self, message: str, context: Optional[Dict] = None, original: Optional[Exception] = None):
        super().__init__(
            message=f"Anthropic API error: {message}",
            error_code=ErrorCode.API_ANTHROPIC_ERROR,
            context=context,
            original_exception=original
        )


class RateLimitError(ExternalAPIError):
    """API rate limit exceeded"""

    def __init__(self, service: str, retry_after: Optional[int] = None, context: Optional[Dict] = None):
        super().__init__(
            message=f"Rate limit exceeded for {service}" +
                   (f" (retry after {retry_after}s)" if retry_after else ""),
            error_code=ErrorCode.API_RATE_LIMITED,
            context={'service': service, 'retry_after': retry_after, **(context or {})}
        )


# =============================================================================
# File Processing Errors
# =============================================================================

class FileProcessingError(NeurosurgicalKBException):
    """Base class for file processing errors"""
    pass


class PDFNotFoundError(FileProcessingError):
    """PDF file not found"""

    def __init__(self, file_path: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"PDF file not found: {file_path}",
            error_code=ErrorCode.FILE_NOT_FOUND,
            context={'file_path': file_path, **(context or {})}
        )


class PDFReadError(FileProcessingError):
    """Failed to read PDF file"""

    def __init__(self, file_path: str, context: Optional[Dict] = None, original: Optional[Exception] = None):
        super().__init__(
            message=f"Failed to read PDF: {file_path}",
            error_code=ErrorCode.FILE_READ_ERROR,
            context={'file_path': file_path, **(context or {})},
            original_exception=original
        )


class CorruptPDFError(FileProcessingError):
    """PDF file is corrupted or invalid"""

    def __init__(self, file_path: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"Corrupt or invalid PDF: {file_path}",
            error_code=ErrorCode.FILE_CORRUPT,
            context={'file_path': file_path, **(context or {})}
        )


class FileTooLargeError(FileProcessingError):
    """File exceeds maximum size limit"""

    def __init__(self, file_path: str, size_mb: float, max_size_mb: float):
        super().__init__(
            message=f"File too large: {file_path} ({size_mb}MB, max {max_size_mb}MB)",
            error_code=ErrorCode.FILE_TOO_LARGE,
            context={'file_path': file_path, 'size_mb': size_mb, 'max_size_mb': max_size_mb}
        )


# =============================================================================
# Timeout Errors
# =============================================================================

class TimeoutError(NeurosurgicalKBException):
    """Operation exceeded timeout"""

    def __init__(self, operation: str, timeout_seconds: int, context: Optional[Dict] = None):
        super().__init__(
            message=f"Operation timed out: {operation} ({timeout_seconds}s)",
            error_code=ErrorCode.TIMEOUT_OPERATION,
            context={'operation': operation, 'timeout': timeout_seconds, **(context or {})}
        )


class AIGenerationTimeoutError(TimeoutError):
    """AI generation exceeded timeout"""

    def __init__(self, timeout_seconds: int, context: Optional[Dict] = None):
        super().__init__(
            message=f"AI generation timed out ({timeout_seconds}s)",
            error_code=ErrorCode.TIMEOUT_AI_GENERATION,
            context={'timeout': timeout_seconds, **(context or {})}
        )


class SearchTimeoutError(TimeoutError):
    """Search operation exceeded timeout"""

    def __init__(self, search_type: str, timeout_seconds: int, context: Optional[Dict] = None):
        super().__init__(
            message=f"{search_type} search timed out ({timeout_seconds}s)",
            error_code=ErrorCode.TIMEOUT_SEARCH,
            context={'search_type': search_type, 'timeout': timeout_seconds, **(context or {})}
        )
