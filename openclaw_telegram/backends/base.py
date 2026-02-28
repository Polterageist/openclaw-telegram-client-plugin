"""Abstract backend interface for Telegram operations."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseBackend(ABC):
    """Abstract base class for Telegram backends.

    Implementations: telegram-cli, Telethon, etc.
    """

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to Telegram."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from Telegram."""
        pass

    @abstractmethod
    async def is_connected(self) -> bool:
        """Check connection status."""
        pass

    @abstractmethod
    async def get_dialogs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user dialogs (chats)."""
        pass

    @abstractmethod
    async def get_messages(
        self,
        peer: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get messages from a chat."""
        pass

    @abstractmethod
    async def send_message(self, peer: str, text: str) -> Dict[str, Any]:
        """Send a message."""
        pass
