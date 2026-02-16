# Contributing to Dictate

Thank you for your interest in contributing to Dictate! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- macOS 12+ (Monterey or later)
- Python 3.10–3.13
- Git

### Setting Up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/ADJ-HUB1/dictate.git
   cd dictate
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install in development mode with dev dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

5. **Run tests to verify setup:**
   ```bash
   pytest tests/ -v
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_pipeline.py

# Run with coverage report
pytest --cov=dictate tests/
```

### Writing Tests

- All new features should include tests
- Place tests in the `tests/` directory
- Use descriptive test names: `test_<functionality>_<expected_behavior>`
- Mock external dependencies (microphone, clipboard, etc.)

Example test structure:
```python
def test_filler_removal_removes_um():
    """Test that 'um' is removed from transcription."""
    processor = RegexProcessor()
    result = processor.process("um this is a test")
    assert result == "This is a test."
```

## 📝 Code Style

### Python Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all public functions and classes

### Code Quality Tools

We recommend using:
- **mypy** for type checking
- **black** for code formatting
- **ruff** for linting

```bash
# Run type checking
mypy src/

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```

## 🏗️ Architecture

### Project Structure

```
dictate/
├── src/dictate/           # Main package
│   ├── app.py            # Menu bar application
│   ├── pipeline.py       # Core orchestrator
│   ├── config.py         # Configuration management
│   ├── audio/            # Audio recording and feedback
│   ├── asr/              # ASR engines (Whisper, OpenAI API)
│   ├── processing/       # Text processors (regex, ollama)
│   ├── hotkey/           # Hotkey listeners
│   ├── injection/        # Text injection
│   └── notification/     # macOS notifications
├── tests/                # Unit tests
├── scripts/              # Utility scripts
└── .env.example          # Example configuration
```

### Design Patterns

1. **Protocol-based interfaces** — Each component defines a Protocol for its interface
2. **Factory pattern** — Components are created via factory functions based on config
3. **Dependency injection** — Pipeline receives all dependencies in `__init__`

### Adding a New Component

Example: Adding a new ASR engine

1. **Create the implementation** in `src/dictate/asr/your_engine.py`:
   ```python
   from dictate.asr.base import ASREngine

   class YourEngine(ASREngine):
       def transcribe(self, audio: np.ndarray, sample_rate: int) -> str:
           # Your implementation
           pass
   ```

2. **Update the factory** in `src/dictate/asr/factory.py`:
   ```python
   def create_asr_engine(config: Config) -> ASREngine:
       if config.asr_engine == "your_engine":
           from dictate.asr.your_engine import YourEngine
           return YourEngine()
       # ... existing code
   ```

3. **Update config validation** in `src/dictate/config.py`:
   ```python
   valid_asr = ("local", "openai_api", "your_engine")
   ```

4. **Add tests** in `tests/test_your_engine.py`

5. **Update documentation** in README.md and .env.example

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing [GitHub Issues](https://github.com/ADJ-HUB1/dictate/issues)
2. Verify you're using a supported Python version (3.10–3.13)
3. Try with the default configuration (`.env.example`)
4. Check the [Troubleshooting](README.md#-troubleshooting) section

### Bug Report Template

```markdown
**Description:**
Clear description of the bug

**To Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- macOS version:
- Python version:
- Dictate version/commit:
- Configuration (.env settings):

**Logs:**
```
Paste relevant logs here
```
```

## 💡 Feature Requests

We welcome feature requests! Please:

1. Check if the feature is already requested or in the [Roadmap](README.md#-roadmap)
2. Open a new issue with the `enhancement` label
3. Clearly describe:
   - The problem you're trying to solve
   - Your proposed solution
   - Any alternatives you've considered
   - Potential implementation approach

## 🔀 Pull Request Process

### Before Submitting

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, well-documented code
   - Add or update tests
   - Update documentation (README, docstrings, etc.)

3. **Test thoroughly:**
   ```bash
   pytest tests/ -v
   ```

4. **Commit with clear messages:**
   ```bash
   git commit -m "feat: add support for custom hotkeys"
   ```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add new feature`
- `fix: fix bug in component`
- `docs: update documentation`
- `test: add or update tests`
- `refactor: refactor code without changing behavior`
- `perf: performance improvement`
- `chore: maintenance task`

### Submitting the PR

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub with:
   - Clear title following conventional commits format
   - Description of changes
   - Link to related issue (if applicable)
   - Screenshots/demos for UI changes

3. **Wait for review** — maintainers will review and provide feedback

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally (`pytest`)
- [ ] New code has tests
- [ ] Documentation updated (README, docstrings, etc.)
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow conventional commits

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what's best for the project and community
- Accept constructive criticism gracefully
- Show empathy toward other contributors

### Unacceptable Behavior

- Harassment, discrimination, or derogatory comments
- Trolling, insulting, or personal attacks
- Publishing others' private information
- Any conduct inappropriate in a professional setting

## 🎯 Areas for Contribution

Looking for where to start? Check out:

1. **Good First Issues** — Simple bugs or features labeled `good first issue`
2. **Documentation** — Improve README, add examples, clarify confusing parts
3. **Testing** — Increase test coverage, add integration tests
4. **Performance** — Optimize slow parts of the codebase
5. **Features from Roadmap** — Implement planned features

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Chat**: (Add Discord/Slack link if applicable)
- **Email**: (Add contact email if applicable)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Dictate! 🎉
