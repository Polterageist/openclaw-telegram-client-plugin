"""Main Telegram client implementation."""

import asyncio
import logging
from typing import List, Optional

from telethon import TelegramClient as TelethonClient

from .config import Config
from .exceptions import AuthenticationError, ConnectionError

logger = logging.getLogger(__name__)


class TelegramClient:
    """Telegram user account client."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize Telegram client.
        
        Args:
            config: Configuration object. If None, loads from .env
        """
        self.config = config or Config()
        
        if not self.config.validate():
            raise ValueError("Invalid configuration: missing API_ID, API_HASH, or PHONE_NUMBER")
        
        self._client: Optional[TelethonClient] = None
        self._connected = False

    async def connect(self) -> bool:
        """Connect to Telegram.
        
        Returns:
            True if connected, False otherwise
            
        Raises:
            ConnectionError: If connection fails
        """
        try:
            self._client = TelethonClient(
                self.config.session_name,
                self.config.api_id,
                self.config.api_hash,
            )
            
            await self._client.connect()
            self._connected = True
            logger.info("Connected to Telegram")
            return True
        
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise ConnectionError(f"Failed to connect to Telegram: {e}")

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self._client and self._connected:
            await self._client.disconnect()
            self._connected = False
            logger.info("Disconnected from Telegram")

    async def authenticate(self) -> bool:
        """Authenticate with Telegram.
        
        Prompts user for SMS code if not already authenticated.
        
        Returns:
            True if authenticated, False otherwise
            
        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            if not self._connected:
                await self.connect()
            
            if await self._client.is_user_authorized():
                logger.info("Already authorized")
                return True
            
            # Request code
            await self._client.send_code_request(self.config.phone_number)
            
            # Get code from user
            code = input("Enter the code you received via SMS: ")
            
            # Sign in
            await self._client.sign_in(self.config.phone_number, code)
            
            logger.info("Authentication successful")
            return True
        
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise AuthenticationError(f"Authentication failed: {e}")

    async def is_authorized(self) -> bool:
        """Check if client is authorized.
        
        Returns:
            True if authorized, False otherwise
        """
        if not self._client:
            return False
        
        try:
            return await self._client.is_user_authorized()
        except Exception:
            return False

    async def get_dialogs(self, limit: int = 50) -> List[dict]:
        """Get user dialogs (chats).
        
        Args:
            limit: Maximum number of dialogs to return
            
        Returns:
            List of dialog dictionaries
        """
        if not self._client:
            raise ConnectionError("Not connected")
        
        dialogs = []
        async for dialog in self._client.iter_dialogs(limit=limit):
            dialogs.append({
                'id': dialog.id,
                'title': dialog.title,
                'unread': dialog.unread_count,
                'pinned': dialog.pinned,
                'is_group': dialog.is_group,
                'is_channel': dialog.is_channel,
            })
        
        return dialogs

    async def get_messages(
        self,
        peer: str,
        limit: int = 100,
        min_id: int = 0,
    ) -> List[dict]:
        """Get messages from a chat.
        
        Args:
            peer: Chat username, ID, or alias
            limit: Maximum number of messages
            min_id: Minimum message ID to retrieve
            
        Returns:
            List of message dictionaries
        """
        if not self._client:
            raise ConnectionError("Not connected")
        
        messages = []
        try:
            entity = await self._client.get_entity(peer)
            async for message in self._client.iter_messages(entity, limit=limit, min_id=min_id):
                messages.append({
                    'id': message.id,
                    'text': message.text,
                    'sender': getattr(message.sender, 'username', 'Unknown') if message.sender else 'Unknown',
                    'date': message.date.isoformat() if message.date else None,
                    'media': message.media is not None,
                })
        
        except Exception as e:
            logger.error(f"Failed to get messages from {peer}: {e}")
            raise
        
        return messages

    async def send_message(self, peer: str, text: str) -> dict:
        """Send a message.
        
        Args:
            peer: Chat username, ID, or alias
            text: Message text
            
        Returns:
            Message dictionary
        """
        if not self._client:
            raise ConnectionError("Not connected")
        
        try:
            message = await self._client.send_message(peer, text)
            
            return {
                'id': message.id,
                'text': message.text,
                'date': message.date.isoformat() if message.date else None,
            }
        
        except Exception as e:
            logger.error(f"Failed to send message to {peer}: {e}")
            raise

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
