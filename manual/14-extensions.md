# LEWIS Extensions Guide

This guide covers creating, installing, and managing custom extensions for LEWIS.

## 🔌 Extension System Overview

LEWIS features a modular extension system that allows you to:
- Add custom commands and tools
- Integrate with external services
- Extend AI capabilities
- Create custom interfaces
- Add specialized security modules

## 📁 Extension Structure

### Basic Extension Layout
```
my_extension/
├── __init__.py
├── manifest.json
├── extension.py
├── commands/
│   ├── __init__.py
│   └── custom_commands.py
├── tools/
│   ├── __init__.py
│   └── custom_tools.py
├── templates/
│   └── custom_interface.html
├── static/
│   ├── css/
│   └── js/
├── config/
│   └── default.yaml
├── tests/
│   └── test_extension.py
└── README.md
```

### Extension Manifest
Create a `manifest.json` file to define your extension:

```json
{
  "name": "my-custom-extension",
  "version": "1.0.0",
  "description": "Custom extension for LEWIS",
  "author": "Your Name",
  "license": "MIT",
  "lewis_version": ">=1.0.0",
  "main": "extension.py",
  "dependencies": [
    "requests>=2.28.0",
    "beautifulsoup4>=4.11.0"
  ],
  "permissions": [
    "network",
    "filesystem",
    "system"
  ],
  "entry_points": {
    "commands": "commands.custom_commands",
    "tools": "tools.custom_tools",
    "interfaces": "interfaces.custom_interface"
  },
  "configuration": {
    "api_key": {
      "type": "string",
      "required": true,
      "description": "API key for external service"
    },
    "timeout": {
      "type": "integer",
      "default": 30,
      "description": "Request timeout in seconds"
    }
  }
}
```

## 🛠️ Creating Extensions

### 1. Basic Extension Class

```python
# extension.py
from lewis.core.extension_base import ExtensionBase
from lewis.core.decorators import command, tool
import logging

class MyExtension(ExtensionBase):
    def __init__(self, config):
        super().__init__(config)
        self.name = "my-custom-extension"
        self.version = "1.0.0"
        self.logger = logging.getLogger(f"lewis.{self.name}")
    
    async def initialize(self):
        """Initialize extension resources"""
        self.logger.info(f"Initializing {self.name} v{self.version}")
        # Setup external connections, load models, etc.
        await self.setup_external_service()
    
    async def cleanup(self):
        """Clean up extension resources"""
        self.logger.info(f"Cleaning up {self.name}")
        # Close connections, save state, etc.
    
    @command("custom-scan")
    async def custom_scan(self, target: str, options: dict = None):
        """Custom scanning command"""
        self.logger.info(f"Running custom scan on {target}")
        # Implement custom scanning logic
        return {
            "status": "success",
            "target": target,
            "results": []
        }
    
    @tool("custom-analyzer")
    async def analyze_data(self, data: str):
        """Custom data analysis tool"""
        # Implement analysis logic
        return {
            "analysis": "completed",
            "insights": []
        }
```

### 2. Command Extensions

```python
# commands/custom_commands.py
from lewis.core.command_base import CommandBase
from lewis.core.decorators import command_handler

class CustomCommands(CommandBase):
    @command_handler("network-scan")
    async def network_scan(self, context, args):
        """Advanced network scanning command"""
        target = args.get('target')
        port_range = args.get('ports', '1-1000')
        
        # Implement network scanning logic
        results = await self.perform_network_scan(target, port_range)
        
        return {
            "command": "network-scan",
            "target": target,
            "ports_scanned": port_range,
            "open_ports": results.get('open_ports', []),
            "services": results.get('services', [])
        }
    
    @command_handler("vulnerability-check")
    async def vulnerability_check(self, context, args):
        """Custom vulnerability assessment"""
        target = args.get('target')
        depth = args.get('depth', 'standard')
        
        # Implement vulnerability checking
        vulnerabilities = await self.check_vulnerabilities(target, depth)
        
        return {
            "command": "vulnerability-check",
            "target": target,
            "vulnerabilities": vulnerabilities,
            "risk_level": self.calculate_risk_level(vulnerabilities)
        }
```

