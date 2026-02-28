"""telegram-cli-based backend (default, safe, no APP_ID needed)."""

import asyncio
import json
import logging
import subprocess
from typing import List, Dict, Any, Optional

from .base import BaseBackend
from ..exceptions import ConnectionError as TGConnectionError, MessageError

logger = logging.getLogger(__name__)


class TGCLIBackend(BaseBackend):
    """telegram-cli subprocess wrapper.

    Default backend: safe, no APP_ID/HASH needed, user manages credentials locally.
    """

    def __init__(self, tg_cli_path: str = "tg", config_dir: str = "~/.telegram-cli"):
        """Initialize telegram-cli backend.

        Args:
            tg_cli_path: Path to telegram-cli binary
            config_dir: Config directory for telegram-cli
        """
        self.tg_cli_path = tg_cli_path
        self.config_dir = config_dir
        self._connected = False
        self._process: Optional[subprocess.Popen] = None

    async def connect(self) -> bool:
        """Start telegram-cli subprocess.

        Raises:
            ConnectionError: If telegram-cli not found or fails
        """
        try:
            self._process = subprocess.Popen(
                [self.tg_cli_path, "-D"],  # -D for daemon
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            self._connected = True
            logger.info("Connected via telegram-cli")
            return True

        except FileNotFoundError:
            logger.error(f"telegram-cli not found: {self.tg_cli_path}")
            raise TGConnectionError(
                f"telegram-cli not found. Install from: https://github.com/vysheng/tg"
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

    async def is_connected(self) -> bool:
        """Check if connected."""
        return self._connected

    async def _run_command(self, command: str) -> str:
        """Run command in telegram-cli."""
        if not self._connected or not self._process:
            raise TGConnectionError("Not connected")

        try:
            stdout, stderr = self._process.communicate(input=f"{command}\n", timeout=10)

            if stderr:
                logger.debug(f"tg stderr: {stderr}")

            return str(stdout).strip() if stdout else ""

        except subprocess.TimeoutExpired:
            raise TGConnectionError("Command timeout")

    async def get_dialogs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get dialogs via telegram-cli."""
        output = await self._run_command("dialog_list")

        dialogs = []
        for line in output.split("\n")[:limit]:
            if line.strip():
                dialogs.append({"title": line})

        return dialogs

    async def get_messages(
        self,
        peer: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get messages via telegram-cli."""
        output = await self._run_command(f"history {peer} {limit}")

        messages = []
        for line in output.split("\n"):
            if line.strip():
                messages.append({"text": line})

        return messages

    async def send_message(self, peer: str, text: str) -> Dict[str, Any]:
        """Send message via telegram-cli."""
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
