"""Tests for Telegram client."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from openclaw_telegram import TelegramClient
from openclaw_telegram.exceptions import ConnectionError as TGConnectionError


@pytest.mark.asyncio
async def test_client_initialization(mock_config):
    """Test client initialization."""
    client = TelegramClient(mock_config)
    assert client.config == mock_config
    assert not client._connected


@pytest.mark.asyncio
async def test_connect(mock_config):
    """Test connection to Telegram."""
    client = TelegramClient(mock_config)
    
    with patch('openclaw_telegram.client.TelethonClient') as mock_tg:
        mock_instance = AsyncMock()
        mock_instance.connect = AsyncMock()
        mock_tg.return_value = mock_instance
        
        result = await client.connect()
        
        assert result is True
        assert client._connected


@pytest.mark.asyncio
async def test_disconnect(mock_config):
    """Test disconnection from Telegram."""
    client = TelegramClient(mock_config)
    client._connected = True
    
    with patch('openclaw_telegram.client.TelethonClient') as mock_tg:
        mock_instance = AsyncMock()
        mock_instance.disconnect = AsyncMock()
        client._client = mock_instance
        
        await client.disconnect()
        
        assert not client._connected


@pytest.mark.asyncio
async def test_send_message(mock_config):
    """Test sending a message."""
    client = TelegramClient(mock_config)
    
    with patch('openclaw_telegram.client.TelethonClient') as mock_tg:
        mock_instance = AsyncMock()
        mock_instance.send_message = AsyncMock(return_value=MagicMock(
            id=123,
            text="Test message",
            date=None,
        ))
        client._client = mock_instance
        
        result = await client.send_message("@test", "Hello")
        
        assert result['id'] == 123
        assert result['text'] == "Test message"
        mock_instance.send_message.assert_called_once_with("@test", "Hello")


@pytest.mark.asyncio
async def test_send_message_not_connected(mock_config):
    """Test sending message when not connected."""
    client = TelegramClient(mock_config)
    
    with pytest.raises(TGConnectionError):
        await client.send_message("@test", "Hello")


@pytest.mark.asyncio
async def test_is_authorized(mock_config):
    """Test authorization check."""
    client = TelegramClient(mock_config)
    
    with patch('openclaw_telegram.client.TelethonClient') as mock_tg:
        mock_instance = AsyncMock()
        mock_instance.is_user_authorized = AsyncMock(return_value=True)
        client._client = mock_instance
        
        result = await client.is_authorized()
        
        assert result is True
