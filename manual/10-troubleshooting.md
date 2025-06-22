# LEWIS Troubleshooting Guide

This guide provides solutions to common issues, error messages, and problems you might encounter while using LEWIS.

## 🚨 Common Issues and Solutions

### Installation Issues

#### Issue: Permission Denied During Installation
```bash
# Error message
Permission denied: '/opt/lewis'

# Solutions
# 1. Run with sudo
sudo bash install.sh

# 2. Create directory with proper permissions
sudo mkdir -p /opt/lewis
sudo chown $USER:$USER /opt/lewis

# 3. Install to user directory
./install.sh --prefix ~/.local
```

#### Issue: Python Version Incompatibility
```bash
# Error message
LEWIS requires Python 3.8 or higher. Found: Python 3.7.3

# Solutions
# Ubuntu/Debian - Install newer Python
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-pip

# Set as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# CentOS/RHEL - Enable Python 3.8
sudo dnf install python38 python38-pip
```

#### Issue: Missing System Dependencies
```bash
# Error message
ERROR: Microsoft Visual C++ 14.0 is required
# OR
fatal error: 'openssl/opensslv.h' file not found

# Solutions
# Ubuntu/Debian
sudo apt install build-essential libssl-dev libffi-dev python3-dev

# CentOS/RHEL
sudo dnf groupinstall "Development Tools"
sudo dnf install openssl-devel libffi-devel python3-devel

# Arch Linux
sudo pacman -S base-devel openssl libffi
```

### Configuration Issues

#### Issue: Configuration File Not Found
```bash
# Error message
FileNotFoundError: [Errno 2] No such file or directory: '/etc/lewis/config.yaml'

# Solutions
# 1. Create default configuration
lewis --init

# 2. Specify custom config path
lewis --config ~/.lewis/config.yaml

# 3. Set environment variable
export LEWIS_CONFIG_PATH="/path/to/config.yaml"
```

#### Issue: Invalid Configuration Format
```bash
# Error message
yaml.scanner.ScannerError: mapping values are not allowed here

# Solutions
# 1. Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('/etc/lewis/config.yaml'))"

# 2. Use online YAML validator
# https://yamlchecker.com/

# 3. Reset to default configuration
lewis config reset --backup-current
```

#### Issue: Environment Variable Not Set
```bash
# Error message
ValueError: Environment variable LEWIS_JWT_SECRET not set

# Solutions
# 1. Set required environment variables
export LEWIS_JWT_SECRET="your_32_character_secret_key_here"
export LEWIS_DB_PASSWORD="secure_database_password"

# 2. Create .env file
cat > ~/.lewis/.env << EOF
LEWIS_JWT_SECRET=your_32_character_secret_key_here
LEWIS_DB_PASSWORD=secure_database_password
EOF

# 3. Generate secure secrets
lewis config generate-secrets
```

### Database Issues

#### Issue: Database Connection Failed
```bash
# Error message
pymongo.errors.ServerSelectionTimeoutError: [Errno 111] Connection refused

# Diagnosis
lewis database test

# Solutions
# 1. Check MongoDB status
sudo systemctl status mongod
sudo systemctl start mongod

# 2. Verify connection settings
lewis config show database

# 3. Test manual connection
mongo --host localhost --port 27017

# 4. Check firewall
sudo ufw status
sudo ufw allow 27017
```

#### Issue: Authentication Failed to Database
```bash
# Error message
pymongo.errors.OperationFailure: Authentication failed

# Solutions
# 1. Verify credentials
lewis config show database.username
lewis config test database

# 2. Reset database password
mongo
> use admin
> db.changeUserPassword("lewis", "new_password")

# 3. Update configuration
lewis config set database.password "new_password"
```

#### Issue: Database Disk Full
```bash
# Error message
MongoError: No space left on device

# Diagnosis
df -h
du -sh /var/lib/mongodb/*

# Solutions
# 1. Clean up old data
lewis database cleanup --older-than 30d

# 2. Compact database
lewis database compact

# 3. Add more disk space or move database
sudo systemctl stop mongod
sudo mv /var/lib/mongodb /new/location/mongodb
sudo ln -s /new/location/mongodb /var/lib/mongodb
sudo systemctl start mongod
```

