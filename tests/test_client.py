"""Tests for Telegram client."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from openclaw_telegram import TelegramClient
from openclaw_telegram.exceptions import ConnectionError as TGConnectionError
from openclaw_telegram.policies import AccessPolicy


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

    # Mock backend
    mock_backend = AsyncMock()
    mock_backend.connect = AsyncMock(return_value=True)
    client._backend = mock_backend

    result = await client.connect()

    assert result is True
    assert client._connected
    mock_backend.connect.assert_called_once()


@pytest.mark.asyncio
async def test_disconnect(mock_config):
    """Test disconnection from Telegram."""
    client = TelegramClient(mock_config)

    # Mock backend
    mock_backend = AsyncMock()
    mock_backend.disconnect = AsyncMock()
    client._backend = mock_backend
    client._connected = True

    await client.disconnect()

    assert not client._connected
    mock_backend.disconnect.assert_called_once()


@pytest.mark.asyncio
async def test_is_connected(mock_config):
    """Test connection status check."""
    client = TelegramClient(mock_config)

    assert not await client.is_connected()

    client._connected = True
    assert await client.is_connected()


@pytest.mark.asyncio
async def test_send_message(mock_config):
    """Test sending a message."""
    mock_config.policy = AccessPolicy.permissive()
    client = TelegramClient(mock_config)
    client._connected = True

    # Mock backend
    mock_backend = AsyncMock()
    mock_backend.send_message = AsyncMock(
        return_value={
            "peer": "@test",
            "text": "Hello",
            "sent": True,
        }
    )
    client._backend = mock_backend

    result = await client.send_message("@test", "Hello")

    assert result["sent"] is True
    mock_backend.send_message.assert_called_once_with("@test", "Hello")


@pytest.mark.asyncio
async def test_send_message_not_connected(mock_config):
    """Test sending message when not connected."""
    client = TelegramClient(mock_config)

    with pytest.raises(TGConnectionError):
        await client.send_message("@test", "Hello")


@pytest.mark.asyncio
async def test_get_dialogs(mock_config):
    """Test getting dialogs."""
    client = TelegramClient(mock_config)
    client._connected = True

    # Mock backend
    mock_backend = AsyncMock()
    mock_backend.get_dialogs = AsyncMock(
        return_value=[
            {"title": "Chat 1"},
            {"title": "Chat 2"},
        ]
    )
    client._backend = mock_backend

    result = await client.get_dialogs(limit=10)

    assert len(result) == 2
    mock_backend.get_dialogs.assert_called_once_with(10)


@pytest.mark.asyncio
async def test_context_manager(mock_config):
    """Test async context manager."""
    # Mock backend
    mock_backend = AsyncMock()
    mock_backend.connect = AsyncMock(return_value=True)
    mock_backend.disconnect = AsyncMock()

    async with TelegramClient(mock_config, backend=mock_backend) as client:
        assert client._connected
        mock_backend.connect.assert_called_once()

    assert not client._connected
    mock_backend.disconnect.assert_called_once()
