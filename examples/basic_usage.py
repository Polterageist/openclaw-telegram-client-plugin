"""Basic usage examples for Telegram client (telegram-cli wrapper)."""

import asyncio
from openclaw_telegram import TelegramClient


async def example_send_message():
    """Example: Send a message."""
    async with TelegramClient() as client:
        # Send message
        result = await client.send_message("@username", "Hello!")
        print(f"Sent: {result}")


async def example_get_dialogs():
    """Example: Get list of chats."""
    async with TelegramClient() as client:
        # Get recent dialogs
        dialogs = await client.get_dialogs(limit=10)
        
        print(f"Your chats ({len(dialogs)}):")
        for dialog in dialogs:
            print(f"  - {dialog['title']}")


async def example_get_messages():
    """Example: Get messages from a chat."""
    async with TelegramClient() as client:
        # Get messages
        messages = await client.get_messages("@channel", limit=20)
        
        print(f"Messages ({len(messages)}):")
        for msg in messages:
            print(f"  {msg['text'][:50]}...")


async def example_with_error_handling():
    """Example: With error handling."""
    try:
        async with TelegramClient() as client:
            dialogs = await client.get_dialogs(limit=5)
            
            for dialog in dialogs:
                print(f"Chat: {dialog['title']}")
                
                # Get messages from each chat
                messages = await client.get_messages(
                    dialog['title'],
                    limit=3
                )
                
                for msg in messages:
                    print(f"  Message: {msg['text'][:40]}...")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("  1. telegram-cli is installed")
        print("  2. Session initialized (run 'tg' once)")
        print("  3. ~/.telegram-cli/ exists")


if __name__ == "__main__":
    print("Uncomment an example below to run it\n")
    
    # asyncio.run(example_send_message())
    # asyncio.run(example_get_dialogs())
    # asyncio.run(example_get_messages())
    # asyncio.run(example_with_error_handling())
    
    print("""
    Available examples:
    - example_send_message()
    - example_get_dialogs()
    - example_get_messages()
    - example_with_error_handling()
    
    Uncomment one and run to see it in action!
    """)
