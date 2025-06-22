# LEWIS User Guide

This comprehensive guide covers all aspects of using LEWIS for cybersecurity operations, from basic commands to advanced workflows.

## 🎯 Core Concepts

### Natural Language Processing

LEWIS understands natural language commands, making cybersecurity tools accessible through conversational interaction:

```bash
# Traditional command
nmap -sS -sV -O -A 192.168.1.100

# LEWIS natural language equivalent
lewis> "Perform a comprehensive scan of 192.168.1.100 including service detection and OS fingerprinting"
```

### Intent Recognition

LEWIS recognizes user intent and translates it into appropriate tool execution:

- **Scanning Intent**: "scan", "check", "examine", "probe"
- **Assessment Intent**: "assess", "test", "evaluate", "analyze"
- **Information Gathering**: "discover", "enumerate", "find", "gather"
- **Reporting Intent**: "report", "summarize", "document", "export"

### Context Awareness

LEWIS maintains context throughout conversations:

```bash
lewis> scan 192.168.1.100
lewis> "Check it for web vulnerabilities"  # Refers to 192.168.1.100
lewis> "Generate a report for this host"   # Still refers to 192.168.1.100
```

## 🔍 Scanning Operations

### Network Discovery

#### Host Discovery
```bash
# Basic host discovery
lewis> discover 192.168.1.0/24

# Natural language
lewis> "Find all active hosts in 192.168.1.0/24"
lewis> "Show me devices on my network"

# Advanced discovery with OS detection
lewis> "Discover hosts on 192.168.1.0/24 and identify their operating systems"
```

#### Service Discovery
```bash
# Port scanning
lewis> scan ports 192.168.1.100

# Service enumeration
lewis> "Enumerate services on 192.168.1.100"

# Version detection
lewis> "Identify service versions on 192.168.1.100"
```

### Vulnerability Assessment

#### Automated Vulnerability Scanning
```bash
# Basic vulnerability scan
lewis> vuln scan 192.168.1.100

# Comprehensive assessment
lewis> "Perform a complete vulnerability assessment of 192.168.1.100"

# Specific vulnerability checks
lewis> "Check 192.168.1.100 for CVE-2021-44228"  # Log4j vulnerability
```

#### Web Application Security
```bash
# Basic web scan
lewis> scan web https://example.com

# Comprehensive web assessment
lewis> "Test https://example.com for all common web vulnerabilities"

# Specific tests
lewis> "Check https://example.com for SQL injection vulnerabilities"
lewis> "Test https://example.com for XSS vulnerabilities"
lewis> "Analyze SSL configuration of https://example.com"
```

### Information Gathering

#### DNS Enumeration
```bash
# Basic DNS lookup
lewis> dns lookup example.com

# Comprehensive DNS enumeration
lewis> "Perform complete DNS enumeration of example.com"

# Subdomain discovery
lewis> "Find all subdomains of example.com"
```

#### WHOIS Information
```bash
# Domain information
lewis> whois example.com

# Natural language
lewis> "Get registration information for example.com"
```

#### Social Engineering Information
```bash
# Email harvesting
lewis> "Gather email addresses for example.com"

# Employee information
lewis> "Find employees of Example Company on social media"
```

## 🛠️ Tool Integration

### Supported Tool Categories

#### Network Scanners
- **Nmap** - Network discovery and security scanning
- **Masscan** - High-speed port scanner
- **Zmap** - Internet-wide scanning
- **Unicornscan** - Information gathering

#### Web Application Scanners
- **Nikto** - Web vulnerability scanner
- **Dirb/Dirbuster** - Directory enumeration
- **Gobuster** - URI/DNS brute-forcer
- **SQLMap** - SQL injection detection and exploitation
- **W3AF** - Web application attack and audit framework

#### Vulnerability Scanners
- **OpenVAS** - Comprehensive vulnerability assessment
- **Nuclei** - Fast vulnerability scanner based on templates
- **Nessus** - Professional vulnerability scanner

