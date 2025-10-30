# Contributing to Win-Dev-Ai-MemZero-AzureTTS

Thank you for your interest in contributing to the Universal Memory System! This is a living, breathing repository for open source collaboration.

## Copilot Prime Directive

Before contributing, please understand the governing principle:

**This system creates a universal, model-agnostic memory, freeing AI from context limits. Architecture is MCP-first: The Master Control Program is the single source of truth for all gateways and services.**

Your contributions should align with this directive and not compromise the core architecture.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its benefits
3. Explain how it aligns with the MCP-first architecture
4. Consider impact on model-agnostic design

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Development Guidelines

### Core Principles

1. **Model Agnostic**: Code should work with ANY AI model
2. **MCP-First**: MCP remains the single source of truth
3. **Minimal Dependencies**: Keep external dependencies minimal
4. **Thread Safety**: All shared resources must be thread-safe
5. **Documentation**: Document all public APIs

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write clear, self-documenting code
- Add docstrings to all public functions/classes
- Keep functions focused and modular

### Testing

- Test your changes before submitting
- Include test cases for new features
- Ensure existing tests pass
- Test with different AI models when applicable

### Documentation

- Update README.md if adding user-facing features
- Update API.md for new public APIs
- Add examples for new functionality
- Update ARCHITECTURE.md for architectural changes

## Critical Components

These components are critical and changes should be carefully considered:

1. **MCP Core** (`mcp/core.py`): Single source of truth
2. **Universal Memory** (`agents/memory.py`): Model-agnostic memory
3. **Memory Agent** (`agents/agent.py`): AI-memory bridge
4. **TTS Bridge** (`tts_bridge/bridge.py`): WSL-Windows integration
5. **Ollama Manager** (`ollama_config/manager.py`): Shared instance

Changes to these should:
- Maintain backward compatibility when possible
- Preserve the model-agnostic design
- Keep MCP as the central authority
- Not introduce model-specific dependencies

## Areas for Contribution

### High Priority

- **Semantic Search**: Add vector embeddings for better retrieval
- **Performance**: Optimize memory search algorithms
- **Storage Backends**: Add support for databases (PostgreSQL, MongoDB)
- **Testing**: Expand test coverage
- **Examples**: More integration examples with different AI models

### Medium Priority

- **Distributed Memory**: Multi-node memory sharing
- **Memory Sync**: Cross-instance synchronization
- **Advanced Pruning**: ML-based importance scoring
- **Monitoring**: Better observability and metrics
- **UI/Dashboard**: Web interface for memory management

### Low Priority

- **Additional TTS Providers**: Support for more TTS services
- **More Voices**: Expand Azure TTS voice options
- **Batch Operations**: Bulk memory operations
- **Export/Import**: Memory backup and restore tools

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Help others learn and grow
- Assume good intentions

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## Architecture Governance

### Approved Changes

✅ Adding new memory backends (as long as they're swappable)
✅ Performance optimizations
✅ New AI model integrations (maintaining model-agnostic design)
✅ Better search algorithms
✅ Additional documentation and examples
✅ Bug fixes
✅ Test improvements

### Requires Discussion

⚠️ Changes to MCP core architecture
⚠️ Breaking API changes
⚠️ New required dependencies
⚠️ Changes to memory entry structure
⚠️ Modifications to singleton patterns

### Not Permitted

❌ Making the system model-specific
❌ Removing MCP as single source of truth
❌ Breaking the model-agnostic design
❌ Compromising critical components
❌ Adding hard dependencies on specific AI providers

## Getting Help

- Read the [Quick Start Guide](docs/QUICKSTART.md)
- Check the [API Reference](docs/API.md)
- Review the [Architecture Documentation](docs/ARCHITECTURE.md)
- Look at existing [examples](examples.py)
- Open an issue for questions

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Special thanks in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see LICENSE file).

## Questions?

Open an issue with the "question" label and we'll be happy to help!

---

**Remember**: This system is about creating a universal, model-agnostic memory that frees AI from context limits. Keep this vision in mind with every contribution.

Thank you for helping build the future of AI memory systems! 🚀
