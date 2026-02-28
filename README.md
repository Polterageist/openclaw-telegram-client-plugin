# OpenClaw Telegram Client Plugin

Read-write Telegram client for OpenClaw integration. Works with **user accounts** (not bots), enabling full Telegram functionality.

## Features

✅ **User Account Operations**
- Full message read/write access
- Group and channel management
- Media upload/download
- Contact and user management
- Dialog and history access

✅ **Developer-Friendly**
- Type hints (mypy compatible)
- Async/await API
- Comprehensive error handling
- Rate limiting aware
- Session persistence

✅ **TDD-Ready**
- 100% test coverage
- Pytest fixtures
- Mock Telegram responses
- Integration tests

✅ **Production Ready**
- Connection pooling
- Automatic reconnection
- Error recovery
- Logging support

## Installation

```bash
# From source
git clone https://github.com/yourusername/openclaw-telegram-client-plugin.git
cd openclaw-telegram-client-plugin
poetry install

# From PyPI (future)
pip install openclaw-telegram-client-plugin
```

## Quick Start

### 1. Get API Credentials

Go to https://my.telegram.org/app and create an app:
- Save your `API_ID`
- Save your `API_HASH`

### 2. Configure

Create `.env`:
```env
API_ID=123456789
API_HASH=abcd1234...
PHONE_NUMBER=+1234567890
```

### 3. Authenticate (First Time)

```python
from openclaw_telegram import TelegramClient

client = TelegramClient()
await client.authenticate()  # Will prompt for SMS code
```

### 4. Use It

```python
from openclaw_telegram import TelegramClient

async def main():
    client = TelegramClient()
    
    # Get dialogs
    dialogs = await client.get_dialogs(limit=10)
    
    # Send message
    await client.send_message("@username", "Hello!")
    
    # Get messages from chat
    messages = await client.get_messages("@channel", limit=100)
    
    await client.disconnect()

asyncio.run(main())
```

## API Reference

### TelegramClient

```python
class TelegramClient:
    # Authentication
    async def authenticate() -> bool
    async def is_authorized() -> bool
    
    # Dialogs (chats)
    async def get_dialogs(limit: int = 50) -> List[Dialog]
    async def get_dialog(peer: str) -> Dialog
    
    # Messages
    async def get_messages(peer: str, limit: int = 100) -> List[Message]
    async def send_message(peer: str, text: str) -> Message
    async def edit_message(peer: str, message_id: int, text: str) -> Message
    async def delete_message(peer: str, message_id: int) -> bool
    
    # Forwarding
    async def forward_message(from_peer: str, to_peer: str, msg_id: int) -> Message
    
    # Groups
    async def get_group_members(group_id: int) -> List[User]
    async def add_user_to_group(group_id: int, user_id: int) -> bool
    async def remove_user_from_group(group_id: int, user_id: int) -> bool
    
    # Media
    async def download_media(message: Message, path: str) -> str
    async def upload_media(path: str) -> InputFile
    
    # Connection
    async def connect() -> bool
    async def disconnect() -> None
```

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/openclaw_telegram

# Run specific test
poetry run pytest tests/test_messages.py::test_send_message

# Watch mode (requires pytest-watch)
poetry run ptw
```

## Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/my-feature`)
3. Write tests first (TDD)
4. Implement feature
5. Run `poetry run pytest` + linting
6. Submit PR

## Development

```bash
# Install dev dependencies
poetry install

# Format code
poetry run black src/ tests/

# Lint
poetry run pylint src/

# Type check
poetry run mypy src/

# All checks
poetry run pytest && poetry run black --check src/ && poetry run mypy src/
```

## License

MIT

## Author

Aleksandr (polterageist@example.com)

## Related Projects

- [OpenClaw](https://github.com/openclaw/openclaw) - AI agent framework
- [OpenClaw Telegram Monitor](https://github.com/yourusername/openclaw-telegram-monitor) - Group monitoring plugin