### Network Issues

#### Issue: Network Timeout Errors
```bash
# Error message
requests.exceptions.ConnectTimeout: HTTPSConnectionPool

# Diagnosis
lewis network test
ping google.com
curl -I https://google.com

# Solutions
# 1. Check internet connectivity
route -n
cat /etc/resolv.conf

# 2. Configure proxy if needed
lewis config set network.proxy.http "http://proxy.company.com:8080"
lewis config set network.proxy.https "https://proxy.company.com:8080"

# 3. Adjust timeout settings
lewis config set network.timeout 60
```

#### Issue: Port Already in Use
```bash
# Error message
OSError: [Errno 98] Address already in use

# Diagnosis
sudo netstat -tulpn | grep :8000
sudo ss -tulpn | grep :8000

# Solutions
# 1. Kill process using the port
sudo kill $(sudo lsof -t -i:8000)

# 2. Use different port
lewis --mode server --port 8080

# 3. Configure different port permanently
lewis config set network.web.port 8080
```

#### Issue: SSL Certificate Problems
```bash
# Error message
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED]

# Solutions
# 1. For development, disable SSL verification
lewis config set network.ssl_verify false

# 2. Install proper certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# 3. Add custom CA certificate
sudo cp company-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

### Tool Integration Issues

#### Issue: Tool Not Found
```bash
# Error message
ToolNotFoundError: Tool 'nmap' not found in PATH

# Diagnosis
lewis tools status
which nmap

# Solutions
# 1. Install missing tool
sudo apt install nmap

# 2. Add tool to PATH
echo 'export PATH=$PATH:/opt/custom/tools' >> ~/.bashrc
source ~/.bashrc

# 3. Configure custom tool path
lewis tools config nmap --path /usr/local/bin/nmap
```

#### Issue: Tool Permission Denied
```bash
# Error message
PermissionError: [Errno 13] Permission denied: '/usr/bin/nmap'

# Solutions
# 1. Add user to appropriate group
sudo usermod -a -G netdev $USER

# 2. Configure sudo access for specific tools
sudo visudo
# Add: lewis ALL=(ALL) NOPASSWD: /usr/bin/nmap

# 3. Run LEWIS with appropriate privileges
sudo lewis
```

#### Issue: Tool Execution Timeout
```bash
# Error message
ToolTimeoutError: Tool execution exceeded 300 seconds

# Solutions
# 1. Increase timeout for specific tool
lewis tools config nmap --timeout 600

# 2. Increase global timeout
lewis config set tools.execution.timeout 600

# 3. Optimize scan parameters
lewis config set scanning.defaults.rate_limit 50
```

### Authentication Issues

#### Issue: Login Failed
```bash
# Error message
AuthenticationError: Invalid username or password

# Solutions
# 1. Reset password
lewis user password reset analyst

# 2. Check account status
lewis user status analyst

# 3. Unlock account if locked
lewis user unlock analyst

# 4. Check authentication logs
lewis logs search "authentication.*failed" --since "1 hour"
```

#### Issue: JWT Token Expired
```bash
# Error message
JWTError: Token has expired

# Solutions
# 1. Login again
lewis login analyst

# 2. Increase token expiration time
lewis config set security.authentication.jwt_expiration 7200

# 3. Enable token refresh
lewis config set security.authentication.jwt_refresh_enabled true
```

#### Issue: Two-Factor Authentication Problems
```bash
# Error message
MFAError: Invalid TOTP code

# Solutions
# 1. Check time synchronization
sudo ntpdate -s time.nist.gov

# 2. Generate backup codes
lewis user 2fa backup-codes analyst

# 3. Reset 2FA if necessary
lewis user 2fa reset analyst --admin-override
```

### Performance Issues

#### Issue: Slow Scan Performance
```bash
# Diagnosis
lewis monitor --component scan --duration 60
lewis profile scan 192.168.1.0/24

# Solutions
# 1. Increase parallel execution
lewis config set scanning.defaults.max_concurrent 20

