# Quick Start

Get up and running in 5 minutes.

## 1. Install

```bash
git clone https://github.com/yourusername/openclaw-telegram-client-plugin
cd openclaw-telegram-client-plugin
poetry install
```

## 2. Configure

```bash
cp .env.example .env
# Edit .env with your API_ID, API_HASH, PHONE_NUMBER
```

Get credentials from https://my.telegram.org/app

## 3. First Run

```bash
poetry run telegram-client auth
```

You'll be prompted for an SMS code.

## 4. Send Your First Message

Create `test.py`:

```python
import asyncio
from openclaw_telegram import TelegramClient

async def main():
    client = TelegramClient()
    await client.connect()
    
    # Send message
    await client.send_message("@username", "Hello from Telegram client!")
    
    await client.disconnect()

asyncio.run(main())
```

Run it:
```bash
poetry run python test.py
```

## 5. Read Messages

```python
import asyncio
from openclaw_telegram import TelegramClient

async def main():
    client = TelegramClient()
    await client.connect()
    
    # Get recent messages from a chat
    messages = await client.get_messages("@username", limit=10)
    
    for msg in messages:
        print(f"{msg.sender}: {msg.text}")
    
    await client.disconnect()

asyncio.run(main())
```

## API Cheatsheet

```python
# Connect
await client.connect()

# Get dialogs (chats)
dialogs = await client.get_dialogs(limit=20)

# Send message
await client.send_message("@username", "text")

# Get messages
messages = await client.get_messages("@username", limit=100)

# Disconnect
await client.disconnect()
```

## Troubleshooting

**"Not authorized"**
```bash
rm session.session*
poetry run telegram-client auth
```

**"API rate limit"**
The client handles rate limiting automatically. If you hit limits, wait a few minutes.

**"Connection timeout"**
Check internet connection. Telegram servers might be slow.

## Next Steps

- Read [API Reference](README.md#api-reference)
- Run tests: `poetry run pytest`
