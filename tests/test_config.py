"""Tests for configuration."""

import pytest
import os
from pathlib import Path
from unittest.mock import patch

from openclaw_telegram.config import Config


def test_config_from_env():
    """Test loading config from environment."""
    with patch.dict(os.environ, {
        'TG_CLI_PATH': '/usr/bin/tg',
        'PHONE_NUMBER': '+1234567890',
    }):
        config = Config()
        
        assert config.tg_cli_path == '/usr/bin/tg'
        assert config.phone_number == '+1234567890'


def test_config_defaults():
    """Test config default values."""
    config = Config()
    
    assert config.tg_cli_path == 'tg'  # Default to PATH
    assert config.log_level == 'INFO'
    assert isinstance(config.tg_config_dir, Path)


def test_config_validation():
    """Test config validation."""
    config = Config()
    
    # Should always validate (no APP_ID needed)
    assert config.validate() is True


def test_config_repr():
    """Test config string representation."""
    config = Config()
    
    repr_str = repr(config)
    assert 'tg_cli' in repr_str
    assert 'config_dir' in repr_str
