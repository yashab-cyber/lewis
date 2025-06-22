# LEWIS Extensions Examples

This directory contains example extensions that demonstrate how to extend LEWIS functionality.

## Available Extensions

### 1. Network Security Extension
**Path**: `network_security_extension/`
**Purpose**: Advanced network scanning and security analysis
**Features**:
- Comprehensive network scanning
- Port scanning and service detection
- Vulnerability assessment
- Network topology mapping
- Threat detection

### 2. Custom Interface Extension
**Path**: `custom_interface_extension/`
**Purpose**: Custom web interface with specialized dashboards
**Features**:
- Custom security dashboard
- Real-time monitoring
- Interactive charts and graphs
- WebSocket-based updates
- Responsive design

## Extension Structure

Each extension follows this standard structure:
```
extension_name/
├── __init__.py              # Extension package
├── extension.py             # Main extension class
├── manifest.json            # Extension metadata
├── README.md               # Extension documentation
├── config/
│   └── default.yaml        # Default configuration
├── commands/               # Extension commands (for network ext)
│   ├── __init__.py
│   └── *.py
├── tools/                  # Extension tools (for network ext)
│   ├── __init__.py
│   └── *.py
├── api/                    # API routes (for interface ext)
│   ├── __init__.py
│   └── routes.py
├── static/                 # Static assets (for interface ext)
│   ├── css/
│   └── js/
├── templates/              # HTML templates (for interface ext)
└── tests/                  # Extension tests
    ├── __init__.py
    └── test_*.py
```

## Using Extensions

### 1. Installation
Extensions are automatically discovered when placed in the `examples/` directory or any configured extension path.

### 2. Loading Extensions
```python
from examples.network_security_extension.extension import NetworkSecurityExtension
from examples.custom_interface_extension.extension import CustomInterfaceExtension

# Initialize extensions
network_ext = NetworkSecurityExtension()
interface_ext = CustomInterfaceExtension()

# Initialize
network_ext.initialize()
interface_ext.initialize()
```

### 3. Configuration
Each extension has its own configuration file in `config/default.yaml`. You can override settings by:
- Modifying the default configuration file
- Providing custom configuration during initialization
- Using environment variables (if supported)

## Creating New Extensions

### 1. Basic Extension
```python
from core.extension_base import ExtensionBase
from core.decorators import command, tool

class MyExtension(ExtensionBase):
    def __init__(self):
        super().__init__("my-extension", "1.0.0")
    
    def initialize(self) -> bool:
        # Initialize your extension
        self.enabled = True
        return True
    
    def cleanup(self) -> bool:
        # Cleanup resources
        self.enabled = False
        return True
    
    @command("my-command")
    def my_command(self, arg1: str) -> str:
        return f"Hello {arg1}!"
```

### 2. Network Extension
```python
from core.extension_base import NetworkExtension

class MyNetworkExtension(NetworkExtension):
    def scan_network(self, target: str, scan_type: str = "basic"):
        # Implement network scanning logic
        return {"target": target, "results": []}
```

### 3. Interface Extension
```python
from core.extension_base import InterfaceExtension

class MyInterfaceExtension(InterfaceExtension):
    def initialize(self) -> bool:
        self._setup_flask_app()
        self.register_route("/my-page", self.my_page_handler)
        return True
    
    def my_page_handler(self):
        return self.render_template("my_page.html")
```

## Extension Manifest

Each extension should include a `manifest.json` file:
```json
{
    "name": "my-extension",
    "version": "1.0.0", 
    "description": "My custom extension",
    "author": "Your Name",
    "license": "MIT",
    "dependencies": ["flask", "requests"],
    "lewis_version": ">=1.0.0",
    "entry_point": "extension.MyExtension"
}
```

## Testing Extensions

### Running Tests
```bash
# Test specific extension
python -m pytest examples/network_security_extension/tests/

# Test all extensions
python -m pytest examples/*/tests/

# Run with coverage
python -m pytest --cov=examples examples/*/tests/
```

### Test Structure
```python
import unittest
from examples.my_extension.extension import MyExtension

class TestMyExtension(unittest.TestCase):
    def setUp(self):
        self.extension = MyExtension()
    
    def test_initialization(self):
        result = self.extension.initialize()
        self.assertTrue(result)
```

## Extension Development Guidelines

### 1. Code Standards
- Follow PEP 8 style guidelines
- Use type hints
- Include comprehensive docstrings
- Handle errors gracefully

### 2. Security Considerations
- Validate all inputs
- Use secure defaults
- Implement proper authentication
- Log security events

### 3. Performance
- Use async operations where appropriate
- Implement caching for expensive operations
- Optimize database queries
- Monitor resource usage

### 4. Documentation
- Include comprehensive README
- Document all commands and tools
- Provide usage examples
- Keep documentation up to date

## Deployment

### 1. Development
Extensions are loaded automatically during development when placed in the examples directory.

### 2. Production
For production deployment:
1. Package the extension as a Python wheel
2. Install via pip
3. Configure extension paths in LEWIS configuration
4. Restart LEWIS service

### 3. Distribution
Extensions can be distributed via:
- PyPI packages
- Git repositories
- Docker images
- LEWIS extension marketplace (future)

## Support

For extension development support:
- Check the LEWIS documentation
- Review example extensions
- Join the LEWIS community
- Report issues on GitHub

## Contributing

To contribute new example extensions:
1. Fork the LEWIS repository
2. Create your extension in `examples/`
3. Include comprehensive tests
4. Update this README
5. Submit a pull request

Follow the contributing guidelines in the main LEWIS documentation.
