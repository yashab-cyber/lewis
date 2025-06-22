# Contributing to LEWIS

Thank you for your interest in contributing to LEWIS (Linux Environment Working Intelligence System)! This guide will help you get started with contributing to the project.

## 🌟 Ways to Contribute

There are many ways to contribute to LEWIS:

### 🐛 Bug Reports
- Report bugs and issues
- Help reproduce and debug problems
- Suggest improvements to error messages

### 💡 Feature Requests
- Propose new features and enhancements
- Discuss use cases and requirements
- Help prioritize development roadmap

### 📝 Documentation
- Improve existing documentation
- Write tutorials and guides
- Translate documentation
- Add code examples

### 💻 Code Contributions
- Fix bugs and implement features
- Improve performance and security
- Add tests and improve coverage
- Refactor and optimize code

### 🧪 Testing
- Test new features and releases
- Create and maintain test cases
- Test on different platforms
- Report compatibility issues

### 🎨 Design and UX
- Improve user interfaces
- Design new interface components
- Enhance user experience
- Create visual assets

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of cybersecurity concepts
- Familiarity with async/await programming

### Development Environment Setup

1. **Fork and Clone the Repository**
   ```bash
   # Fork the repository on GitHub
   # Then clone your fork
   git clone https://github.com/yourusername/LEWIS.git
   cd LEWIS
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv lewis-dev
   
   # Activate virtual environment
   # On Linux/macOS:
   source lewis-dev/bin/activate
   # On Windows:
   lewis-dev\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   # Install LEWIS in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   
   # Install pre-commit hooks
   pre-commit install
   ```

4. **Configure Development Environment**
   ```bash
   # Copy example configuration
   cp config/config.example.yaml config/config.yaml
   
   # Edit configuration for development
   nano config/config.yaml
   ```

5. **Verify Installation**
   ```bash
   # Run tests to verify setup
   python -m pytest tests/
   
   # Run LEWIS in development mode
   python lewis.py --help
   ```

## 📋 Development Guidelines

### Code Style

We follow PEP 8 with some specific conventions:

```python
# Use type hints
async def scan_target(target: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """Scan a target with specified options."""
    pass

# Use descriptive variable names
scan_results = await scanner.scan(target)
vulnerability_count = len(scan_results.get('vulnerabilities', []))

# Use docstrings for all public functions
def analyze_vulnerabilities(vulns: List[Dict]) -> Dict[str, Any]:
    """
    Analyze a list of vulnerabilities and return risk assessment.
    
    Args:
        vulns: List of vulnerability dictionaries
        
    Returns:
        Dictionary containing risk analysis
    """
    pass
```

### Async/Await Patterns
```python
# Prefer async/await for I/O operations
async def network_scan(target: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{target}") as response:
            return await response.json()

# Use asyncio.gather for concurrent operations
results = await asyncio.gather(
    scan_ports(target),
    check_services(target),
    analyze_vulnerabilities(target)
)
```

### Error Handling
```python
# Use specific exception types
try:
    result = await risky_operation()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    return {"status": "error", "message": "Connection failed"}
except TimeoutError as e:
    logger.error(f"Operation timed out: {e}")
    return {"status": "timeout", "message": "Operation timed out"}
except Exception as e:
    logger.exception("Unexpected error occurred")
    return {"status": "error", "message": "Internal error"}
```

### Logging
```python
import logging

# Use module-specific loggers
logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning about potential issues")
logger.error("Error occurred")
logger.critical("Critical error requiring immediate attention")
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_core.py

# Run with coverage
python -m pytest tests/ --cov=lewis --cov-report=html

# Run integration tests
python -m pytest tests/integration/

# Run performance tests
python -m pytest tests/performance/ --benchmark
```

### Writing Tests
```python
# tests/test_new_feature.py
import pytest
from unittest.mock import AsyncMock, patch
from lewis.core.new_feature import NewFeature

class TestNewFeature:
    @pytest.fixture
    async def feature(self):
        """Create a NewFeature instance for testing."""
        config = {"setting1": "value1", "setting2": "value2"}
        feature = NewFeature(config)
        await feature.initialize()
        yield feature
        await feature.cleanup()
    
    async def test_basic_functionality(self, feature):
        """Test basic feature functionality."""
        result = await feature.do_something("test_input")
        assert result["status"] == "success"
        assert "output" in result
    
    async def test_error_handling(self, feature):
        """Test error handling."""
        with patch.object(feature, 'internal_method', side_effect=Exception("Test error")):
            result = await feature.do_something("invalid_input")
            assert result["status"] == "error"
    
    @pytest.mark.asyncio
    async def test_async_operation(self, feature):
        """Test asynchronous operations."""
        # Test concurrent operations
        tasks = [
            feature.do_something(f"input_{i}")
            for i in range(5)
        ]
        results = await asyncio.gather(*tasks)
        assert len(results) == 5
        assert all(r["status"] == "success" for r in results)
```

