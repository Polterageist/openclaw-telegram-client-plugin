"""Click CLI for telegram client."""

import asyncio
import click
from pathlib import Path

from .client import TelegramClient
from .config import Config


@click.group()
def main():
    """Telegram client CLI (telegram-cli wrapper)."""
    pass


@main.command()
@click.option("--env", type=click.Path(), help="Path to .env file")
def status(env):
    """Check if telegram-cli is available and configured."""
    config = Config(Path(env) if env else None)

    try:

        async def check():
            client = TelegramClient(config)
            connected = await client.is_connected()
            return connected

        # Try to check status
        click.echo(f"✅ Configuration:")
        click.echo(f"  tg_cli_path: {config.tg_cli_path}")
        click.echo(f"  config_dir: {config.tg_config_dir}")

        if config.tg_config_dir.exists():
            click.echo(f"  session: ✅ Found at {config.tg_config_dir}")
        else:
            click.echo(f"  session: ⚠️  Not found at {config.tg_config_dir}")
            click.echo(f"         Run 'tg' to initialize")

    except Exception as e:
        click.echo(f"❌ Configuration error: {e}")


@main.command()
@click.option("--peer", prompt="Recipient", help="Chat name/ID")
@click.option("--text", prompt="Message", help="Message text")
@click.option("--env", type=click.Path(), help="Path to .env file")
def send(peer, text, env):
    """Send a message."""
    config = Config(Path(env) if env else None)

    async def do_send():
        async with TelegramClient(config) as client:
            result = await client.send_message(peer, text)
            return result

    try:
        result = asyncio.run(do_send())
        click.echo(f"✅ Message sent to {peer}")
    except Exception as e:
        click.echo(f"❌ Failed to send: {e}")


@main.command()
@click.option("--limit", default=10, help="Number of dialogs to show")
@click.option("--env", type=click.Path(), help="Path to .env file")
def dialogs(limit, env):
    """List your chats."""
    config = Config(Path(env) if env else None)

    async def do_list():
        async with TelegramClient(config) as client:
            dialogs_list = await client.get_dialogs(limit=limit)
            return dialogs_list

    try:
        dialogs_list = asyncio.run(do_list())

        if not dialogs_list:
            click.echo("No dialogs found")
        else:
            click.echo(f"📱 Your chats ({len(dialogs_list)}):\n")
            for d in dialogs_list:
                click.echo(f"  • {d.get('title', 'Unknown')}")

    except Exception as e:
        click.echo(f"❌ Failed to list dialogs: {e}")


@main.command()
@click.option("--env", type=click.Path(), help="Path to .env file")
@click.option("--qr", is_flag=True, help="Use QR code instead of phone code")
def login(env, qr):
    """Authenticate with Telegram."""
    config = Config(Path(env) if env else None)

    async def do_login():
        async with TelegramClient(config) as client:
            if qr:
                # Use QR code
                try:
                    import qrcode
                    success = await client.authorize_qr()
                    return success
                except ImportError:
                    click.echo("❌ Error: 'qrcode' package not found. Install with: pip install qrcode")
                    return False
            else:
                # Use phone code
                success = await client.authorize_code()
                return success

    try:
        success = asyncio.run(do_login())
        if success:
            click.echo("✅ Login successful!")
        else:
            click.echo("❌ Login failed.")
    except Exception as e:
        click.echo(f"❌ Error during login: {e}")


@main.command()
def version():
    """Show version."""
    from . import __version__

    click.echo(f"telegram-client v{__version__}")


@main.command()
def setup():
    """Show setup instructions."""
    click.echo(
        """
    📱 Telegram Client Setup Guide
    ==============================
    
    1. Install telegram-cli:
       brew install telegram-cli      # macOS
       sudo apt-get install telegram-cli  # Ubuntu
    
    2. Initialize session (one-time):
       tg
       > +1234567890        # Your phone number
       > 12345              # Code from Telegram
       > quit
    
    3. Use the client:
       telegram-client dialogs      # List chats
       telegram-client send         # Send message
       
    4. Or use in Python:
       from openclaw_telegram import TelegramClient
       
       async with TelegramClient() as client:
           dialogs = await client.get_dialogs()
    
    All credentials stored locally in ~/.telegram-cli/
    No APP_ID/APP_HASH needed!
    """
    )


if __name__ == "__main__":
    main()
