"""Telegram user account client (via telegram-cli backend).

High-level interface for Telegram operations.
"""

import logging
from typing import List, Optional, Dict, Any

from .config import Config
from .tg_cli import TelegramCLIClient
from .exceptions import ConnectionError

logger = logging.getLogger(__name__)


class TelegramClient:
    """High-level Telegram user account client.
    
    Uses telegram-cli as backend (no APP_ID/APP_HASH needed).
    User manages credentials locally via telegram-cli setup.
    """

    def __init__(self, config: Optional[Config] = None, backend: Optional[TelegramCLIClient] = None):
        """Initialize Telegram client.
        
        Args:
            config: Configuration object. If None, loads from .env
            backend: Backend implementation. If None, uses TelegramCLIClient
        """
        self.config = config or Config()
        self._backend = backend or TelegramCLIClient(self.config)
        self._connected = False

    async def connect(self) -> bool:
        """Connect to Telegram.
        
        Returns:
            True if connected
            
        Raises:
            ConnectionError: If connection fails
        """
        result = await self._backend.connect()
        self._connected = result
        return result

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        await self._backend.disconnect()
        self._connected = False

    async def is_connected(self) -> bool:
        """Check if client is connected.
        
        Returns:
            True if connected
        """
        return self._connected

    async def get_dialogs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user dialogs (chats).
        
        Args:
            limit: Maximum number of dialogs to return
            
        Returns:
            List of dialog dictionaries
            
        Raises:
            ConnectionError: If not connected
        """
        if not self._connected:
            raise ConnectionError("Not connected")
        
        return await self._backend.get_dialogs(limit)

    async def get_messages(
        self,
        peer: str,
        limit: int = 100,
        min_id: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get messages from a chat.
        
        Args:
            peer: Chat name, ID, or username
            limit: Maximum number of messages
            min_id: Minimum message ID (for pagination)
            
        Returns:
            List of message dictionaries
            
        Raises:
            ConnectionError: If not connected
        """
        if not self._connected:
            raise ConnectionError("Not connected")
        
        return await self._backend.get_messages(peer, limit)

    async def send_message(self, peer: str, text: str) -> Dict[str, Any]:
        """Send a message.
        
        Args:
            peer: Chat name, ID, or username
            text: Message text
            
        Returns:
            Message dictionary
            
        Raises:
            ConnectionError: If not connected
            MessageError: If sending fails
        """
        if not self._connected:
            raise ConnectionError("Not connected")
        
        return await self._backend.send_message(peer, text)

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
