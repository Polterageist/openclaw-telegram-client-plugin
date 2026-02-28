"""Configuration management.

Supports both telegram-cli (default) and Telethon backends.
"""

import os
from pathlib import Path
from typing import Optional, Literal

from dotenv import load_dotenv

from .policies import AccessPolicy


class Config:
    """Configuration for Telegram client.
    
    Supports:
    - telegram-cli backend (default, no secrets needed)
    - Telethon backend (advanced, with APP_ID/HASH for personal use)
    """

    def __init__(self, env_path: Optional[Path] = None):
        """Load configuration from .env or environment variables."""
        if env_path is None:
            env_path = Path(__file__).parent.parent / ".env"

        if env_path.exists():
            load_dotenv(env_path)

        # Backend selection
        self.backend = os.getenv("BACKEND", "tg_cli").lower()  # "tg_cli" or "telethon"
        
        # ===== telegram-cli (default) =====
        self.tg_cli_path = os.getenv("TG_CLI_PATH", "tg")
        self.tg_config_dir = Path(os.getenv("TG_CONFIG_DIR", str(Path.home() / ".telegram-cli")))
        
        # ===== Telethon (advanced, optional) =====
        self.telethon_api_id = os.getenv("TELETHON_API_ID", "")
        self.telethon_api_hash = os.getenv("TELETHON_API_HASH", "")
        self.telethon_phone = os.getenv("PHONE_NUMBER", "")
        self.telethon_session = os.getenv("TELETHON_SESSION", "telethon_session")
        self.telethon_qr_timeout = int(os.getenv("TELETHON_QR_TIMEOUT", "300"))
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Access control policies
        self.policy = AccessPolicy.read_only()  # Default: read-only

    def validate(self) -> bool:
        """Validate configuration."""
        if self.backend == "telethon":
            return bool(self.telethon_api_id and self.telethon_api_hash and self.telethon_phone)
        else:  # tg_cli
            return True  # No validation needed

    def use_telethon(self) -> bool:
        """Check if Telethon backend should be used."""
        return self.backend == "telethon" and self.validate()

    def __repr__(self) -> str:
        return (
            f"Config(backend={self.backend}, "
            f"policy={self.policy})"
        )
