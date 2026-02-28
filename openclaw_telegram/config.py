"""Configuration management for telegram-cli."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Configuration for telegram-cli wrapper.
    
    Does NOT require APP_ID or APP_HASH (user manages via telegram-cli setup).
    """

    def __init__(self, env_path: Optional[Path] = None):
        """Load configuration from .env or environment variables."""
        if env_path is None:
            env_path = Path(__file__).parent.parent.parent / ".env"

        if env_path.exists():
            load_dotenv(env_path)

        # telegram-cli binary path
        self.tg_cli_path = os.getenv("TG_CLI_PATH", "tg")
        
        # Session/config directory
        self.tg_config_dir = Path(
            os.getenv("TG_CONFIG_DIR", str(Path.home() / ".telegram-cli"))
        )
        
        # Phone number (optional, for setup)
        self.phone_number = os.getenv("PHONE_NUMBER", "")
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self) -> bool:
        """Check if configuration is valid."""
        # Just need telegram-cli to be available
        return True

    def __repr__(self) -> str:
        return (
            f"Config(tg_cli={self.tg_cli_path}, "
            f"config_dir={self.tg_config_dir})"
        )
