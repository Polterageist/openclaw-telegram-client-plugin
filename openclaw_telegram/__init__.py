"""OpenClaw Telegram Client Plugin (telegram-cli wrapper).

No APP_ID/APP_HASH needed. User manages credentials locally via telegram-cli.
"""

__version__ = "0.2.0"
__author__ = "Aleksandr"

from .client import TelegramClient
from .config import Config
from .exceptions import (
    TelegramClientError,
    AuthenticationError,
    ConnectionError,
    MessageError,
    RateLimitError,
    NotFoundError,
)

__all__ = [
    "TelegramClient",
    "Config",
    "TelegramClientError",
    "AuthenticationError",
    "ConnectionError",
    "MessageError",
    "RateLimitError",
    "NotFoundError",
]