### 3. Tool Extensions

```python
# tools/custom_tools.py
from lewis.core.tool_base import ToolBase
from lewis.core.decorators import tool_handler

class CustomTools(ToolBase):
    @tool_handler("log-analyzer")
    async def analyze_logs(self, log_file: str, pattern: str = None):
        """Advanced log analysis tool"""
        # Implement log analysis logic
        analysis = await self.parse_log_file(log_file, pattern)
        
        return {
            "tool": "log-analyzer",
            "file": log_file,
            "pattern": pattern,
            "entries_analyzed": analysis.get('total_entries'),
            "anomalies": analysis.get('anomalies', []),
            "summary": analysis.get('summary')
        }
    
    @tool_handler("threat-intel")
    async def threat_intelligence(self, indicators: list):
        """Threat intelligence lookup"""
        # Query threat intelligence sources
        intel = await self.query_threat_sources(indicators)
        
        return {
            "tool": "threat-intel",
            "indicators": indicators,
            "threats": intel.get('threats', []),
            "reputation": intel.get('reputation', {})
        }
```

## 📦 Installing Extensions

### Method 1: From Source
```bash
# Clone extension repository
git clone https://github.com/user/lewis-extension.git
cd lewis-extension

# Install extension
lewis extension install .
```

### Method 2: From Package
```bash
# Install from PyPI
lewis extension install my-extension

# Install from URL
lewis extension install https://github.com/user/extension.git
```

### Method 3: Manual Installation
```bash
# Copy extension to LEWIS extensions directory
cp -r my_extension ~/.lewis/extensions/

# Enable extension
lewis extension enable my-extension
```

## 🔧 Managing Extensions

### List Extensions
```bash
# List all extensions
lewis extension list

# List enabled extensions only
lewis extension list --enabled

# List extension details
lewis extension info my-extension
```

### Enable/Disable Extensions
```bash
# Enable extension
lewis extension enable my-extension

# Disable extension
lewis extension disable my-extension

# Toggle extension
lewis extension toggle my-extension
```

### Update Extensions
```bash
# Update single extension
lewis extension update my-extension

# Update all extensions
lewis extension update --all

# Check for updates
lewis extension check-updates
```

### Remove Extensions
```bash
# Remove extension
lewis extension remove my-extension

# Force remove (ignore dependencies)
lewis extension remove my-extension --force
```

## 🔒 Extension Security

### Permission System
Extensions must declare required permissions:

```json
{
  "permissions": [
    "network",      // Network access
    "filesystem",   // File system access
    "system",       // System command execution
    "database",     // Database access
    "encryption",   // Cryptographic operations
    "external_api", // External API calls
    "user_data"     // Access to user data
  ]
}
```

### Sandboxing
LEWIS runs extensions in isolated environments:

```python
# Secure extension execution
from lewis.security.sandbox import ExtensionSandbox

sandbox = ExtensionSandbox(
    permissions=['network', 'filesystem'],
    resource_limits={
        'memory': '512MB',
        'cpu_time': 30,
        'network_bandwidth': '10MB/s'
    }
)

result = await sandbox.execute_extension(extension, command, args)
```

### Code Signing
Sign your extensions for distribution:

```bash
# Generate signing key
lewis keygen extension-signing

# Sign extension
lewis sign my-extension.zip

# Verify signature
lewis verify my-extension.zip
```

## 🧪 Testing Extensions

### Unit Tests
```python
# tests/test_extension.py
import pytest
from lewis.testing import LewisTestCase
from my_extension.extension import MyExtension

class TestMyExtension(LewisTestCase):
    async def test_custom_scan(self):
        """Test custom scan functionality"""
        extension = MyExtension(self.get_test_config())
        result = await extension.custom_scan("example.com")
        
        assert result['status'] == 'success'
        assert result['target'] == 'example.com'
    
    async def test_data_analysis(self):
        """Test data analysis tool"""
        extension = MyExtension(self.get_test_config())
        result = await extension.analyze_data("test data")
        
        assert 'analysis' in result
        assert result['analysis'] == 'completed'
```

