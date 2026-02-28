# Quick Start (5 minutes)

## 1. Install telegram-cli

```bash
# macOS
brew install telegram-cli

# Ubuntu/Debian
sudo apt-get install telegram-cli

# Verify
tg -h
```

## 2. Initialize Telegram Session

```bash
# Run telegram-cli interactively (one-time setup)
tg

# You'll see:
# > 

# Type your phone number
> +1234567890

# You'll get a code via Telegram
> 12345  # (example code)

# You're in! Type 'quit' to exit
> quit
```

This creates `~/.telegram-cli/` with your session (one-time).

## 3. Install Plugin

```bash
git clone https://github.com/yourusername/openclaw-telegram-client-plugin
cd openclaw-telegram-client-plugin
poetry install
```

## 4. First Test

Create `test.py`:

```python
import asyncio
from openclaw_telegram import TelegramClient

async def main():
    client = TelegramClient()
    await client.connect()
    
    # Get your chats
    dialogs = await client.get_dialogs(limit=5)
    for d in dialogs:
        print(f"- {d['title']}")
    
    await client.disconnect()

asyncio.run(main())
```

Run:
```bash
poetry run python test.py
```

You should see your chats listed!

## 5. Send a Message

```python
import asyncio
from openclaw_telegram import TelegramClient

async def main():
    async with TelegramClient() as client:
        await client.send_message("@username", "Hello from Python!")

asyncio.run(main())
```

## API Cheatsheet

```python
async with TelegramClient() as client:
    # List chats
    dialogs = await client.get_dialogs(limit=20)
    
    # Get messages
    msgs = await client.get_messages("@username", limit=50)
    
    # Send message
    await client.send_message("@username", "text")
```

## Next Steps

- Read [README.md](README.md) for full API
- Check [examples/](examples/) for more patterns
- Run tests: `poetry run pytest`

---

**That's it! No APP_ID, no secrets in code.** 🔐
