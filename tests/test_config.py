"""Tests for configuration."""

import pytest
import os
from pathlib import Path
from unittest.mock import patch

from openclaw_telegram.config import Config


def test_config_from_env():
    """Test loading config from environment."""
    with patch.dict(os.environ, {
        'API_ID': '123456',
        'API_HASH': 'test_hash',
        'PHONE_NUMBER': '+1234567890',
    }):
        config = Config()
        
        assert config.api_id == 123456
        assert config.api_hash == 'test_hash'
        assert config.phone_number == '+1234567890'


def test_config_validation():
    """Test config validation."""
    config = Config.__new__(Config)
    config.api_id = 0
    config.api_hash = ''
    config.phone_number = ''
    
    assert not config.validate()
    
    config.api_id = 123456
    config.api_hash = 'hash'
    config.phone_number = '+1234567890'
    
    assert config.validate()


def test_config_defaults():
    """Test config default values."""
    config = Config.__new__(Config)
    config.api_id = 0
    config.api_hash = ''
    config.phone_number = ''
    config.session_name = os.getenv('SESSION_NAME', 'telegram_session')
    config.log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    assert config.session_name == 'telegram_session'
    assert config.log_level == 'INFO'
