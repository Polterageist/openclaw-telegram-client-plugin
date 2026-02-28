"""Configuration management."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Configuration from environment."""

    def __init__(self, env_path: Optional[Path] = None):
        """Load configuration from .env or environment variables."""
        if env_path is None:
            env_path = Path(__file__).parent.parent.parent / ".env"

        if env_path.exists():
            load_dotenv(env_path)

        self.api_id = int(os.getenv("API_ID", "0"))
        self.api_hash = os.getenv("API_HASH", "")
        self.phone_number = os.getenv("PHONE_NUMBER", "")
        self.session_name = os.getenv("SESSION_NAME", "telegram_session")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self) -> bool:
        """Check if configuration is valid."""
        return bool(self.api_id and self.api_hash and self.phone_number)

    def __repr__(self) -> str:
        return (
            f"Config(api_id={self.api_id}, "
            f"phone={self.phone_number[:10]}..., "
            f"session={self.session_name})"
        )