#### Information Gathering Tools
- **TheHarvester** - Email, subdomain, and people names harvester
- **Subfinder** - Subdomain discovery tool
- **Amass** - In-depth attack surface mapping
- **Fierce** - Domain scanner

### Tool Management

#### List Available Tools
```bash
# Show all tools
lewis> tools list

# Show tools by category
lewis> tools list --category scanner
lewis> tools list --category web

# Show tool details
lewis> tools info nmap
```

#### Tool Configuration
```bash
# Configure tool paths
lewis> tools config nmap --path /usr/bin/nmap

# Set tool preferences
lewis> tools config nikto --timeout 300

# Update tool definitions
lewis> tools update
```

#### Custom Tool Integration
```bash
# Add custom tool
lewis> tools add custom_scanner --path /opt/custom/scanner --type scanner

# Create tool wrapper
lewis> tools wrapper create my_tool.py
```

## 📊 Reporting and Analytics

### Report Generation

#### Automatic Reports
```bash
# Generate scan report
lewis> "Generate a report for the last scan"

# Executive summary
lewis> "Create an executive summary of today's findings"

# Detailed technical report
lewis> "Generate a detailed technical report with all findings"
```

#### Custom Reports
```bash
# Vulnerability-focused report
lewis> "Create a vulnerability report for the last week"

# Compliance report
lewis> "Generate a PCI DSS compliance report"

# Risk assessment report
lewis> "Create a risk assessment report for 192.168.1.0/24"
```

#### Report Formats
```bash
# PDF export
lewis> "Export the last report as PDF"

# HTML report
lewis> "Generate HTML report for web viewing"

# JSON data export
lewis> "Export findings as JSON"

# CSV for spreadsheet analysis
lewis> "Export vulnerability data as CSV"
```

### Analytics Dashboard

#### Real-time Monitoring
```bash
# Start web dashboard
lewis --mode server

# View analytics at http://localhost:8000/analytics
```

#### Key Metrics
- **Scan Performance**: Success rates, timing, coverage
- **Vulnerability Trends**: New discoveries, remediation rates
- **Risk Scores**: Host-based and network-wide risk assessment
- **Tool Usage**: Effectiveness and reliability metrics

### Data Visualization

#### Network Maps
- Interactive network topology
- Host relationships and dependencies
- Vulnerability distribution
- Risk heat maps

#### Trend Analysis
- Vulnerability discovery over time
- Remediation progress tracking
- Tool effectiveness metrics
- Security posture improvements

## 🔒 Security and Compliance

### Access Control

#### User Management
```bash
# Create users with specific roles
lewis> user create analyst --role security_analyst
lewis> user create admin --role administrator
lewis> user create readonly --role viewer

# Assign permissions
lewis> user permissions analyst --add scan_network
lewis> user permissions analyst --add generate_reports
```

#### Role-Based Access Control
- **Administrator**: Full system access
- **Security Analyst**: Scanning and reporting
- **Junior Analyst**: Limited scanning capabilities
- **Viewer**: Read-only access to reports
- **Auditor**: Access to logs and compliance data

### Audit and Compliance

#### Audit Logging
```bash
# Enable comprehensive auditing
lewis> config set audit.enabled true
lewis> config set audit.level detailed

# View audit logs
lewis> audit log --filter user:analyst
lewis> audit log --filter action:scan
lewis> audit log --since "2025-06-01"
```

#### Compliance Frameworks
```bash
# PCI DSS compliance checks
lewis> compliance check pci-dss

# NIST framework assessment
lewis> compliance check nist

# Custom compliance policies
lewis> compliance policy create custom_policy.yaml
```

### Data Protection

#### Encryption
```bash
# Enable data encryption
lewis> config set security.encryption true

# Configure encryption keys
lewis> security keys generate
lewis> security keys rotate
```

