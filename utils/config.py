"""
Configuration management for StudyBuddy.
Follows Neurocore Lesson 9: Type-safe configuration with Pydantic.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseConfig(BaseModel):
    """Database configuration."""
    db_path: Path = Field(
        default=Path("data/database/studybuddy.db"),
        description="Path to SQLite database file"
    )
    
    @field_validator('db_path')
    @classmethod
    def ensure_db_dir_exists(cls, v: Path) -> Path:
        """Ensure database directory exists."""
        v.parent.mkdir(parents=True, exist_ok=True)
        return v


class LibraryConfig(BaseModel):
    """Library configuration for PDFs and books."""
    books_dir: Path = Field(
        default=Path("data/books"),
        description="Directory for storing PDF books"
    )
    images_dir: Path = Field(
        default=Path("data/images"),
        description="Directory for extracted images"
    )
    
    @field_validator('books_dir', 'images_dir')
    @classmethod
    def ensure_dir_exists(cls, v: Path) -> Path:
        """Ensure directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v


class StudyConfig(BaseModel):
    """Study session configuration."""
    default_session_duration_minutes: int = Field(
        default=25,
        ge=1,
        le=120,
        description="Default study session duration in minutes"
    )
    flashcard_review_interval_days: int = Field(
        default=1,
        ge=1,
        le=365,
        description="Default interval for flashcard review"
    )


class AppConfig(BaseModel):
    """Main application configuration."""
    app_name: str = Field(default="StudyBuddy", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    library: LibraryConfig = Field(default_factory=LibraryConfig)
    study: StudyConfig = Field(default_factory=StudyConfig)
    logs_dir: Path = Field(
        default=Path("logs"),
        description="Directory for log files"
    )
    
    @field_validator('logs_dir')
    @classmethod
    def ensure_logs_dir_exists(cls, v: Path) -> Path:
        """Ensure logs directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    model_config = {"validate_assignment": True}


def get_config() -> AppConfig:
    """Get application configuration singleton."""
    return AppConfig()
