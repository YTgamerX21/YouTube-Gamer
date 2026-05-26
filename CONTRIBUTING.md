# Contributing to YouTube Gamer AI

Thank you for your interest in contributing! Here's how you can help.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/YouTube-Gamer.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run tests: `pytest`
6. Commit: `git commit -m "Add feature"`
7. Push: `git push origin feature/your-feature`
8. Open a Pull Request

## Code Standards

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Write tests for new features
- Keep functions focused and single-purpose

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_ai.py
```

## Code Style

```bash
# Format code
black src/

# Check linting
flake8 src/

# Type checking
mypy src/
```

## Pull Request Process

1. Update README.md with any new features
2. Ensure all tests pass
3. Update documentation
4. Request review from maintainers

## Reporting Issues

Use GitHub Issues to report bugs. Include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and environment

## Feature Requests

Discuss major features in Issues first before implementing.

## Questions?

Open an issue or discussion for questions about the project.

Thank you for contributing! 🚀