#### Data Retention
```bash
# Set retention policies
lewis> config set data.retention.scans 90d
lewis> config set data.retention.logs 365d

# Manual data cleanup
lewis> data cleanup --older-than 30d
```

## 🔧 Advanced Features

### Automation and Scripting

#### Workflow Automation
```python
# ~/.lewis/workflows/network_audit.py
def network_audit_workflow(network):
    """Automated network security audit"""
    
    # Discovery phase
    hosts = lewis.discover_hosts(network)
    
    # Scanning phase
    for host in hosts:
        lewis.scan_host(host, comprehensive=True)
        lewis.vuln_scan(host)
    
    # Reporting phase
    lewis.generate_report("network_audit", format="pdf")
    lewis.notify_completion("Network audit completed")
```

```bash
# Execute workflow
lewis> workflow run network_audit 192.168.1.0/24
```

#### Scheduled Operations
```bash
# Schedule daily vulnerability scans
lewis> schedule create "daily_vuln_scan" --cron "0 2 * * *" --command "vuln scan all_hosts"

# Schedule weekly reports
lewis> schedule create "weekly_report" --cron "0 8 * * 1" --command "report generate weekly"
```

### Integration Capabilities

#### SIEM Integration
```bash
# Configure Splunk integration
lewis> integration add splunk --host splunk.company.com --token API_TOKEN

# Send events to SIEM
lewis> config set siem.auto_export true
```

#### Ticketing System Integration
```bash
# Configure Jira integration
lewis> integration add jira --url https://company.atlassian.net --token API_TOKEN

# Auto-create tickets for high-risk findings
lewis> config set ticketing.auto_create_high_risk true
```

#### CI/CD Pipeline Integration
```bash
# Security scan in CI/CD
lewis scan web $BUILD_URL --format json --output security_report.json

# Exit with error code if high-risk vulnerabilities found
lewis scan web $BUILD_URL --fail-on high
```

### Machine Learning Features

#### Behavioral Analysis
```bash
# Enable AI-powered anomaly detection
lewis> ai enable anomaly_detection

# Train on historical data
lewis> ai train --dataset scan_history

# Analyze network behavior
lewis> "Analyze network traffic patterns for anomalies"
```

#### Intelligent Recommendations
```bash
# Get security recommendations
lewis> "What security improvements should I prioritize?"

# Tool selection assistance
lewis> "What's the best tool to test for SQL injection?"

# Risk prioritization
lewis> "Which vulnerabilities should I fix first?"
```

## 📱 Multi-Modal Interfaces

### Voice Commands

#### Setup and Configuration
```bash
# Enable voice assistant
lewis> config set voice.enabled true
lewis> config set voice.wake_word "lewis"

# Test voice functionality
lewis --voice --test
```

#### Voice Command Examples
```
"Lewis, scan one nine two dot one six eight dot one dot one hundred"
"Lewis, check example dot com for vulnerabilities"
"Lewis, generate a report for the last scan"
"Lewis, show me the security status of my network"
```

### Mobile Interface

#### Web Mobile Access
- Responsive web interface accessible on mobile devices
- Touch-optimized controls
- Essential scanning functions
- Real-time notifications

#### Mobile App Features
- Quick scan initiation
- Report viewing and sharing
- Alert notifications
- Dashboard summaries

### API Integration

#### REST API Usage
```python
import requests

# Authenticate
response = requests.post('https://lewis.company.com/api/v1/auth/login', 
                        json={'username': 'analyst', 'password': 'password'})
token = response.json()['token']

# Initiate scan
headers = {'Authorization': f'Bearer {token}'}
scan_response = requests.post('https://lewis.company.com/api/v1/scan/network',
                             headers=headers,
                             json={'target': '192.168.1.0/24'})

# Get results
scan_id = scan_response.json()['scan_id']
results = requests.get(f'https://lewis.company.com/api/v1/scan/{scan_id}/results',
                      headers=headers)
```

