"""OpenClaw Telegram Client Plugin.

A user-account Telegram client for OpenClaw integration.
"""

__version__ = "0.1.0"
__author__ = "Aleksandr"

from .client import TelegramClient
from .config import Config
from .exceptions import TelegramClientError, AuthenticationError, ConnectionError

__all__ = [
    "TelegramClient",
    "Config",
    "TelegramClientError",
    "AuthenticationError",
    "ConnectionError",
]
