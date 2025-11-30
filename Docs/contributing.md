# 🤝 Contributing to Home Lab Log Analyzer

Thank you for considering contributing to this project! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

---

## Code of Conduct

This project follows a simple code of conduct:

- **Be respectful** to all contributors
- **Be patient** with new contributors
- **Be constructive** in feedback
- **Be inclusive** and welcoming

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:

1. **Check existing issues** to avoid duplicates
2. **Verify it's actually a bug** (not a configuration issue)
3. **Test with the latest version**

When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **System information** (OS, Docker version, model used)
- **Logs** (from `docker logs log-analyzer`)

**Template**:
```markdown
## Bug Description
Brief description of what's wrong

## Steps to Reproduce
1. Run command X
2. Observe behavior Y
3. Error occurs

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 22.04
- Docker: 24.0.5
- Model: qwen2.5-1.5b-instruct
- Python: 3.11

## Logs
```
[paste relevant logs here]
```
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:

- **Use case** - Why is this enhancement needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - What other options did you think about?

### Pull Requests

We welcome pull requests for:

- Bug fixes
- New features
- Documentation improvements
- Performance optimizations
- Test coverage improvements

---

## Development Setup

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- LM Studio (for testing)

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/homelab-log-analyzer.git
cd homelab-log-analyzer

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/homelab-log-analyzer.git
```

### Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Run Locally

```bash
# Start the API
python log_analyzer.py

# In another terminal, test
curl http://localhost:8000/health
```

---

## Making Changes

### Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### Write Code

Follow these principles:

1. **Keep it simple** - Avoid unnecessary complexity
2. **Write tests** - For new features or bug fixes
3. **Document** - Add docstrings and comments
4. **Type hints** - Use Python type hints where possible

### Test Your Changes

```bash
# Run tests (when available)
pytest

# Test manually
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"hours": 1, "model": "qwen2.5-1.5b-instruct"}'

# Test with Docker
docker-compose build
docker-compose up
```

---

## Submitting Changes

### Commit Guidelines

Use clear, descriptive commit messages:

**Format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat: add support for custom log filters"
git commit -m "fix: resolve timeout issue with large log volumes"
git commit -m "docs: improve setup guide with troubleshooting steps"
```

### Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Then create a Pull Request on GitHub
```

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Related Issue
Fixes #123

## Changes Made
- Added feature X
- Fixed bug Y
- Updated documentation Z

## Testing
- [ ] Tested locally
- [ ] Tested in Docker
- [ ] Added/updated tests
- [ ] Updated documentation

## Screenshots (if applicable)
[Add screenshots here]
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

---

## Style Guidelines

### Python Code Style

Follow PEP 8 with these specifics:

```python
# Use 4 spaces for indentation (no tabs)

# Maximum line length: 100 characters

# Use type hints
def analyze_logs(container_name: str, hours: int) -> Dict[str, Any]:
    pass

# Use docstrings
def filter_noise(self, log_line: str) -> bool:
    """
    Remove common noise patterns from logs
    
    Args:
        log_line: Single line from container logs
        
    Returns:
        True if line should be kept, False if it's noise
    """
    pass

# Use f-strings for formatting
message = f"Analyzed {count} containers"

# Use list comprehensions when appropriate
filtered = [line for line in logs if self.filter_noise(line)]
```

### Format Code

```bash
# Auto-format with Black
black log_analyzer.py

# Check style with flake8
flake8 log_analyzer.py

# Type check with mypy
mypy log_analyzer.py
```

### Documentation Style

- Use **Markdown** for all documentation
- Keep lines under 100 characters
- Use code blocks with language tags
- Include examples for complex features

### Commit Message Style

```bash
# Good
git commit -m "feat: add filtering for health check logs"

# Bad
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "asdfasdf"
```

---

## Areas That Need Help

Current priorities:

- [ ] **Test coverage** - Add unit tests and integration tests
- [ ] **Documentation** - More examples and use cases
- [ ] **Performance** - Optimize log filtering and analysis
- [ ] **Features**:
  - [ ] Web UI for viewing reports
  - [ ] Database storage for historical analysis
  - [ ] Alerting integration (Slack, Discord, etc.)
  - [ ] Custom model support beyond LM Studio
  - [ ] Multi-node Docker Swarm support

---

## Getting Help

If you need help:

1. Check the [documentation](../README.md)
2. Search [existing issues](https://github.com/OWNER/homelab-log-analyzer/issues)
3. Ask in [Discussions](https://github.com/OWNER/homelab-log-analyzer/discussions)
4. Join the conversation on r/homelab

---

## Recognition

Contributors will be:

- Listed in the README
- Thanked in release notes
- Given credit in commit history

Thank you for making this project better! 🎉
