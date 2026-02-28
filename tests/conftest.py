"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from openclaw_telegram.config import Config


@pytest.fixture
def mock_config():
    """Mock configuration."""
    config = Config()
    config.telethon_api_id = 123456
    config.telethon_api_hash = "test_hash"
    config.telethon_phone = "+1234567890"
    return config


@pytest.fixture
def mock_telethon_client():
    """Mock Telethon client."""
    client = AsyncMock()
    client.connect = AsyncMock(return_value=None)
    client.disconnect = AsyncMock(return_value=None)
    client.is_user_authorized = AsyncMock(return_value=True)
    client.send_message = AsyncMock(
        return_value=MagicMock(
            id=1,
            text="Test message",
            date=None,
        )
    )
    return client
