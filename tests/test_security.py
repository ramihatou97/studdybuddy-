"""Test security utilities"""
import pytest
from pathlib import Path
from utils.security import InputValidator, SecurityUtils
from utils.exceptions import *


def test_sanitize_text_removes_html():
    """Test HTML tag removal"""
    dirty = "<script>alert('XSS')</script><b>Hello</b> World"
    clean = InputValidator.sanitize_text(dirty)

    assert '<' not in clean
    assert '>' not in clean
    assert 'script' not in clean
    assert 'Hello' in clean
    assert 'World' in clean


def test_sanitize_text_escapes_special_chars():
    """Test special character escaping"""
    text = "Tom & Jerry's <adventure>"
    clean = InputValidator.sanitize_text(text)

    assert '&amp;' in clean
    assert '&#x27;' in clean or "'" in clean  # Apostrophe handling varies


def test_sanitize_text_truncates():
    """Test length truncation"""
    long_text = "A" * 2000
    clean = InputValidator.sanitize_text(long_text, max_length=100)

    assert len(clean) == 100


def test_path_traversal_detection():
    """Test path traversal is blocked"""
    with pytest.raises(PathTraversalError):
        InputValidator.validate_file_path(
            "../../../etc/passwd",
            allowed_dirs=["/safe/dir"]
        )


def test_valid_path_accepted(tmp_path):
    """Test valid paths are accepted"""
    test_file = tmp_path / "test.pdf"
    test_file.touch()

    validated = InputValidator.validate_file_path(
        str(test_file),
        allowed_dirs=[str(tmp_path)],
        must_exist=True
    )

    assert validated == test_file


def test_sanitize_filename():
    """Test filename sanitization"""
    dangerous = "../../../etc/passwd"
    safe = InputValidator.sanitize_filename(dangerous)

    assert '/' not in safe
    assert '..' not in safe
    assert 'passwd' in safe


def test_sanitize_filename_windows_reserved():
    """Test Windows reserved names are handled"""
    reserved = "CON.txt"
    safe = InputValidator.sanitize_filename(reserved)

    assert safe != "CON.txt"
    assert safe.startswith('_')


def test_email_validation():
    """Test email validation"""
    # Valid emails
    assert InputValidator.validate_email("user@example.com") == "user@example.com"
    assert InputValidator.validate_email("  TEST@EXAMPLE.COM  ") == "test@example.com"

    # Invalid emails
    with pytest.raises(InvalidFormatError):
        InputValidator.validate_email("invalid.email")

    with pytest.raises(InvalidFormatError):
        InputValidator.validate_email("@example.com")


def test_integer_range_validation():
    """Test integer range validation"""
    # Valid
    assert InputValidator.validate_integer_range(5, "count", 0, 10) == 5

    # Too small
    with pytest.raises(InvalidRangeError):
        InputValidator.validate_integer_range(-1, "count", 0, 10)

    # Too large
    with pytest.raises(InvalidRangeError):
        InputValidator.validate_integer_range(11, "count", 0, 10)


def test_file_size_validation(tmp_path):
    """Test file size validation"""
    # Create a small file
    small_file = tmp_path / "small.pdf"
    small_file.write_bytes(b"x" * 1024)  # 1KB

    # Should pass
    InputValidator.validate_file_size(small_file, max_size_mb=1)

    # Create a large file
    large_file = tmp_path / "large.pdf"
    large_file.write_bytes(b"x" * (2 * 1024 * 1024))  # 2MB

    # Should fail
    with pytest.raises(FileTooLargeError):
        InputValidator.validate_file_size(large_file, max_size_mb=1)


def test_generate_secure_id():
    """Test secure ID generation"""
    id1 = SecurityUtils.generate_secure_id("test")
    id2 = SecurityUtils.generate_secure_id("test")

    # IDs should be unique
    assert id1 != id2

    # Should have prefix
    assert id1.startswith("test_")

    # Should be long enough
    assert len(id1) > 20


def test_password_hashing():
    """Test password hashing and verification"""
    password = "SecurePassword123!"

    # Hash password
    hashed, salt = SecurityUtils.hash_password(password)

    # Should be able to verify
    assert SecurityUtils.verify_password(password, hashed, salt)

    # Wrong password should fail
    assert not SecurityUtils.verify_password("WrongPassword", hashed, salt)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