# 2. Optimize tool parameters
lewis tools config nmap --args "-T4 --min-rate 1000"

# 3. Use faster scanning techniques
lewis config set scanning.network.quick_mode true
```

#### Issue: High Memory Usage
```bash
# Diagnosis
lewis monitor --component memory
free -h
top -p $(pgrep lewis)

# Solutions
# 1. Reduce cache size
lewis config set performance.cache_size "512MB"

# 2. Enable garbage collection tuning
lewis config set performance.memory.gc_threshold 0.7

# 3. Restart LEWIS to clear memory
sudo systemctl restart lewis
```

#### Issue: AI Engine Slow Response
```bash
# Diagnosis
lewis ai test --benchmark
lewis profile ai "scan network 192.168.1.0/24"

# Solutions
# 1. Enable GPU acceleration
lewis config set ai.use_gpu true

# 2. Use lighter AI model
lewis config set ai.model_name "microsoft/DialoGPT-small"

# 3. Increase AI timeout
lewis config set ai.timeout 60
```

### Web Interface Issues

#### Issue: Web Interface Not Loading
```bash
# Error message
This site can't be reached

# Diagnosis
curl -I http://localhost:8000
lewis --mode server --debug

# Solutions
# 1. Check service status
sudo systemctl status lewis

# 2. Verify port binding
sudo netstat -tulpn | grep lewis

# 3. Check firewall rules
sudo ufw status
sudo ufw allow 8000
```

#### Issue: 500 Internal Server Error
```bash
# Diagnosis
lewis logs tail --component web --level ERROR

# Solutions
# 1. Check web server logs
tail -f /var/log/lewis/web.log

# 2. Restart web service
sudo systemctl restart lewis

# 3. Clear web cache
lewis cache clear --component web
```

#### Issue: Static Files Not Loading
```bash
# Error message
404 Not Found for /static/css/style.css

# Solutions
# 1. Check static file permissions
ls -la /opt/lewis/static/

# 2. Reconfigure static file serving
lewis config set web.static_files_path "/opt/lewis/static"

# 3. Rebuild static files
lewis web collect-static
```

## 🔧 Diagnostic Commands

### Quick Diagnostic Commands
```bash
# System health check
lewis --health-check

# Component status
lewis status --all

# Configuration validation
lewis config validate

# Network connectivity test
lewis network test

# Database connection test
lewis database test

# Tool availability check
lewis tools status
```

### Detailed Diagnostics
```bash
# Full system diagnostic
lewis diagnostics --full --output diagnostic_report.txt

# Performance analysis
lewis diagnostics --performance --duration 300

# Security audit
lewis diagnostics --security

# Component-specific deep dive
lewis diagnostics --component ai --verbose
```

## 📊 Log Analysis for Troubleshooting

### Common Log Patterns

#### Authentication Issues
```bash
# Failed login attempts
lewis logs search "authentication.*failed" --since "1 hour"

# Account lockouts
lewis logs search "account.*locked" --since "1 day"

# Permission denied
lewis logs search "permission.*denied" --since "1 hour"
```

#### Performance Issues
```bash
# Slow operations
lewis logs search "slow.*query|timeout" --since "1 hour"

# Memory issues
lewis logs search "memory.*error|out.*of.*memory" --since "1 day"

# High CPU usage
lewis logs search "cpu.*high|performance.*degraded" --since "1 hour"
```

#### Network Issues
```bash
# Connection failures
lewis logs search "connection.*failed|network.*error" --since "1 hour"

# Timeout errors
lewis logs search "timeout|timed.*out" --since "1 hour"

# DNS issues
lewis logs search "dns.*error|name.*resolution" --since "1 hour"
```

### Log Analysis Tools
```bash
# Generate log summary
lewis logs analyze --summary --since "1 day"

# Error pattern analysis
lewis logs analyze --errors --pattern-detection

# Performance bottleneck identification
lewis logs analyze --performance --bottlenecks
```

## 🛠️ Recovery Procedures

### Service Recovery

#### LEWIS Service Won't Start
```bash
# Check service status
sudo systemctl status lewis

