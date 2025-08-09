# Contributing to LEWIS

We love your input! We want to make contributing to LEWIS as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with GitHub

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [GitHub Flow](https://guides.github.com/introduction/flow/index.html)

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/yashab-cyber/lewis/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yashab-cyber/lewis/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Environment Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup Steps
```bash
# 1. Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/lewis.git
cd lewis

# 2. Create virtual environment
python3 -m venv lewis-dev
source lewis-dev/bin/activate  # On Windows: lewis-dev\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Install in development mode
pip install -e .

# 5. Install pre-commit hooks
pre-commit install

# 6. Run tests to verify setup
python -m pytest tests/ -v
```

## Code Style

### Python Code Standards
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [flake8](https://flake8.pycqa.org/) for linting
- Include type hints for all functions
- Write comprehensive docstrings

### Running Code Quality Tools
```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .

# Security analysis
bandit -r .

# Dependency vulnerability check
safety check

# All checks together
make quality-check
```

## Testing

### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── security/       # Security-specific tests
├── performance/    # Performance benchmarks
└── e2e/           # End-to-end tests
```

### Running Tests
```bash
# All tests
python -m pytest

# Specific test categories
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/security/ -v

# Coverage report
python -m pytest --cov=lewis --cov-report=html

# Performance tests
python -m pytest tests/performance/ --benchmark-only
```

### Writing Tests
- Write tests for all new functionality
- Maintain >90% test coverage
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies

## Security Guidelines

### Security-First Development
- Never commit secrets, API keys, or passwords
- Use environment variables for sensitive configuration
- Validate all inputs and sanitize outputs
- Follow principle of least privilege
- Report security vulnerabilities privately to yashabalam707@gmail.com

### Security Testing
- Run security tests: `python -m pytest tests/security/`
- Use Bandit for static security analysis: `bandit -r .`
- Scan dependencies: `safety check`

## Documentation

### Code Documentation
- Write clear, comprehensive docstrings
- Include examples in docstrings where helpful
- Document all public APIs
- Keep documentation up-to-date with code changes

### Project Documentation
- Update README.md for significant changes
- Add new features to the changelog
- Update API documentation
- Include setup and usage examples

## Pull Request Process

### Before Submitting
1. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
2. **Write Tests**: Ensure new code has appropriate test coverage
3. **Update Documentation**: Update relevant documentation
4. **Run Quality Checks**: Ensure all checks pass
5. **Commit Changes**: Use clear, descriptive commit messages

### Pull Request Requirements
- **Clear Description**: Explain what changes you made and why
- **Link Issues**: Reference any related issues
- **Test Coverage**: Include tests for new functionality
- **Documentation**: Update docs as needed
- **Quality Checks**: All CI checks must pass

### Commit Message Guidelines
```
type(scope): brief description

Longer description if needed, explaining what and why, not how.

Fixes #123
```

**Types**: feat, fix, docs, style, refactor, test, chore

## Issue Guidelines

### Bug Reports
Use the bug report template and include:
- **Environment**: OS, Python version, LEWIS version
- **Steps to Reproduce**: Clear, numbered steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Additional Context**: Screenshots, logs, etc.

### Feature Requests
Use the feature request template and include:
- **Problem**: What problem does this solve?
- **Solution**: Describe your proposed solution
- **Alternatives**: Alternative solutions considered
- **Additional Context**: Screenshots, mockups, etc.

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers and answer questions
- Follow GitHub's Community Guidelines

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Discord**: Real-time chat and community support
- **Email**: Security issues and private matters

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Hall of Fame (coming soon)
- Annual contributor spotlight

## Getting Help

### Development Questions
- Check existing [GitHub Issues](https://github.com/yashab-cyber/lewis/issues)
- Join our [Discord community](https://discord.gg/zehrasec)
- Review the [documentation](https://docs.lewis-security.com)

### Contact Maintainers
- **Yashab Alam**: [@yashab-cyber](https://github.com/yashab-cyber)
- **Email**: yashabalam707@gmail.com
- **LinkedIn**: [Yashab Alam](https://www.linkedin.com/in/yashab-alam)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to LEWIS! 🚀**

*Together, we're advancing cybersecurity through AI innovation.*
