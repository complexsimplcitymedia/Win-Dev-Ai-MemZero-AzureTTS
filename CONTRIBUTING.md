# Contributing to Win-Dev-AI-MemZero-AzureTTS

Thank you for your interest in contributing! This project is built on the principles of true Open Source collaboration.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Prioritize security and quality

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the issue template
3. Include steps to reproduce
4. Provide system information
5. Add relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Explain the use case
3. Describe the proposed solution
4. Consider backward compatibility

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Write clean, documented code
4. Add tests for new features
5. Ensure all tests pass
6. Update documentation
7. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Win-Dev-Ai-MemZero-AzureTTS.git
cd Win-Dev-Ai-MemZero-AzureTTS

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/ -v

# Format code
black win_dev_ai/

# Check code style
flake8 win_dev_ai/
```

## Coding Standards

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all public functions
- Keep functions focused and small
- Add comments for complex logic
- Write unit tests for new code

## Testing

- All new features must include tests
- Maintain test coverage above 80%
- Test both success and error cases
- Use meaningful test names

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all modules, classes, and functions
- Include examples for new features
- Keep documentation up to date

## Security

- Never commit API keys or secrets
- Use environment variables for configuration
- Report security issues privately
- Follow secure coding practices

## Pull Request Process

1. Update documentation
2. Add/update tests
3. Ensure CI passes
4. Request review
5. Address feedback
6. Maintain clean commit history

## Questions?

Open an issue or start a discussion!

Thank you for contributing! 🎉