### Test Categories

1. **Unit Tests** (`tests/unit/`)
   - Test individual functions and classes
   - Mock external dependencies
   - Fast execution

2. **Integration Tests** (`tests/integration/`)
   - Test component interactions
   - Use real external services (when safe)
   - Test complete workflows

3. **Performance Tests** (`tests/performance/`)
   - Benchmark critical operations
   - Memory usage tests
   - Load testing

4. **Security Tests** (`tests/security/`)
   - Test security features
   - Vulnerability scanning
   - Input validation tests

## 📝 Pull Request Process

### Before Submitting

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/awesome-new-feature
   # or
   git checkout -b bugfix/fix-critical-bug
   ```

2. **Make Your Changes**
   - Write code following our guidelines
   - Add or update tests
   - Update documentation

3. **Test Your Changes**
   ```bash
   # Run tests
   python -m pytest tests/
   
   # Check code style
   flake8 lewis/
   black --check lewis/
   isort --check-only lewis/
   
   # Check type hints
   mypy lewis/
   
   # Run security checks
   bandit -r lewis/
   ```

4. **Update Documentation**
   - Update relevant manual pages
   - Add docstrings to new functions
   - Update API documentation if needed

### Submitting Pull Request

1. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add awesome new feature
   
   - Implement feature X
   - Add comprehensive tests
   - Update documentation"
   ```

2. **Push to Your Fork**
   ```bash
   git push origin feature/awesome-new-feature
   ```

3. **Create Pull Request**
   - Use the GitHub web interface
   - Fill out the PR template completely
   - Link any related issues

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

## 🔍 Code Review Process

### What We Look For

1. **Functionality**
   - Code works as intended
   - Handles edge cases
   - Error handling is appropriate

2. **Code Quality**
   - Follows style guidelines
   - Well-structured and readable
   - Appropriate abstractions

3. **Security**
   - No security vulnerabilities
   - Input validation
   - Secure defaults

4. **Performance**
   - Efficient algorithms
   - Appropriate resource usage
   - Scales well

5. **Testing**
   - Adequate test coverage
   - Tests are meaningful
   - Tests pass consistently

### Review Timeline
- Initial review: 1-3 business days
- Follow-up reviews: 1-2 business days
- Security reviews: 3-5 business days

## 🏗️ Architecture Guidelines

### Module Structure
```
lewis/
├── core/           # Core system functionality
├── ai/            # AI and ML components
├── interfaces/    # User interfaces (CLI, GUI, Web)
├── tools/         # Security tools integration
├── execution/     # Command execution engine
├── security/      # Security and authentication
├── storage/       # Data storage and management
├── learning/      # Machine learning and knowledge base
├── reports/       # Report generation
├── analytics/     # Analytics and metrics
├── detection/     # Threat detection
├── voice/         # Voice interface
└── utils/         # Utility functions
```

### Design Principles

1. **Modularity**: Keep components loosely coupled
2. **Extensibility**: Design for easy extension
3. **Security**: Security by design and default
4. **Performance**: Optimize for real-world usage
5. **Usability**: Prioritize user experience

### Coding Standards

```python
# File header
"""
LEWIS - Linux Environment Working Intelligence System
Module: Description of module functionality
Author: ZehraSec Team
License: MIT
"""

# Imports organization
# Standard library
import asyncio
import logging
from typing import Dict, List, Any, Optional

# Third-party
import aiohttp
import yaml

# Local imports
from lewis.core.base import BaseModule
from lewis.utils.helpers import validate_input
```

## 🐛 Bug Report Guidelines

### Before Reporting
1. Check existing issues
2. Try latest version
3. Verify it's not a configuration issue

### Bug Report Template
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. With configuration '...'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.9.5]
- LEWIS version: [e.g. 1.0.0]
- Installation method: [e.g. pip, source]

**Additional context**
Add any other context about the problem here.

**Logs**
```
Paste relevant log output here
```

