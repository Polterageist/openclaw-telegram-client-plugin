# Contributing

Contributions are welcome! Follow these guidelines:

## Development Setup

```bash
git clone https://github.com/yourusername/openclaw-telegram-client-plugin
cd openclaw-telegram-client-plugin
poetry install
```

## TDD Workflow

1. **Write test first** (test fails)
   ```bash
   # Add test in tests/test_*.py
   ```

2. **Implement feature** (test passes)
   ```bash
   # Add implementation in src/openclaw_telegram/
   ```

3. **Refactor** (test still passes)
   ```bash
   # Improve code quality
   ```

## Before Submitting PR

```bash
# Run all checks
poetry run pytest
poetry run black openclaw_telegram/ tests/
poetry run pylint openclaw_telegram/
poetry run mypy openclaw_telegram/
```

## Code Style

- Use [Black](https://github.com/psf/black) for formatting
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Type hints required
- Docstrings for public APIs

## Testing

- Write tests in `tests/` directory
- Use pytest fixtures in `conftest.py`
- Mock external dependencies
- Aim for >80% coverage

```bash
poetry run pytest tests/test_client.py -v
poetry run pytest --cov=src/openclaw_telegram
```

## Documentation

- Update `README.md` for user-facing changes
- Update docstrings for code changes
- Add examples for new features

## Commit Messages

```
feat: add message encryption
fix: handle rate limit errors
docs: improve quickstart
test: add message handler tests
refactor: simplify client connection logic
```

## Pull Request

1. Create feature branch: `git checkout -b feature/my-feature`
2. Commit with clear messages
3. Push: `git push origin feature/my-feature`
4. Create PR with description
5. Address review comments
6. Merge when approved ✅

## Questions?

Open an issue or reach out to the maintainer.

Thanks for contributing! 🎉
