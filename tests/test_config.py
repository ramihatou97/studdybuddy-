"""Test configuration management"""
import pytest
import os
from pathlib import Path
from utils.config import Settings, get_settings, reload_settings


def test_settings_from_env(monkeypatch):
    """Test settings load from environment"""
    # Set environment variables (using nested delimiter __)
    monkeypatch.setenv('AI__ANTHROPIC_API_KEY', 'test_anthropic')
    monkeypatch.setenv('AI__OPENAI_API_KEY', 'test_openai')
    monkeypatch.setenv('PUBMED_EMAIL', 'test@example.com')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

    settings = reload_settings()

    assert settings.ai.anthropic_api_key == 'test_anthropic'
    assert settings.ai.openai_api_key == 'test_openai'
    assert settings.pubmed_email == 'test@example.com'
    assert settings.log_level == 'DEBUG'


def test_settings_validation_fails_on_invalid():
    """Test settings validation catches errors"""
    with pytest.raises(ValueError):
        Settings(
            ai={'anthropic_api_key': 'test', 'openai_api_key': 'test'},
            pubmed_email='test@example.com',
            log_level='INVALID'  # Should fail
        )


def test_timeout_configuration():
    """Test timeout configuration with bounds"""
    settings = Settings(
        ai={'anthropic_api_key': 'test', 'openai_api_key': 'test'},
        pubmed_email='test@example.com',
        timeouts={'ai_generation': 60}
    )

    assert settings.timeouts.ai_generation == 60

    # Test bounds
    with pytest.raises(ValueError):
        Settings(
            ai={'anthropic_api_key': 'test', 'openai_api_key': 'test'},
            pubmed_email='test@example.com',
            timeouts={'ai_generation': 700}  # Exceeds max
        )


def test_nested_config_from_env(monkeypatch):
    """Test nested configuration from environment"""
    monkeypatch.setenv('AI__ANTHROPIC_API_KEY', 'test')
    monkeypatch.setenv('AI__OPENAI_API_KEY', 'test')
    monkeypatch.setenv('PUBMED_EMAIL', 'test@example.com')
    monkeypatch.setenv('DATABASE__URL', 'postgresql://test')
    monkeypatch.setenv('REDIS__ENABLED', 'true')
    monkeypatch.setenv('REDIS__HOST', 'redis.example.com')

    settings = reload_settings()

    assert settings.database.url == 'postgresql://test'
    assert settings.redis.enabled is True
    assert settings.redis.host == 'redis.example.com'


def test_get_settings_singleton():
    """Test settings is a singleton"""
    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
