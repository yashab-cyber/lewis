# LEWIS Getting Started Guide

Welcome to LEWIS! This guide will help you get started with the Linux Environment Working Intelligence System quickly and efficiently.

## 🎯 Quick Start Overview

LEWIS is an AI-powered cybersecurity platform that uses natural language processing to simplify complex security operations. You can interact with LEWIS through:

- **Command Line Interface (CLI)** - Terminal-based interaction
- **Web Dashboard** - Browser-based interface
- **REST API** - Programmatic integration
- **Voice Commands** - Speech-based interaction (optional)

## 🚀 First Steps

### 1. Verify Installation

```bash
# Check LEWIS version
lewis --version

# Verify all components are working
lewis --health-check

# View system status
lewis status
```

Expected output:
```
LEWIS v1.0.0 - Linux Environment Working Intelligence System
✅ Core Engine: Operational
✅ AI Engine: Ready
✅ Database: Connected
✅ Tools: 47 tools available
✅ Security: Enabled
```

### 2. Initial Configuration

```bash
# Run initial setup wizard
lewis --setup

# Configure basic settings
lewis config set user.name "Your Name"
lewis config set user.email "your.email@company.com"

# Set security preferences
lewis config set security.level "standard"
lewis config set logging.level "info"
```

### 3. Authentication Setup

```bash
# Create your user account
lewis user create --username admin --role administrator

# Set password (will prompt securely)
lewis user password admin

# Login
lewis login admin
```

## 💻 Interface Options

### Command Line Interface (CLI)

The CLI is the primary interface for LEWIS, offering powerful natural language command processing.

#### Starting CLI Mode
```bash
# Start interactive CLI
lewis

# Start with voice support
lewis --voice

# Start with debug mode
lewis --debug
```

#### Basic CLI Commands
```bash
# Inside LEWIS CLI (lewis>)
help                    # Show available commands
status                  # Show system status
scan 192.168.1.1       # Scan a single host
scan 192.168.1.0/24    # Scan a network
tools list              # List available tools
config show             # Show current configuration
exit                    # Exit LEWIS
```

### Web Dashboard

The web interface provides a modern, intuitive way to interact with LEWIS.

#### Starting Web Mode
```bash
# Start web server (default port 8000)
lewis --mode server

# Start on custom port
lewis --mode server --port 8080

# Start with custom host binding
lewis --mode server --host 0.0.0.0 --port 8000
```

#### Accessing Web Dashboard
1. Open browser and navigate to: `http://localhost:8000`
2. Login with your credentials
3. Explore the dashboard features

### Voice Commands (Optional)

Enable voice interaction for hands-free operation.

#### Setup Voice Assistant
```bash
# Install voice dependencies
sudo apt install -y espeak-ng portaudio19-dev

# Configure voice settings
lewis config set voice.enabled true
lewis config set voice.wake_word "lewis"
lewis config set voice.language "en-US"

# Test voice functionality
lewis --voice --test
```

## 🔍 Your First Security Scan

Let's perform your first security scan using LEWIS!

### 1. Network Discovery

```bash
# Start LEWIS CLI
lewis

# Discover hosts on your network
lewis> discover network 192.168.1.0/24

# Or use natural language
lewis> "Show me all devices on my local network"
```

### 2. Host Scanning

```bash
# Scan a specific host
lewis> scan host 192.168.1.100

# Comprehensive scan with service detection
lewis> "Perform a detailed security scan of 192.168.1.100 including service enumeration"

# Quick vulnerability check
lewis> "Check 192.168.1.100 for common vulnerabilities"
```

### 3. Web Application Testing

```bash
# Basic web scan
lewis> scan web https://example.com

# Comprehensive web assessment
lewis> "Assess the security of https://example.com including directory enumeration and vulnerability scanning"

# SSL/TLS analysis
lewis> "Analyze SSL configuration of https://example.com"
```

### 4. Generate Reports

```bash
# Generate scan report
lewis> "Generate a report for the last scan"

# Executive summary
lewis> "Create an executive summary of today's security findings"

# Export to PDF
lewis> "Export the last report as PDF"
```

## 📊 Understanding Results

### Scan Output Format

LEWIS provides structured output in multiple formats:

#### CLI Output
```
[INFO] Starting network scan of 192.168.1.0/24
[INFO] Discovered 12 hosts
[SCAN] 192.168.1.1 - Router (22/tcp, 80/tcp, 443/tcp)
[SCAN] 192.168.1.100 - Server (22/tcp, 80/tcp, 443/tcp, 3306/tcp)
[WARN] 192.168.1.100 - MySQL service detected (potential security risk)
[INFO] Scan completed in 45 seconds
```

#### Web Dashboard
- Real-time progress indicators
- Interactive network maps
- Detailed host information
- Vulnerability risk scores
- Exportable reports

### Result Categories

#### 🟢 **Low Risk** - Informational findings
- Open ports with secure configurations
- Properly configured services
- Up-to-date software versions

#### 🟡 **Medium Risk** - Potential security concerns
- Default configurations
- Information disclosure
- Missing security headers

#### 🔴 **High Risk** - Critical security issues
- Known vulnerabilities
- Weak authentication
- Exposed sensitive services

#### ⚫ **Critical** - Immediate attention required
- Remote code execution vulnerabilities
- Unauthenticated access
- Data exposure

