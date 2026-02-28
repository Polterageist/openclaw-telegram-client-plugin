# AGENTS.md - openclaw-telegram-client-plugin (v0.2: telegram-cli backend)

Unified configuration for all AI agents working on this project.

## Project Change (v0.2)

**Migrated from Telethon to telegram-cli:**
- ✅ No APP_ID/APP_HASH exposure
- ✅ Safe to publish on GitHub
- ✅ User manages credentials locally
- ✅ Lightweight subprocess wrapper

## agents

### default
- **role**: "Telegram client library developer (telegram-cli wrapper)"
- **style**: "technical, direct, focus on simplicity"
- **constraints**:
  - "TDD: tests written BEFORE implementation"
  - "Full type hints required (mypy strict mode)"
  - "Async/await for all I/O operations"
  - "Custom exceptions, not generic errors"
  - "Proper logging: DEBUG for details, INFO for state changes"
  - "No hardcoded paths (use Config class)"
  - "Docstrings for all public APIs"
  - "Mock subprocess calls in tests"

### existenz
- **role**: "Development assistant (primary)"
- **responsibilities**:
  - Code review and PRs
  - Test generation and improvement
  - Documentation updates
  - API design decisions

### codex
- **role**: "Coding expert (complex tasks)"
- **responsibilities**:
  - Large refactorings
  - Subprocess communication patterns
  - Async/subprocess coordination
  - Error recovery in subprocess handling

## code_quality

### testing
- **framework**: "pytest"
- **min_coverage**: 80
- **strategy**: "TDD (write test first, then code)"
- **async_fixtures**: true
- **mocking**: "Mock subprocess.Popen in all tests"
- **approach**: "Unit tests + integration with actual telegram-cli optional"

### formatting
- **tool**: "black"
- **line_length**: 100
- **command**: `poetry run black src/ tests/`

### typing
- **tool**: "mypy"
- **strict**: true
- **command**: `poetry run mypy src/`

### linting
- **tool**: "pylint"
- **command**: `poetry run pylint src/`

## code_patterns

### Subprocess Handling
```python
# Good: Proper process management
async def send_message(self, peer: str, text: str) -> Dict[str, Any]:
    if not self._connected:
        raise ConnectionError("Not connected")
    
    try:
        output = await self._run_command(f'msg {peer} "{text}"')
        return {"peer": peer, "text": text, "sent": True}
    except subprocess.TimeoutExpired:
        logger.error("telegram-cli timeout")
        raise ConnectionError("telegram-cli timeout")
```

### Configuration
```python
# Good: Config from environment
self.tg_cli_path = os.getenv("TG_CLI_PATH", "tg")
self.tg_config_dir = Path(os.getenv("TG_CONFIG_DIR", str(...)))

# Bad: Hardcoded paths
self.tg_cli_path = "/usr/bin/tg"
```

### Error Handling
```python
# Good: Custom exceptions with context
raise ConnectionError(f"Failed to connect: {e}")

# Bad: Generic exceptions
raise Exception("failed")
```

## documentation

### README.md
- telegram-cli backend explanation
- No APP_ID needed (safety angle)
- Installation of telegram-cli
- Quick setup (tg command once)
- API reference
- Security/privacy benefits

### QUICKSTART.md
- Install telegram-cli
- Run 'tg' for session (one-time)
- Install plugin
- First test
- Send message example

### CONTRIBUTING.md
- TDD workflow
- How to run tests
- Code style rules
- Subprocess mocking patterns

### Docstrings
- Google style
- Note when subprocess involved
- Explain telegram-cli requirement

## project

- **name**: "openclaw-telegram-client-plugin"
- **domain**: "User account Telegram client (no APP_ID needed)"
- **language**: "Python 3.9+"
- **version**: "0.2.0" (telegram-cli backend)
- **publish**: "yes (GitHub + PyPI)"
- **license**: "MIT"

## publishing

- **github**: "yourusername/openclaw-telegram-client-plugin"
- **pypi**: "openclaw-telegram-client-plugin"
- **ci_cd**: "GitHub Actions (tests.yml)"
- **python_versions**: ["3.9", "3.10", "3.11"]
- **dependency**: "telegram-cli (user installed, not in pip)"

## communication

- **style**: "technical, direct, pragmatic"
- **avoid**: 
  - App ID security discussions (already solved)
  - Telethon references (migrated away)
  - Complex async patterns (keep it simple for subprocess)
- **prefer**:
  - Subprocess handling patterns
  - Real code examples
  - Error cases with telegram-cli
  - Setup simplicity

## workflow

### TDD Cycle
1. Write failing test: `tests/test_*.py` (mock subprocess)
2. Run: `poetry run pytest tests/test_file.py`
3. Implement in `src/openclaw_telegram/`
4. Test passes
5. Format: `poetry run black src/ tests/`
6. Type check: `poetry run mypy src/`
7. Commit: `git commit -m "feat: ..."`

### Before PR
```bash
poetry run pytest               # All tests pass
poetry run black --check src/   # Formatted
poetry run mypy src/            # Types ok
poetry run pylint src/          # No critical issues
```

## constraints

**Hard Rules**
- ✅ Must have tests (TDD)
- ✅ Must type hint (mypy strict)
- ✅ Must handle errors (custom exceptions)
- ✅ Must mock subprocess in tests
- ✅ Must document (docstrings + examples)
- ✅ No APP_ID/APP_HASH in code

**Not Allowed**
- ❌ Hardcoded telegram-cli path
- ❌ Untested subprocess operations
- ❌ Generic Exception raises
- ❌ Silent subprocess failures
- ❌ Secrets in documentation

## migration_notes

**From v0.1 (Telethon) to v0.2 (telegram-cli):**
- `TelegramClient` API stays the same (backward compat)
- `config.py` removes APP_ID/APP_HASH requirements
- `tg_cli.py` replaces telethon client impl
- Tests now mock `subprocess.Popen`
- Documentation emphasizes local credentials

## See Also

- [README.md](README.md) — Full documentation
- [QUICKSTART.md](QUICKSTART.md) — Setup guide
- [telegram-cli](https://github.com/vysheng/tg) — Backend tool
- [CONTRIBUTING.md](CONTRIBUTING.md) — Development guide

---

**Safe, simple, published. No secrets exposed.** 🔐
