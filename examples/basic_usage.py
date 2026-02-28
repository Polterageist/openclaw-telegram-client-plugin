"""Basic usage examples for Telegram client."""

import asyncio
from openclaw_telegram import TelegramClient


async def example_send_message():
    """Example: Send a message."""
    client = TelegramClient()
    
    try:
        await client.connect()
        
        # Send message
        message = await client.send_message("@username", "Hello!")
        print(f"Message sent: {message}")
        
    finally:
        await client.disconnect()


async def example_get_dialogs():
    """Example: Get list of chats."""
    client = TelegramClient()
    
    try:
        await client.connect()
        
        # Get recent dialogs
        dialogs = await client.get_dialogs(limit=10)
        
        for dialog in dialogs:
            print(f"{dialog['title']}: {dialog['unread']} unread")
    
    finally:
        await client.disconnect()


async def example_get_messages():
    """Example: Get messages from a chat."""
    client = TelegramClient()
    
    try:
        await client.connect()
        
        # Get messages
        messages = await client.get_messages("@channel", limit=20)
        
        for msg in messages:
            print(f"{msg['sender']}: {msg['text'][:50]}...")
    
    finally:
        await client.disconnect()


async def example_context_manager():
    """Example: Using context manager."""
    async with TelegramClient() as client:
        await client.authenticate()
        
        dialogs = await client.get_dialogs(limit=5)
        for dialog in dialogs:
            print(f"Chat: {dialog['title']}")


if __name__ == "__main__":
    print("Uncomment an example to run it\n")
    
    # asyncio.run(example_send_message())
    # asyncio.run(example_get_dialogs())
    # asyncio.run(example_get_messages())
    # asyncio.run(example_context_manager())
