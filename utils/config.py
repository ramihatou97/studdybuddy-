"""
Configuration management with Pydantic
Implements Neurocore Lesson 9: Type-safe configuration
"""

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional, List
from pathlib import Path
import os


class DatabaseConfig(BaseModel):
    """Database configuration"""

    url: str = Field(
        default="sqlite:///neurosurgery_library.db",
        description="Database connection URL"
    )
    pool_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Connection pool size"
    )
    max_overflow: int = Field(
        default=10,
        ge=0,
        le=100,
        description="Maximum pool overflow"
    )
    echo: bool = Field(
        default=False,
        description="Echo SQL queries (debug mode)"
    )


class RedisConfig(BaseModel):
    """Redis cache configuration"""

    enabled: bool = Field(
        default=False,
        description="Enable Redis caching"
    )
    host: str = Field(
        default="localhost",
        description="Redis host"
    )
    port: int = Field(
        default=6379,
        ge=1,
        le=65535,
        description="Redis port"
    )
    password: Optional[str] = Field(
        default=None,
        description="Redis password"
    )
    db: int = Field(
        default=0,
        ge=0,
        le=15,
        description="Redis database number"
    )


class AIProviderConfig(BaseModel):
    """AI provider configuration"""

    anthropic_api_key: str = Field(
        ...,
        description="Anthropic API key (required)"
    )
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key (required)"
    )
    google_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API key (optional)"
    )

    default_provider: str = Field(
        default="claude",
        description="Default AI provider"
    )

    @field_validator('default_provider')
    @classmethod
    def validate_provider(cls, v):
        valid = ['claude', 'openai', 'gemini']
        if v not in valid:
            raise ValueError(f"Invalid provider: {v}. Must be one of {valid}")
        return v


class TimeoutConfig(BaseModel):
    """Timeout configuration"""

    default: int = Field(
        default=30,
        ge=1,
        le=600,
        description="Default timeout (seconds)"
    )
    ai_generation: int = Field(
        default=120,
        ge=1,
        le=600,
        description="AI generation timeout (seconds)"
    )
    ai_embedding: int = Field(
        default=30,
        ge=1,
        le=300,
        description="AI embedding timeout (seconds)"
    )
    pubmed_search: int = Field(
        default=45,
        ge=1,
        le=300,
        description="PubMed search timeout (seconds)"
    )
    pdf_indexing: int = Field(
        default=300,
        ge=1,
        le=3600,
        description="PDF indexing timeout (seconds)"
    )


class ReferenceLibraryConfig(BaseModel):
    """Reference library configuration"""

    path: Optional[Path] = Field(
        default=None,
        description="Path to reference library directory"
    )
    max_pdf_size_mb: float = Field(
        default=100.0,
        ge=1.0,
        le=1000.0,
        description="Maximum PDF size in MB"
    )
    concurrent_indexing_jobs: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of concurrent indexing jobs"
    )

    @field_validator('path', mode='before')
    @classmethod
    def validate_path(cls, v):
        if v and not Path(v).exists():
            raise ValueError(f"Reference library path does not exist: {v}")
        return v


class Settings(BaseSettings):
    """
    Main application settings

    Loads from environment variables with optional .env file
    Type-safe with validation
    """

    # Database
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)

    # Redis cache
    redis: RedisConfig = Field(default_factory=RedisConfig)

    # AI providers
    ai: AIProviderConfig

    # Timeouts
    timeouts: TimeoutConfig = Field(default_factory=TimeoutConfig)

    # Reference library
    reference_library: ReferenceLibraryConfig = Field(default_factory=ReferenceLibraryConfig)

    # PubMed
    pubmed_email: str = Field(
        ...,
        description="Email for PubMed API (required by NCBI)"
    )
    pubmed_api_key: Optional[str] = Field(
        default=None,
        description="PubMed API key (optional)"
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    log_format: str = Field(
        default="text",
        description="Log format (json or text)"
    )
    log_file: Optional[Path] = Field(
        default=None,
        description="Log file path"
    )

    # Feature flags
    use_reference_library: bool = Field(
        default=True,
        description="Enable reference library"
    )
    enable_alive_chapters: bool = Field(
        default=False,
        description="Enable alive chapters monitoring"
    )
    track_costs: bool = Field(
        default=True,
        description="Track API costs"
    )

    # Development
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        valid = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v = v.upper()
        if v not in valid:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid}")
        return v

    @field_validator('log_format')
    @classmethod
    def validate_log_format(cls, v):
        valid = ['json', 'text']
        v = v.lower()
        if v not in valid:
            raise ValueError(f"Invalid log format: {v}. Must be one of {valid}")
        return v

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "env_nested_delimiter": "__",
    }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get application settings (singleton)

    Returns:
        Settings instance

    Example:
        >>> settings = get_settings()
        >>> print(settings.ai.default_provider)
        'claude'
    """
    global _settings

    if _settings is None:
        _settings = Settings()

    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment (useful for testing)"""
    global _settings
    _settings = None
    return get_settings()
