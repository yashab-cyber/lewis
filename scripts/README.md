# LEWIS Utility Scripts

This directory contains utility scripts for LEWIS setup, maintenance, and development.

## Available Scripts

### `setup_environment.py`
**Purpose**: Complete environment setup and validation
**Usage**: `python scripts/setup_environment.py`
**Features**:
- System requirements checking
- Directory structure creation
- Dependency installation
- Configuration validation
- Database initialization
- Installation testing

### `download_models.py`
**Purpose**: Download and install AI/ML models
**Usage**: `python scripts/download_models.py`
**Features**:
- Vosk speech recognition models
- Hugging Face transformer models
- Automatic extraction and setup
- Progress tracking

### Script Usage Examples

```bash
# Full environment setup
python scripts/setup_environment.py

# Download AI models
python scripts/download_models.py

# Make scripts executable (Linux/Mac)
chmod +x scripts/*.py
```

## Development Scripts

For development and testing:

```bash
# Run all setup scripts
python scripts/setup_environment.py
python scripts/download_models.py

# Validate installation
python validate_lewis.py

# Run tests
python -m pytest tests/
```

## Creating New Scripts

When creating new utility scripts:

1. **Follow naming convention**: `action_subject.py`
2. **Include docstring**: Describe purpose and usage
3. **Add to this README**: Document the new script
4. **Make executable**: `chmod +x script_name.py`
5. **Add error handling**: Robust error handling and user feedback

## Script Template

```python
#!/usr/bin/env python3
"""
Script Description
Brief description of what this script does
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print script banner"""
    print("=" * 60)
    print("LEWIS - Script Name")
    print("=" * 60)

def main():
    """Main script function"""
    print_banner()
    
    # Script logic here
    
    print("Script completed successfully!")

if __name__ == "__main__":
    main()
```

## Dependencies

Scripts may require additional packages:
- `wget` - For downloading files
- `requests` - For HTTP requests
- `yaml` - For configuration parsing
- `zipfile` - For archive extraction

Install script dependencies:
```bash
pip install wget requests pyyaml
```