#### WebSocket Integration
```javascript
// Real-time scan updates
const ws = new WebSocket('wss://lewis.company.com/api/v1/ws');

ws.on('scan_progress', (data) => {
    console.log(`Scan progress: ${data.percentage}%`);
});

ws.on('vulnerability_found', (data) => {
    console.log(`Vulnerability found: ${data.cve_id}`);
});
```

## 🎨 Customization

### Themes and Appearance

#### CLI Themes
```bash
# Available themes
lewis> theme list

# Apply theme
lewis> theme set dark_matrix
lewis> theme set light_professional

# Custom theme
lewis> theme create custom --colors "primary:#00ff00,secondary:#ff0000"
```

#### Web Interface Customization
```bash
# Company branding
lewis> config set web.company_name "Your Company"
lewis> config set web.logo_url "/path/to/logo.png"

# Color scheme
lewis> config set web.theme custom
lewis> config set web.primary_color "#1a73e8"
```

### Custom Commands

#### Command Aliases
```bash
# Create shortcuts
lewis> alias add "netscan" "scan network {target} --comprehensive"
lewis> alias add "webtest" "scan web {target} --all-checks"

# Use aliases
lewis> netscan 192.168.1.0/24
lewis> webtest https://example.com
```

#### Custom Scripts
```bash
# Create custom command
lewis> command create pentest_workflow --script /path/to/pentest.py

# Execute custom command
lewis> pentest_workflow --target 192.168.1.100
```

### Plugin System

#### Available Plugins
```bash
# List available plugins
lewis> plugins list

# Install plugin
lewis> plugins install advanced_reporting

# Enable plugin
lewis> plugins enable advanced_reporting
```

#### Custom Plugin Development
```python
# ~/.lewis/plugins/custom_scanner.py
from lewis.plugins import Plugin

class CustomScanner(Plugin):
    name = "custom_scanner"
    version = "1.0.0"
    
    def scan(self, target):
        # Custom scanning logic
        return results
```

## 🔍 Troubleshooting

### Common Issues

#### Scanning Problems
```bash
# Check tool availability
lewis> tools status

# Verify network connectivity
lewis> network test

# Debug scan execution
lewis> scan debug 192.168.1.100
```

#### Performance Issues
```bash
# Monitor system resources
lewis> system resources

# Optimize configuration
lewis> config optimize

# Clear cache
lewis> cache clear
```

#### Authentication Issues
```bash
# Reset user password
lewis> user password reset analyst

# Check session status
lewis> auth status

# Refresh authentication token
lewis> auth refresh
```

### Diagnostic Tools

#### System Diagnostics
```bash
# Full system check
lewis> diagnostics --full

# Component-specific checks
lewis> diagnostics --component database
lewis> diagnostics --component ai_engine

# Performance diagnostics
lewis> diagnostics --performance
```

#### Log Analysis
```bash
# View recent logs
lewis> logs tail

# Search logs
lewis> logs search "error"

# Export logs for support
lewis> logs export --level error --since "1 hour ago"
```

## 📚 Best Practices

### Scanning Best Practices

#### Planning
- Define clear scope and objectives
- Obtain proper authorization
- Schedule scans during maintenance windows
- Consider network impact

#### Execution
- Start with passive reconnaissance
- Gradually increase scan intensity
- Monitor for defensive responses
- Document all activities

#### Analysis
- Prioritize findings by risk
- Validate all discovered vulnerabilities
- Consider false positive rates
- Plan remediation activities

### Security Best Practices

#### Access Control
- Use strong authentication
- Implement least privilege principle
- Regular access reviews
- Monitor user activities

#### Data Protection
- Encrypt sensitive data
- Secure data transmission
- Regular backups
- Proper data disposal

#### Network Security
- Segment LEWIS deployment
- Use VPN for remote access
- Monitor network traffic
- Regular security updates

---

**📝 User Guide Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)
