"""Custom exceptions for Telegram client."""


class TelegramClientError(Exception):
    """Base exception for Telegram client."""

    pass


class AuthenticationError(TelegramClientError):
    """Authentication failed."""

    pass


class ConnectionError(TelegramClientError):
    """Connection error."""

    pass


class MessageError(TelegramClientError):
    """Error sending/receiving message."""

    pass


class RateLimitError(TelegramClientError):
    """Rate limit exceeded."""

    pass


class NotFoundError(TelegramClientError):
    """Resource not found."""

    pass