**Configuration**
```yaml
# Paste relevant configuration (remove sensitive data)
```
```

## 💡 Feature Request Guidelines

### Before Requesting
1. Check existing feature requests
2. Consider if it fits LEWIS's scope
3. Think about implementation challenges

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Use cases**
Describe specific use cases where this feature would be valuable.

**Implementation ideas**
If you have ideas about how this could be implemented, share them here.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 🔒 Security Guidelines

### Reporting Security Issues
- **DO NOT** create public issues for security vulnerabilities
- Email security@zehrasec.com with details
- Include steps to reproduce
- Allow time for responsible disclosure

### Security Best Practices
```python
# Input validation
def validate_target(target: str) -> bool:
    """Validate scan target to prevent injection attacks."""
    if not target or len(target) > 255:
        return False
    
    # Check for malicious patterns
    dangerous_patterns = [';', '|', '&&', '`', '$']
    return not any(pattern in target for pattern in dangerous_patterns)

# Secure defaults
CONFIG_DEFAULTS = {
    'max_threads': 10,          # Limit resource usage
    'timeout': 30,              # Prevent hanging operations
    'output_sanitization': True, # Sanitize output by default
    'logging_level': 'INFO'     # Don't log sensitive data
}

# Safe command execution
async def execute_command(cmd: List[str], timeout: int = 30) -> Dict[str, Any]:
    """Execute command safely with timeout and validation."""
    if not validate_command(cmd):
        raise ValueError("Invalid command")
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            timeout=timeout
        )
        stdout, stderr = await process.communicate()
        return {
            'returncode': process.returncode,
            'stdout': stdout.decode(),
            'stderr': stderr.decode()
        }
    except asyncio.TimeoutError:
        process.kill()
        raise TimeoutError(f"Command timed out after {timeout}s")
```

## 📊 Performance Guidelines

### Profiling
```bash
# Profile LEWIS execution
python -m cProfile -o profile.stats lewis.py scan example.com

# Analyze results
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(20)
"

# Memory profiling
python -m memory_profiler lewis.py scan example.com
```

### Optimization Tips
1. Use async/await for I/O operations
2. Batch operations when possible
3. Implement caching for expensive operations
4. Use connection pooling
5. Profile before optimizing

## 🌐 Internationalization

### Adding Translations
```python
# lewis/i18n/messages.py
MESSAGES = {
    'en': {
        'scan_started': 'Scan started for target: {target}',
        'scan_completed': 'Scan completed successfully',
        'error_occurred': 'An error occurred: {error}'
    },
    'es': {
        'scan_started': 'Escaneo iniciado para objetivo: {target}',
        'scan_completed': 'Escaneo completado exitosamente',
        'error_occurred': 'Ocurrió un error: {error}'
    }
}

# Usage
from lewis.i18n import get_message
message = get_message('scan_started', target='example.com')
```

## 📞 Getting Help

### Documentation
- Read the [User Guide](03-user-guide.md)
- Check [FAQ](18-faq.md)
- Review [API Reference](05-api-reference.md)

### Community
- GitHub Discussions: Ask questions and share ideas
- Discord Server: Real-time chat with community
- Stack Overflow: Tag questions with 'lewis-security'

### Direct Support
- Bug reports: GitHub Issues
- Security issues: security@zehrasec.com
- General inquiries: info@zehrasec.com

## 🎯 Project Roadmap

### Current Priorities
1. **Core Stability** - Bug fixes and performance improvements
2. **Documentation** - Comprehensive guides and tutorials
3. **Testing** - Improved test coverage and CI/CD
4. **Security** - Enhanced security features and auditing

### Upcoming Features
1. **Machine Learning** - Advanced threat detection
2. **Cloud Integration** - AWS, Azure, GCP support
3. **Mobile App** - iOS and Android companion apps
4. **Enterprise Features** - RBAC, SSO, compliance reporting

### Long-term Vision
- Industry-standard cybersecurity platform
- AI-powered threat intelligence
- Global security community
- Educational resources and certification

## 🏆 Recognition

### Contributors
All contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Hall of Fame on website

### Contribution Levels
- **Contributor**: Made accepted contributions
- **Regular Contributor**: 5+ merged PRs
- **Core Contributor**: 20+ merged PRs + significant features
- **Maintainer**: Trusted with repository access

## 📜 License

By contributing to LEWIS, you agree that your contributions will be licensed under the MIT License.

---

*Thank you for contributing to LEWIS! Together, we're building the future of cybersecurity automation.*
