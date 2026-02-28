"""Telethon-based backend (advanced, with QR code authorization)."""

import logging
from typing import List, Dict, Any, Optional

try:
    from telethon import TelegramClient
    from telethon.errors import SessionPasswordNeededError
except ImportError:
    raise ImportError(
        "Telethon backend requires telethon. "
        "Install with: pip install telethon qrcode"
    )

from .base import BaseBackend
from ..exceptions import ConnectionError as TGConnectionError, AuthenticationError

logger = logging.getLogger(__name__)


class TelethonBackend(BaseBackend):
    """Telethon-based backend with QR code authorization.
    
    Advanced backend for advanced users with their own APP_ID/HASH.
    Supports QR code login for convenience.
    """

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        phone_number: str,
        session_name: str = "telethon_session",
    ):
        """Initialize Telethon backend.
        
        Args:
            api_id: Telegram API ID
            api_hash: Telegram API hash
            phone_number: Phone number for login
            session_name: Session file name
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_name = session_name
        self._client: Optional[TelegramClient] = None
        self._connected = False

    async def connect(self) -> bool:
        """Connect to Telegram.
        
        Raises:
            ConnectionError: If connection fails
        """
        try:
            self._client = TelegramClient(
                self.session_name,
                self.api_id,
                self.api_hash,
            )
            
            await self._client.connect()
            self._connected = True
            logger.info("Connected to Telegram via Telethon")
            return True
        
        except Exception as e:
            logger.error(f"Telethon connection failed: {e}")
            raise TGConnectionError(f"Telethon connection failed: {e}")

    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        if self._client and self._connected:
            await self._client.disconnect()
            self._connected = False
            logger.info("Disconnected from Telegram")

    async def is_connected(self) -> bool:
        """Check if connected."""
        return self._connected

    async def authorize_qr(self, timeout: int = 300) -> bool:
        """Authorize with QR code.
        
        Args:
            timeout: QR code timeout in seconds (default 5 minutes)
            
        Returns:
            True if authorized
            
        Raises:
            AuthenticationError: If authorization fails
        """
        if not self._client:
            raise TGConnectionError("Not connected")
        
        try:
            if await self._client.is_user_authorized():
                logger.info("Already authorized")
                return True
            
            logger.info("Starting QR code authorization...")
            qr_login = await self._client.qr_login()
            
            logger.info(f"QR Code URL: {qr_login.url}")
            logger.info("Scan with your Telegram app or open the URL above")
            logger.info(f"Waiting for authorization (timeout: {timeout}s)...")
            
            user = await qr_login.wait(timeout=timeout)
            
            logger.info(f"✅ Authorized as {user.first_name} {user.last_name or ''}")
            return True
        
        except SessionPasswordNeededError:
            logger.error("2FA enabled - not supported for QR login")
            raise AuthenticationError(
                "2FA is enabled. Please use phone/code login instead."
            )
        except Exception as e:
            logger.error(f"QR authorization failed: {e}")
            raise AuthenticationError(f"Authorization failed: {e}")

    async def authorize_code(self) -> bool:
        """Authorize with phone number and code (fallback).
        
        Returns:
            True if authorized
            
        Raises:
            AuthenticationError: If authorization fails
        """
        if not self._client:
            raise TGConnectionError("Not connected")
        
        try:
            if await self._client.is_user_authorized():
                logger.info("Already authorized")
                return True
            
            logger.info(f"Sending code to {self.phone_number}...")
            await self._client.send_code_request(self.phone_number)
            
            code = input("Enter the code you received: ")
            
            user = await self._client.sign_in(self.phone_number, code)
            
            logger.info(f"✅ Authorized as {user.first_name}")
            return True
        
        except SessionPasswordNeededError:
            password = input("2FA Password: ")
            user = await self._client.sign_in(password=password)
            logger.info(f"✅ Authorized with 2FA")
            return True
        
        except Exception as e:
            logger.error(f"Code authorization failed: {e}")
            raise AuthenticationError(f"Authorization failed: {e}")

    async def get_dialogs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user dialogs."""
        if not self._connected or not self._client:
            raise TGConnectionError("Not connected")
        
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
    ) -> List[Dict[str, Any]]:
        """Get messages from a chat."""
        if not self._connected or not self._client:
            raise TGConnectionError("Not connected")
        
        messages = []
        try:
            entity = await self._client.get_entity(peer)
            async for message in self._client.iter_messages(entity, limit=limit):
                messages.append({
                    'id': message.id,
                    'text': message.text,
                    'sender': (
                        getattr(message.sender, 'username', None)
                        or getattr(message.sender, 'first_name', 'Unknown')
                    ),
                    'date': message.date.isoformat() if message.date else None,
                    'media': message.media is not None,
                })
        
        except Exception as e:
            logger.error(f"Failed to get messages from {peer}: {e}")
            raise
        
        return messages

    async def send_message(self, peer: str, text: str) -> Dict[str, Any]:
        """Send a message."""
        if not self._connected or not self._client:
            raise TGConnectionError("Not connected")
        
        try:
            message = await self._client.send_message(peer, text)
            
            return {
                'id': message.id,
                'text': message.text,
                'date': message.date.isoformat() if message.date else None,
            }
        
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise
