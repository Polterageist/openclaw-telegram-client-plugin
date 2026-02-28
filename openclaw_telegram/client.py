"""High-level Telegram client with policy support.

Supports both telegram-cli and Telethon backends.
Default: telegram-cli (safe, no secrets).
Optional: Telethon (advanced features like QR login).
"""

import logging
from typing import List, Optional, Dict, Any, Type

from .config import Config
from .policies import AccessPolicy, ChatType
from .exceptions import ConnectionError
from .backends.base import BaseBackend
from .backends.tg_cli_backend import TGCLIBackend

# Optional Telethon backend
try:
    from .backends.telethon_backend import TelethonBackend
except ImportError:
    TelethonBackend = None  # type: ignore

logger = logging.getLogger(__name__)


class TelegramClient:
    """High-level Telegram client.

    Features:
    - Multiple backends (telegram-cli, Telethon)
    - Access control policies
    - Default: read-only for all
    """

    def __init__(self, config: Optional[Config] = None, backend: Optional[BaseBackend] = None):
        """Initialize Telegram client.

        Args:
            config: Configuration object. If None, loads from .env
            backend: Backend implementation. If None, auto-selects based on config
        """
        self.config = config or Config()

        if backend:
            self._backend = backend
        else:
            # Auto-select backend
            if self.config.use_telethon():
                if TelethonBackend is None:
                    raise ImportError("Telethon backend requires: pip install telethon qrcode")
                self._backend = TelethonBackend(
                    api_id=int(self.config.telethon_api_id),
                    api_hash=self.config.telethon_api_hash,
                    phone_number=self.config.telethon_phone,
                    session_name=self.config.telethon_session,
                )
                logger.info("Using Telethon backend")
            else:
                self._backend = TGCLIBackend(
                    tg_cli_path=self.config.tg_cli_path,
                    config_dir=str(self.config.tg_config_dir),
                )
                logger.info("Using telegram-cli backend")

        self._connected = False

    async def connect(self) -> bool:
        """Connect to Telegram.

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
        """Check if client is connected."""
        return self._connected

    async def authorize_qr(self, timeout: int = 300) -> bool:
        """Authorize using QR code (Telethon only).

        Args:
            timeout: QR code timeout in seconds

        Returns:
            True if authorized

        Raises:
            ConnectionError: If not Telethon backend
        """
        if not isinstance(self._backend, TelethonBackend):
            raise ConnectionError("QR authorization only available with Telethon backend")

        return await self._backend.authorize_qr(timeout=timeout)

    async def authorize_code(self) -> bool:
        """Authorize using phone number and code (Telethon only).

        Falls back for users with 2FA.
        """
        if not isinstance(self._backend, TelethonBackend):
            raise ConnectionError("Code authorization only available with Telethon backend")

        return await self._backend.authorize_code()

    async def get_dialogs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user dialogs with policy enforcement.

        Args:
            limit: Maximum dialogs to return

        Returns:
            List of accessible dialogs

        Raises:
            ConnectionError: If not connected
        """
        if not self._connected:
            raise ConnectionError("Not connected")

        all_dialogs = await self._backend.get_dialogs(limit)

        # Filter by policy
        filtered = []
        for d in all_dialogs:
            chat_id = d.get("id", 0)

            # Determine chat type
            if d.get("is_channel"):
                chat_type = ChatType.CHANNEL
            elif d.get("is_group"):
                chat_type = ChatType.GROUP
            else:
                chat_type = ChatType.DM

            # Check policy
            if self.config.policy.can_read(chat_id, chat_type):
                filtered.append(d)

        return filtered

    async def get_messages(
        self,
        peer: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get messages with policy enforcement.

        Args:
            peer: Chat identifier
            limit: Maximum messages

        Returns:
            List of accessible messages

        Raises:
            ConnectionError: If not connected
        """
        if not self._connected:
            raise ConnectionError("Not connected")

        # Check policy (we don't know chat_type without fetching, so check by ID if possible)
        # For now, check read access
        if not self.config.policy.can_read(0):  # Generic check
            logger.warning(f"Read access denied for {peer}")
            return []

        return await self._backend.get_messages(peer, limit)

    async def send_message(self, peer: str, text: str) -> Dict[str, Any]:
        """Send message with policy enforcement.

        Args:
            peer: Chat identifier
            text: Message text

        Returns:
            Message info dict

        Raises:
            ConnectionError: If not connected
            PermissionError: If write access denied
        """
        if not self._connected:
            raise ConnectionError("Not connected")

        # Check policy
        if not self.config.policy.can_write(0):  # Generic check
            raise PermissionError("Write access denied by policy")

        return await self._backend.send_message(peer, text)

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