## 🛠️ Common Tasks

### Tool Management

```bash
# List all available tools
lewis> tools list

# Show tool information
lewis> tools info nmap

# Check tool status
lewis> tools status

# Update tool definitions
lewis> tools update
```

### Configuration Management

```bash
# Show current configuration
lewis> config show

# Set configuration values
lewis> config set ai.temperature 0.7
lewis> config set scan.timeout 300

# Reset to defaults
lewis> config reset

# Backup configuration
lewis> config backup /path/to/backup.yaml
```

### User Management

```bash
# Create new user
lewis> user create analyst --role analyst

# List users
lewis> user list

# Modify user permissions
lewis> user modify analyst --add-permission scan_network

# Remove user
lewis> user remove analyst
```

### Workspace Management

```bash
# Create project workspace
lewis> workspace create "penetration_test_2025"

# Switch workspace
lewis> workspace switch "penetration_test_2025"

# List workspaces
lewis> workspace list

# Export workspace data
lewis> workspace export /path/to/export.zip
```

## 🎨 Customization Basics

### Command Aliases

Create shortcuts for frequently used commands:

```bash
# Add custom aliases
lewis> alias add "quickscan" "scan host {target} --quick"
lewis> alias add "webcheck" "scan web {url} --comprehensive"

# Use aliases
lewis> quickscan 192.168.1.100
lewis> webcheck https://example.com
```

### Custom Scripts

Automate complex workflows:

```python
# ~/.lewis/scripts/network_audit.py
def network_audit(network):
    """Comprehensive network security audit"""
    lewis.scan_network(network, detailed=True)
    lewis.check_vulnerabilities()
    lewis.generate_report("network_audit")
    lewis.notify_completion()
```

```bash
# Run custom script
lewis> script run network_audit 192.168.1.0/24
```

### Templates

Create reusable scan templates:

```yaml
# ~/.lewis/templates/web_audit.yaml
name: "Web Application Security Audit"
description: "Comprehensive web application security assessment"
tools:
  - nikto
  - dirb
  - sqlmap
  - ssl-enum
options:
  timeout: 3600
  detailed: true
  include_headers: true
```

```bash
# Use template
lewis> template run web_audit --target https://example.com
```

## 📈 Performance Tips

### Optimize Scan Performance

```bash
# Parallel scanning
lewis> config set scan.parallel_threads 10

# Scan timeout configuration
lewis> config set scan.timeout 300

# Memory optimization
lewis> config set ai.cache_size "1GB"
```

### Resource Management

```bash
# Monitor resource usage
lewis> system resources

# Set resource limits
lewis> config set system.max_memory "4GB"
lewis> config set system.max_cpu_percent 80
```

## 🔒 Security Best Practices

### Authentication

```bash
# Enable two-factor authentication
lewis> user 2fa enable

# Set session timeout
lewis> config set security.session_timeout 3600

# Require strong passwords
lewis> config set security.password_policy strong
```

### Audit Logging

```bash
# Enable comprehensive logging
lewis> config set logging.audit true
lewis> config set logging.level debug

# View audit logs
lewis> logs audit --tail 100

# Export logs
lewis> logs export /path/to/logs.zip
```

### Network Security

```bash
# Restrict access by IP
lewis> config set security.allowed_ips "192.168.1.0/24,10.0.0.0/8"

# Enable SSL/TLS
lewis> config set web.ssl true
lewis> config set web.ssl_cert "/path/to/cert.pem"
```

## 🆘 Getting Help

### Built-in Help

```bash
# General help
lewis> help

# Command-specific help
lewis> help scan
lewis> help config

# Show examples
lewis> examples scan
lewis> examples report
```

### Documentation

```bash
# Open documentation
lewis> docs

# Search documentation
lewis> docs search "vulnerability scanning"

# Show command reference
lewis> reference
```

### Community Support

- 📧 **Email**: yashabalam707@gmail.com
- 💬 **Discord**: [ZehraSec Community](https://discord.gg/zehrasec)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yashab-cyber/lewis/issues)
- 📖 **Documentation**: [docs.lewis-security.com](https://docs.lewis-security.com)

## 📚 Next Steps

Now that you're familiar with the basics:

1. **[User Guide](03-user-guide.md)** - Deep dive into LEWIS features
2. **[Configuration](04-configuration.md)** - Advanced configuration options
3. **[Security](08-security.md)** - Secure your LEWIS deployment
4. **[API Reference](05-api-reference.md)** - Programmatic integration
5. **[Troubleshooting](10-troubleshooting.md)** - Common issues and solutions

## 🎓 Training Resources

### Hands-on Tutorials
- **Basic Network Scanning** - 30 minutes
- **Web Application Testing** - 45 minutes  
- **Vulnerability Assessment** - 60 minutes
- **Report Generation** - 20 minutes

### Video Tutorials
- [LEWIS Quick Start](https://youtube.com/zehrasec/lewis-quickstart)
- [Advanced Features](https://youtube.com/zehrasec/lewis-advanced)
- [Best Practices](https://youtube.com/zehrasec/lewis-best-practices)

### Practice Labs
- **Home Network Assessment** - Scan your own network safely
- **Web App Testing Lab** - Practice on intentionally vulnerable applications
- **Report Generation** - Create professional security reports

---

**📝 Getting Started Guide Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)
