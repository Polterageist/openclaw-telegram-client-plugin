"""Click CLI for telegram client."""

import asyncio
import click
from pathlib import Path

from .client import TelegramClient
from .config import Config


@click.group()
def main():
    """Telegram client CLI."""
    pass


@main.command()
@click.option('--env', type=click.Path(), help='Path to .env file')
def auth(env):
    """Authenticate with Telegram."""
    config = Config(Path(env) if env else None)
    
    if not config.validate():
        click.echo("❌ Missing configuration: API_ID, API_HASH, PHONE_NUMBER")
        return
    
    async def do_auth():
        client = TelegramClient(config)
        await client.connect()
        await client.authenticate()
    
    try:
        asyncio.run(do_auth())
        click.echo("✅ Authenticated!")
    except Exception as e:
        click.echo(f"❌ Authentication failed: {e}")


@main.command()
@click.option('--peer', prompt='Chat username/ID', help='Target chat')
@click.option('--text', prompt='Message text', help='Message to send')
@click.option('--env', type=click.Path(), help='Path to .env file')
def send(peer, text, env):
    """Send a message."""
    config = Config(Path(env) if env else None)
    
    async def do_send():
        client = TelegramClient(config)
        await client.connect()
        await client.authenticate()
        message = await client.send_message(peer, text)
        await client.disconnect()
        return message
    
    try:
        message = asyncio.run(do_send())
        click.echo(f"✅ Message sent (ID: {message['id']})")
    except Exception as e:
        click.echo(f"❌ Failed to send message: {e}")


@main.command()
def version():
    """Show version."""
    from . import __version__
    click.echo(f"telegram-client v{__version__}")


if __name__ == '__main__':
    main()