# View service logs
sudo journalctl -u lewis -f

# Reset service configuration
sudo systemctl daemon-reload
sudo systemctl enable lewis
sudo systemctl start lewis
```

#### Database Recovery
```bash
# Stop LEWIS service
sudo systemctl stop lewis

# Repair MongoDB
sudo mongod --repair --dbpath /var/lib/mongodb

# Restore from backup
lewis backup restore /backup/lewis-backup-latest.tar.gz

# Start service
sudo systemctl start lewis
```

#### Configuration Recovery
```bash
# Backup current configuration
cp /etc/lewis/config.yaml /etc/lewis/config.yaml.backup

# Reset to defaults
lewis config reset

# Restore from backup
lewis config restore /backup/lewis-config-backup.yaml
```

### Data Recovery

#### Scan Data Recovery
```bash
# Check data integrity
lewis database integrity-check

# Recover scan data from logs
lewis data recover --from-logs --since "1 week"

# Export/import scan data
lewis data export scan_data.json
lewis data import scan_data.json
```

#### User Data Recovery
```bash
# Export user data
lewis user export --output users_backup.yaml

# Recreate user from backup
lewis user import users_backup.yaml

# Reset user passwords
lewis user password reset --all-users
```

## 🆘 Emergency Procedures

### System Emergency Reset

#### Complete System Reset
```bash
# WARNING: This will reset all configuration and data
lewis emergency-reset --confirm --backup-first

# Or step by step
lewis backup create emergency_backup.tar.gz
lewis config reset --all
lewis database reset --confirm
lewis user create admin --role administrator
```

#### Partial Reset Options
```bash
# Reset only configuration
lewis reset --config-only

# Reset only database
lewis reset --database-only

# Reset only user accounts
lewis reset --users-only
```

### Security Incident Response

#### Suspected Compromise
```bash
# Immediately lock all accounts
lewis user lock --all

# Enable detailed auditing
lewis config set audit.level maximum

# Export all logs for analysis
lewis logs export --all --output incident_logs.tar.gz

# Generate security report
lewis security incident-report --output security_incident.pdf
```

#### Password Reset After Breach
```bash
# Force password reset for all users
lewis user password reset --all --force-change

# Invalidate all active sessions
lewis auth invalidate-all-sessions

# Rotate all API keys
lewis api-keys rotate --all
```

## 📞 Getting Help

### Before Contacting Support

#### Information to Collect
1. **System Information**
   ```bash
   lewis --version
   uname -a
   python3 --version
   ```

2. **Error Details**
   ```bash
   lewis logs export --level ERROR --since "1 hour"
   lewis diagnostics --full
   ```

3. **Configuration Information**
   ```bash
   lewis config sanitize-export config_sanitized.yaml
   ```

4. **Recent Changes**
   - Configuration modifications
   - System updates
   - New tool installations

### Support Channels

#### Community Support
- 💬 **Discord**: [ZehraSec Community](https://discord.gg/zehrasec)
- 🐛 **GitHub Issues**: [Report Issues](https://github.com/yashab-cyber/lewis/issues)
- 📖 **Documentation**: [docs.lewis-security.com](https://docs.lewis-security.com)

#### Direct Support
- 📧 **Email**: yashabalam707@gmail.com
- 🎫 **Support Portal**: [support.zehrasec.com](https://support.zehrasec.com)

### Creating Effective Bug Reports

#### Bug Report Template
```
**LEWIS Version**: 1.0.0
**Operating System**: Ubuntu 20.04.3 LTS
**Python Version**: 3.9.7

**Description**:
Brief description of the issue

**Steps to Reproduce**:
1. Start LEWIS with: lewis --mode cli
2. Run command: scan 192.168.1.1
3. Error occurs

**Expected Behavior**:
Scan should complete successfully

**Actual Behavior**:
Error message: Tool execution failed

**Error Logs**:
```
[Include relevant log entries]
```

**Configuration** (sanitized):
```
[Include relevant configuration sections]
```

**Additional Context**:
Any other relevant information
```

---

**📝 Troubleshooting Guide Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)
