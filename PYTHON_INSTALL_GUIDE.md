# LEWIS Python 3.11.9 Installation Guide

This guide explains how LEWIS uses pyenv to manage Python 3.11.9 for optimal compatibility while keeping your system Python intact.

## Why Python 3.11.9?

LEWIS dependencies are tested and optimized for Python 3.11.9. Some packages in `requirements.txt` may have compatibility issues with Python 3.13.x due to:

- Binary wheel availability
- C extension compilation issues  
- API changes in newer Python versions
- Dependencies not yet updated for Python 3.13

## Installation Approach

LEWIS uses **pyenv** to manage Python versions, which provides these benefits:

### ✅ Advantages
- **System Python Protection**: Your system Python remains untouched
- **Version Isolation**: LEWIS runs on Python 3.11.9 regardless of system Python
- **Clean Environment**: No conflicts with system packages
- **Easy Management**: Simple version switching and management
- **Production Ready**: Widely used in production environments

### 🔧 How It Works

1. **pyenv Installation**: Installs pyenv at `/opt/pyenv`
2. **Python 3.11.9 Build**: Compiles Python 3.11.9 with optimizations
3. **Virtual Environment**: Creates isolated environment for LEWIS
4. **Dependency Installation**: Installs LEWIS packages in isolated environment
5. **Service Configuration**: Configures systemd service to use correct Python

## Automatic Installation

The main `install.sh` script now automatically:

```bash
sudo ./install.sh
```

This will:
1. Install pyenv dependencies
2. Install pyenv itself
3. Build Python 3.11.9
4. Create LEWIS virtual environment
5. Install optimized dependencies
6. Configure all services

## Manual Python Installation

If you need to install Python 3.11.9 separately:

```bash
sudo ./install_python311.sh
```

## Verification

After installation, verify your setup:

```bash
# Check Python version
sudo -u lewis bash -c "source /opt/lewis/activate_lewis_python.sh && python --version"

# Validate environment
sudo -u lewis bash -c "source /opt/lewis/activate_lewis_python.sh && python validate_python_env.py"

# Test LEWIS imports
sudo -u lewis bash -c "source /opt/lewis/activate_lewis_python.sh && python -c 'import lewis; print(\"LEWIS OK\")'"
```

## Directory Structure

```
/opt/pyenv/                     # pyenv installation
├── bin/pyenv                   # pyenv binary
├── versions/3.11.9/           # Python 3.11.9 installation
│   ├── bin/python             # Python 3.11.9 binary
│   └── lib/python3.11/        # Python libraries
└── ...

/opt/lewis/                     # LEWIS installation
├── venv/                      # Virtual environment (uses Python 3.11.9)
├── activate_lewis_python.sh   # Environment activation script
├── validate_python_env.py     # Environment validator
└── ...
```

## Configuration Files

### 1. System Profile (`/etc/profile.d/pyenv.sh`)
```bash
export PYENV_ROOT="/opt/pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

### 2. LEWIS Activation Script (`/opt/lewis/activate_lewis_python.sh`)
```bash
#!/bin/bash
export PYENV_ROOT="/opt/pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
cd /opt/lewis
pyenv local 3.11.9
source /opt/lewis/venv/bin/activate
```

### 3. Systemd Service
The service is configured to use the pyenv Python:
```ini
[Service]
Environment=PYENV_ROOT=/opt/pyenv
Environment=PATH=/opt/pyenv/bin:/opt/lewis/venv/bin:/usr/local/bin:/usr/bin
ExecStart=/bin/bash -c 'source /opt/lewis/activate_lewis_python.sh && python lewis.py --mode server'
```

## Optimized Dependencies

LEWIS includes `requirements-python311.txt` with version pins optimized for Python 3.11.9:

- **PyTorch**: `>=1.13.0,<2.1.0`
- **Transformers**: `>=4.21.0,<5.0.0`  
- **NumPy**: `>=1.21.0,<1.25.0`
- **Flask**: `>=2.2.0,<2.4.0`
- And many more...

## Troubleshooting

### Python Build Fails
```bash
# Install additional dependencies
sudo apt-get install -y liblzma-dev python3-openssl

# Try manual installation
sudo ./install_python311.sh
```

### Import Errors
```bash
# Validate environment
sudo -u lewis python3 /opt/lewis/validate_python_env.py

# Reinstall dependencies
sudo -u lewis bash -c "source /opt/lewis/activate_lewis_python.sh && pip install --force-reinstall -r requirements-python311.txt"
```

### Service Won't Start
```bash
# Check service status
sudo systemctl status lewis

# Check Python path
sudo -u lewis bash -c "source /opt/lewis/activate_lewis_python.sh && which python"

# Test manual start
sudo -u lewis /opt/lewis/start_lewis.sh --mode cli
```

### pyenv Not Found
```bash
# Reload shell environment
source /etc/profile.d/pyenv.sh

# Verify pyenv installation
pyenv --version
pyenv versions
```

## Usage Examples

### Start LEWIS CLI
```bash
# Method 1: Direct command
lewis

# Method 2: Manual activation
sudo -u lewis bash
source /opt/lewis/activate_lewis_python.sh
python lewis.py --mode cli
```

### Start LEWIS GUI
```bash
lewis-gui
```

### Service Management
```bash
# Start service
sudo systemctl start lewis

# View logs
sudo journalctl -u lewis -f

# Restart service
sudo systemctl restart lewis
```

### Development Mode
```bash
# Activate environment
sudo -u lewis bash
source /opt/lewis/activate_lewis_python.sh

# Install additional packages
pip install package_name

# Run development server
python lewis.py --mode server --debug
```

## Benefits of This Approach

1. **Compatibility**: Python 3.11.9 ensures all dependencies work correctly
2. **Isolation**: No interference with system Python or other applications
3. **Flexibility**: Easy to upgrade or change Python versions
4. **Production Ready**: Proven approach used in production environments
5. **Maintenance**: Easy to maintain and troubleshoot
6. **Future Proof**: Easy to migrate to newer Python versions when dependencies support them

## Migration Notes

If you previously installed LEWIS with system Python:

1. **Backup**: Back up your LEWIS configuration and data
2. **Uninstall**: Remove old LEWIS installation
3. **Reinstall**: Run new installation script
4. **Restore**: Restore your configuration and data

The new installation will not affect your system Python or other applications.

---

**LEWIS - Linux Environment Working Intelligence System**  
**© 2024 ZehraSec | Created by Yashab Alam**
