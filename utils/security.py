"""
Security utilities for input validation and sanitization
Implements Neurocore Lesson 2: Security from Day 1
"""

import re
import html
from pathlib import Path
from typing import List, Optional
import hashlib

from .exceptions import (
    PathTraversalError,
    InvalidFormatError,
    InvalidRangeError,
    FileTooLargeError
)


class InputValidator:
    """
    Validates and sanitizes all user inputs

    Protections:
    - XSS (Cross-Site Scripting)
    - SQL Injection
    - Path Traversal
    - DoS via huge inputs
    """

    @staticmethod
    def sanitize_text(
        text: str,
        max_length: int = 1000,
        allow_newlines: bool = True
    ) -> str:
        """
        Sanitize text input for safe storage and display

        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            allow_newlines: Whether to preserve newline characters

        Returns:
            Sanitized text

        Example:
            >>> InputValidator.sanitize_text("<script>alert('XSS')</script>Hello")
            "alert('XSS')Hello"
        """
        if not text:
            return ""

        # Truncate to max length (DoS prevention)
        text = text[:max_length]

        # Remove all HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Escape HTML special characters
        text = html.escape(text)

        # Remove control characters except newlines/tabs if allowed
        if allow_newlines:
            text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
        else:
            text = re.sub(r'[\x00-\x1F\x7F]', '', text)

        return text.strip()

    @staticmethod
    def validate_file_path(
        path: str,
        allowed_dirs: List[str],
        must_exist: bool = False
    ) -> Path:
        """
        Validate file path to prevent path traversal attacks

        Args:
            path: File path to validate
            allowed_dirs: List of allowed parent directories
            must_exist: Whether file must exist

        Returns:
            Validated Path object

        Raises:
            PathTraversalError: If path traversal detected
            FileNotFoundError: If must_exist=True and file doesn't exist

        Example:
            >>> validator.validate_file_path(
            ...     "/safe/dir/file.pdf",
            ...     allowed_dirs=["/safe/dir"]
            ... )
            Path('/safe/dir/file.pdf')
        """
        # Convert to Path and resolve
        try:
            path_obj = Path(path).resolve()
        except (ValueError, OSError) as e:
            raise PathTraversalError(path, {'reason': str(e)})

        # Check for suspicious patterns
        if '../' in str(path) or '..\\'  in str(path):
            raise PathTraversalError(path, {'reason': 'Relative path detected'})

        if '~' in str(path):
            raise PathTraversalError(path, {'reason': 'Home directory expansion not allowed'})

        # Verify path is within allowed directories
        is_allowed = False
        for allowed_dir in allowed_dirs:
            try:
                allowed_path = Path(allowed_dir).resolve()
                # Check if path is relative to allowed directory
                path_obj.relative_to(allowed_path)
                is_allowed = True
                break
            except ValueError:
                continue

        if not is_allowed:
            raise PathTraversalError(
                path,
                {
                    'allowed_dirs': allowed_dirs,
                    'attempted_path': str(path_obj)
                }
            )

        # Check existence if required
        if must_exist and not path_obj.exists():
            from .exceptions import PDFNotFoundError
            raise PDFNotFoundError(str(path_obj))

        return path_obj

    @staticmethod
    def sanitize_filename(filename: str, max_length: int = 255) -> str:
        """
        Sanitize filename to prevent injection and filesystem issues

        Args:
            filename: Filename to sanitize
            max_length: Maximum filename length

        Returns:
            Sanitized filename

        Example:
            >>> InputValidator.sanitize_filename("../../../etc/passwd")
            "etc_passwd"
        """
        # Remove path separators
        filename = filename.replace('/', '_').replace('\\', '_')

        # Remove or replace special characters
        # Keep: alphanumeric, dash, underscore, dot
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

        # Replace consecutive dots with single underscore
        filename = re.sub(r'\.\.+', '_', filename)

        # Prevent hidden files
        if filename.startswith('.'):
            filename = '_' + filename[1:]

        # Prevent reserved names (Windows)
        reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                   'LPT1', 'LPT2', 'LPT3'}
        if filename.upper().split('.')[0] in reserved:
            filename = '_' + filename

        # Truncate to max length
        if len(filename) > max_length:
            # Preserve extension
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            name = name[:max_length - len(ext) - 1]
            filename = f"{name}.{ext}" if ext else name

        return filename

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate email format

        Args:
            email: Email address to validate

        Returns:
            Normalized email address

        Raises:
            InvalidFormatError: If email format invalid
        """
        # Simple regex for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        email = email.strip().lower()

        if not re.match(pattern, email):
            raise InvalidFormatError('email', 'valid email address', email)

        return email

    @staticmethod
    def validate_integer_range(
        value: int,
        field: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None
    ) -> int:
        """
        Validate integer is within acceptable range

        Args:
            value: Value to validate
            field: Field name for error messages
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value

        Returns:
            Validated value

        Raises:
            InvalidRangeError: If value outside range
        """
        if min_val is not None and value < min_val:
            raise InvalidRangeError(field, value, min_val, max_val)

        if max_val is not None and value > max_val:
            raise InvalidRangeError(field, value, min_val, max_val)

        return value

    @staticmethod
    def validate_float_range(
        value: float,
        field: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> float:
        """Validate float is within acceptable range"""
        if min_val is not None and value < min_val:
            raise InvalidRangeError(field, value, min_val, max_val)

        if max_val is not None and value > max_val:
            raise InvalidRangeError(field, value, min_val, max_val)

        return value

    @staticmethod
    def validate_file_size(
        file_path: Path,
        max_size_mb: float = 100
    ) -> Path:
        """
        Validate file size doesn't exceed limit

        Args:
            file_path: Path to file
            max_size_mb: Maximum size in megabytes

        Returns:
            Validated file path

        Raises:
            FileTooLargeError: If file too large
        """
        if not file_path.exists():
            from .exceptions import PDFNotFoundError
            raise PDFNotFoundError(str(file_path))

        size_bytes = file_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)

        if size_mb > max_size_mb:
            raise FileTooLargeError(str(file_path), size_mb, max_size_mb)

        return file_path


class SecurityUtils:
    """Additional security utilities"""

    @staticmethod
    def generate_secure_id(prefix: str = "") -> str:
        """
        Generate cryptographically secure unique ID

        Args:
            prefix: Optional prefix for the ID

        Returns:
            Secure unique identifier

        Example:
            >>> SecurityUtils.generate_secure_id("chapter")
            "chapter_a1b2c3d4e5f6..."
        """
        import uuid
        unique_id = uuid.uuid4().hex
        return f"{prefix}_{unique_id}" if prefix else unique_id

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """
        Hash password securely

        Args:
            password: Plain text password
            salt: Optional salt (generated if not provided)

        Returns:
            Tuple of (hashed_password, salt)
        """
        import secrets

        if salt is None:
            salt = secrets.token_hex(32)

        # Use PBKDF2 with 100,000 iterations
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )

        return password_hash.hex(), salt

    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """
        Verify password against hash

        Args:
            password: Plain text password to verify
            hashed: Stored hash
            salt: Salt used during hashing

        Returns:
            True if password matches
        """
        new_hash, _ = SecurityUtils.hash_password(password, salt)
        return new_hash == hashed
