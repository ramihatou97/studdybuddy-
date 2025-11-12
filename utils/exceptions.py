"""
Custom exception hierarchy for StudyBuddy application.
Follows Neurocore Lesson 5: Structured exceptions with error codes.
"""


class StudyBuddyException(Exception):
    """Base exception for all StudyBuddy errors."""
    
    def __init__(self, message: str, error_code: str, context: dict = None):
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


# Database Exceptions
class DatabaseError(StudyBuddyException):
    """Base class for database-related errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Failed to connect to database."""
    
    def __init__(self, context: dict = None):
        super().__init__(
            message="Failed to connect to database",
            error_code="DB_001",
            context=context
        )


class RecordNotFoundError(DatabaseError):
    """Record not found in database."""
    
    def __init__(self, record_type: str, record_id: str, context: dict = None):
        ctx = context or {}
        ctx.update({"record_type": record_type, "record_id": record_id})
        super().__init__(
            message=f"{record_type} with ID {record_id} not found",
            error_code="DB_002",
            context=ctx
        )


# File Exceptions
class FileError(StudyBuddyException):
    """Base class for file-related errors."""
    pass


class FileNotFoundError(FileError):
    """File not found."""
    
    def __init__(self, file_path: str, context: dict = None):
        ctx = context or {}
        ctx.update({"file_path": file_path})
        super().__init__(
            message=f"File not found: {file_path}",
            error_code="FILE_001",
            context=ctx
        )


class InvalidFileFormatError(FileError):
    """Invalid file format."""
    
    def __init__(self, file_path: str, expected_format: str, context: dict = None):
        ctx = context or {}
        ctx.update({"file_path": file_path, "expected_format": expected_format})
        super().__init__(
            message=f"Invalid file format for {file_path}, expected {expected_format}",
            error_code="FILE_002",
            context=ctx
        )


# Validation Exceptions
class ValidationError(StudyBuddyException):
    """Base class for validation errors."""
    pass


class InvalidInputError(ValidationError):
    """Invalid user input."""
    
    def __init__(self, field_name: str, reason: str, context: dict = None):
        ctx = context or {}
        ctx.update({"field_name": field_name, "reason": reason})
        super().__init__(
            message=f"Invalid input for {field_name}: {reason}",
            error_code="VAL_001",
            context=ctx
        )


# Configuration Exceptions
class ConfigurationError(StudyBuddyException):
    """Base class for configuration errors."""
    pass


class MissingConfigError(ConfigurationError):
    """Required configuration is missing."""
    
    def __init__(self, config_key: str, context: dict = None):
        ctx = context or {}
        ctx.update({"config_key": config_key})
        super().__init__(
            message=f"Missing required configuration: {config_key}",
            error_code="CFG_001",
            context=ctx
        )
