"""Wrapper around telegram-cli (tg) for user account operations.

telegram-cli (https://github.com/vysheng/tg) is a standalone CLI for Telegram.
No APP_ID/APP_HASH needed - user manages credentials locally.
"""

import asyncio
import json
import logging
import subprocess
from typing import List, Optional, Dict, Any

from .config import Config
from .exceptions import (
    ConnectionError as TGConnectionError,
    AuthenticationError,
    MessageError,
)

logger = logging.getLogger(__name__)


class TelegramCLIClient:
    """Async wrapper around telegram-cli.
    
    Uses subprocess to communicate with tg binary.
    User creates own APP_ID via Telegram (or uses default).
    """

    def __init__(self, config: Optional[Config] = None):
        """Initialize client.
        
        Args:
            config: Configuration object. If None, loads from .env
        """
        self.config = config or Config()
        self._connected = False
        self._process: Optional[subprocess.Popen] = None

    async def connect(self) -> bool:
        """Start telegram-cli subprocess.
        
        Returns:
            True if connected
            
        Raises:
            ConnectionError: If telegram-cli not found or fails to start
        """
        try:
            # Start tg process
            self._process = subprocess.Popen(
                [self.config.tg_cli_path, "-D"],  # -D for daemon
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
            )
            
            self._connected = True
            logger.info("Connected to telegram-cli")
            return True
        
        except FileNotFoundError:
            logger.error(f"telegram-cli not found: {self.config.tg_cli_path}")
            raise TGConnectionError(
                f"telegram-cli binary not found at {self.config.tg_cli_path}. "
                "Install from: https://github.com/vysheng/tg"
            )
        except Exception as e:
            logger.error(f"Failed to start telegram-cli: {e}")
            raise TGConnectionError(f"Failed to connect: {e}")

    async def disconnect(self) -> None:
        """Stop telegram-cli subprocess."""
        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=5)
                self._connected = False
                logger.info("Disconnected from telegram-cli")
            except subprocess.TimeoutExpired:
                self._process.kill()
                logger.warning("Force-killed telegram-cli")

    async def _run_command(self, command: str) -> str:
        """Run a command in telegram-cli and return output.
        
        Args:
            command: Command to send to tg
            
        Returns:
            Command output
        """
        if not self._connected or not self._process:
            raise TGConnectionError("Not connected")
        
        try:
            stdout, stderr = self._process.communicate(
                input=f"{command}\n",
                timeout=10
            )
            
            if stderr:
                logger.warning(f"tg stderr: {stderr}")
            
            return stdout.strip()
        
        except subprocess.TimeoutExpired:
            raise TGConnectionError("Command timeout")

    async def get_dialogs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user dialogs (chats).
        
        Args:
            limit: Maximum dialogs to return
            
        Returns:
            List of dialog info dicts
        """
        output = await self._run_command("dialog_list")
        
        dialogs = []
        for line in output.split("\n"):
            if line.strip():
                # Parse tg output (format varies)
                dialogs.append({"title": line})
        
        return dialogs[:limit]

    async def get_messages(
        self,
        peer: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get messages from a chat.
        
        Args:
            peer: Chat name/ID
            limit: Number of messages
            
        Returns:
            List of message dicts
        """
        output = await self._run_command(f"history {peer} {limit}")
        
        messages = []
        for line in output.split("\n"):
            if line.strip():
                messages.append({"text": line})
        
        return messages

    async def send_message(self, peer: str, text: str) -> Dict[str, Any]:
        """Send a message.
        
        Args:
            peer: Chat name/ID
            text: Message text
            
        Returns:
            Message info dict
            
        Raises:
            MessageError: If send fails
        """
        try:
            output = await self._run_command(f'msg {peer} "{text}"')
            
            return {
                "peer": peer,
                "text": text,
                "sent": True,
                "output": output,
            }
        
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise MessageError(f"Failed to send: {e}")

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