### Integration Tests
```bash
# Run extension tests
lewis test my-extension

# Run all extension tests
lewis test --extensions

# Run with coverage
lewis test my-extension --coverage
```

## 📚 Extension Development Best Practices

### 1. Follow Naming Conventions
- Use kebab-case for extension names
- Prefix commands with extension name
- Use descriptive function names

### 2. Handle Errors Gracefully
```python
async def my_command(self, args):
    try:
        result = await self.risky_operation(args)
        return result
    except Exception as e:
        self.logger.error(f"Command failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
```

### 3. Use Async/Await
```python
# Good - Non-blocking
async def network_scan(self, target):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{target}") as response:
            return await response.json()

# Avoid - Blocking
def network_scan(self, target):
    response = requests.get(f"http://{target}")
    return response.json()
```

### 4. Implement Configuration Validation
```python
def validate_config(self, config):
    required_fields = ['api_key', 'endpoint']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    if len(config['api_key']) < 10:
        raise ValueError("API key too short")
```

### 5. Provide Rich Output
```python
async def scan_command(self, target):
    return {
        "status": "completed",
        "target": target,
        "timestamp": datetime.utcnow().isoformat(),
        "results": {
            "summary": "Scan completed successfully",
            "details": scan_results,
            "recommendations": recommendations
        },
        "metadata": {
            "scan_duration": scan_time,
            "tools_used": tools_list,
            "confidence": confidence_score
        }
    }
```

## 🌐 Publishing Extensions

### 1. Prepare for Release
```bash
# Validate extension
lewis extension validate my-extension

# Run tests
lewis test my-extension --all

# Build package
lewis extension build my-extension
```

### 2. Publish to Registry
```bash
# Login to LEWIS registry
lewis login

# Publish extension
lewis extension publish my-extension

# Publish with metadata
lewis extension publish my-extension --tag stable --category security
```

### 3. Documentation
Create comprehensive documentation:
- README.md with usage examples
- API documentation
- Configuration guide
- Troubleshooting section
- Changelog

## 🔄 Extension Lifecycle

### Development Phase
1. Design extension architecture
2. Implement core functionality
3. Add tests and documentation
4. Validate with `lewis extension validate`

### Testing Phase
1. Unit testing
2. Integration testing
3. Security review
4. Performance testing

### Release Phase
1. Version tagging
2. Package building
3. Digital signing
4. Registry publication

### Maintenance Phase
1. Bug fixes
2. Feature updates
3. Security patches
4. Compatibility updates

## 📖 Examples and Templates

### Minimal Extension Template
```python
from lewis.core.extension_base import ExtensionBase
from lewis.core.decorators import command

class MinimalExtension(ExtensionBase):
    def __init__(self, config):
        super().__init__(config)
        self.name = "minimal-extension"
    
    @command("hello")
    async def hello_command(self, name: str = "World"):
        return {"message": f"Hello, {name}!"}
```

### Network Security Extension
See `examples/network_security_extension/` for a complete example of a network security extension.

### Custom Interface Extension
See `examples/custom_interface_extension/` for creating custom web interfaces.

## 🆘 Troubleshooting Extensions

### Common Issues
1. **Extension not loading**: Check manifest.json syntax
2. **Permission denied**: Review required permissions
3. **Import errors**: Verify dependencies
4. **Performance issues**: Profile with `lewis profile`

### Debug Mode
```bash
# Enable extension debugging
lewis --debug extension enable my-extension

# View extension logs
lewis logs extension my-extension

# Trace extension execution
lewis trace extension my-extension command args
```

## 📞 Support

- **Documentation**: Check extension-specific docs
- **Community**: Join LEWIS Discord/Forums
- **Issues**: Report on GitHub
- **Email**: extensions@zehrasec.com

---

*For more information, see the [Development Guide](11-development.md) and [API Reference](05-api-reference.md).*
