# OpenClaw Telegram Client Plugin

Python wrapper around **telegram-cli** for user account operations. **No APP_ID/APP_HASH needed** — credentials managed locally.

## Key Difference from Telethon

✅ **No APP_ID exposure** — Each user runs telegram-cli locally  
✅ **Safe to publish** — No secrets in your code  
✅ **User controls credentials** — Telegram account security is user's responsibility  
✅ **Lightweight** — Just wraps existing telegram-cli binary  

## Requirements

- **telegram-cli** installed and in PATH
  ```bash
  # macOS
  brew install telegram-cli
  
  # Ubuntu/Debian
  sudo apt-get install telegram-cli
  
  # Build from source
  git clone https://github.com/vysheng/tg.git
  cd tg && ./configure && make
  ```

- Python 3.9+

## Installation

### 1. As a Python package (pip)
```bash
pip install openclaw-telegram-client-plugin
```

### 2. As an OpenClaw Skill (ClawHub)
```bash
openclaw skill install telegram-client
```

## Setup

### Step 1: Authentication
If using **Telethon backend** (default), run the interactive login:
```bash
telegram-client login
```
Follow the prompts to enter your phone number and confirm with the code received.

### Step 2: Configuration
Create a `.env` file or export environment variables:
```env
BACKEND=telethon
TELETHON_API_ID=your_id
TELETHON_API_HASH=your_hash
PHONE_NUMBER=+your_phone
```

### 3. Use via Python

```python
import asyncio
from openclaw_telegram import TelegramClient

async def main():
    client = TelegramClient()
    
    await client.connect()
    
    # Get dialogs
    dialogs = await client.get_dialogs(limit=10)
    for d in dialogs:
        print(d['title'])
    
    # Send message
    await client.send_message("@username", "Hello!")
    
    await client.disconnect()

asyncio.run(main())
```

## Project Structure

```
openclaw-telegram-client-plugin/
├── openclaw_telegram/           # Main module
│   ├── __init__.py             # Exports: TelegramClient, Config, exceptions
│   ├── client.py               # High-level API
│   ├── tg_cli.py               # telegram-cli subprocess wrapper
│   ├── config.py               # Configuration (no APP_ID needed!)
│   ├── cli.py                  # Click CLI commands
│   └── exceptions.py           # Custom exception types
├── tests/                       # Pytest test suite (TDD)
│   ├── conftest.py
│   ├── test_client.py
│   └── test_config.py
├── examples/                    # Real usage examples
│   └── basic_usage.py
├── .github/workflows/           # CI/CD (GitHub Actions)
├── pyproject.toml              # Poetry configuration
├── README.md                   # This file
├── QUICKSTART.md               # 5-minute setup guide
├── CONTRIBUTING.md             # Development guidelines
├── AGENTS.md                   # Agent behavior config
└── LICENSE (MIT)
```

## API Reference

### TelegramClient

```python
class TelegramClient:
    async def connect() -> bool
    async def disconnect() -> None
    async def is_connected() -> bool
    
    async def get_dialogs(limit: int = 50) -> List[Dict]
    async def get_messages(peer: str, limit: int = 100) -> List[Dict]
    async def send_message(peer: str, text: str) -> Dict
```

### Context Manager

```python
async with TelegramClient() as client:
    dialogs = await client.get_dialogs()
    # client auto-disconnects on exit
```

## Configuration

Create `.env` (optional):

```env
# Path to telegram-cli binary (if not in PATH)
TG_CLI_PATH=/usr/local/bin/tg

# Telegram-cli config directory
TG_CONFIG_DIR=~/.telegram-cli

# Your phone number
PHONE_NUMBER=+1234567890

# Logging level
LOG_LEVEL=INFO
```

## How It Works

1. **telegram-cli** (C binary) runs locally and manages Telegram connection
2. This plugin wraps tg via subprocess
3. All credentials stored locally (`~/.telegram-cli/`)
4. No APP_ID/APP_HASH in code = safe to publish

## Testing

```bash
poetry run pytest
poetry run pytest --cov=openclaw_telegram
```

## Development

```bash
# Format code
poetry run black openclaw_telegram/ tests/

# Type check
poetry run mypy openclaw_telegram/

# Lint
poetry run pylint openclaw_telegram/

# All checks
poetry run pytest && poetry run black --check . && poetry run mypy openclaw_telegram/
```

## Troubleshooting

**"telegram-cli: command not found"**
```bash
# Install telegram-cli
brew install telegram-cli  # or apt-get install

# Or set custom path
export TG_CLI_PATH=/path/to/tg
```

**"Could not connect"**
```bash
# Verify tg works standalone
tg -h

# Verify session exists
ls ~/.telegram-cli/
```

**"Authentication failed"**
```bash
# Re-run telegram-cli setup
tg
# Follow prompts, then exit
```

## Security

✅ **No secret keys in code**  
✅ **Credentials stored locally** in `~/.telegram-cli/`  
✅ **User controls Telegram account access**  
✅ **Safe to publish on GitHub**  

## Related Projects

- [telegram-cli](https://github.com/vysheng/tg) — Underlying CLI tool
- [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework
- [OpenClaw Telegram Monitor](https://github.com/yourusername/openclaw-telegram-monitor) — Group monitoring plugin

## License

MIT

## Author

Aleksandr (polterageist@example.com)

---

**Safe, simple, no secrets exposed.** 🔐
