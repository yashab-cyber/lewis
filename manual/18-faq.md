# LEWIS FAQ - Frequently Asked Questions

This document answers the most commonly asked questions about LEWIS installation, configuration, usage, and troubleshooting.

## 🚀 General Questions

### What is LEWIS?
**LEWIS** (Linux Environment Working Intelligence System) is an AI-powered cybersecurity platform that uses natural language processing to simplify complex security operations. It allows security professionals to interact with cybersecurity tools using plain English commands.

### Who developed LEWIS?
LEWIS was developed by **[Yashab Alam](https://linkedin.com/in/yashabalam)**, founder and CEO of **[ZehraSec](https://www.zehrasec.com)**, a leading cybersecurity company specializing in AI-driven security solutions.

### What makes LEWIS different from other security tools?
- **AI-First Architecture**: Built from the ground up with artificial intelligence
- **Natural Language Interface**: No need to memorize complex command syntax
- **Intelligent Automation**: Automated threat detection and response
- **Comprehensive Integration**: 100+ security tools in one platform
- **Continuous Learning**: Self-improving system that adapts to new threats

### Is LEWIS free to use?
Yes, LEWIS is open-source software released under the MIT License. However, enterprise support and advanced features may require a commercial license.

### What operating systems does LEWIS support?
LEWIS is designed for Linux-based systems including:
- Ubuntu 18.04+
- Debian 10+
- CentOS 7+
- Kali Linux
- Arch Linux
- Termux (Android)

## 📦 Installation Questions

### What are the minimum system requirements?
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM (8GB recommended)
- **Storage**: 10GB free space (20GB recommended)
- **OS**: Linux-based system
- **Network**: Internet connection for AI models and updates

### How do I install LEWIS?
The easiest method is using our automated installer:
```bash
curl -fsSL https://raw.githubusercontent.com/yashab-cyber/lewis/main/install.sh | sudo bash
```

For other installation methods, see our [Installation Guide](01-installation.md).

### Can I install LEWIS without root privileges?
Yes, you can install LEWIS in your home directory:
```bash
./install.sh --prefix ~/.local
```

### Why am I getting permission errors during installation?
This usually happens when installing to system directories. Either:
1. Run the installer with `sudo`
2. Install to a user directory with `--prefix ~/.local`
3. Ensure you have write permissions to the installation directory

### How do I install LEWIS on Docker?
```bash
docker pull yashab/lewis:latest
docker run -it --rm -p 8000:8000 yashab/lewis:latest
```

## ⚙️ Configuration Questions

### Where are LEWIS configuration files located?
- System-wide: `/etc/lewis/`
- User-specific: `~/.lewis/`
- Default config: `/etc/lewis/config.yaml`

### How do I change the default port?
```bash
lewis config set network.web.port 8080
# or
lewis --mode server --port 8080
```

### How do I enable SSL/TLS?
```bash
lewis config set network.web.ssl_enabled true
lewis config set network.web.ssl_cert_path "/path/to/cert.crt"
lewis config set network.web.ssl_key_path "/path/to/private.key"
```

### Can I use LEWIS with a different database?
Yes, LEWIS supports:
- MongoDB (default)
- PostgreSQL
- SQLite

Configure in `/etc/lewis/config.yaml`:
```yaml
database:
  primary:
    type: "postgresql"
    host: "localhost"
    port: 5432
    name: "lewis"
```

### How do I reset LEWIS configuration?
```bash
lewis config reset --backup-current
```

## 🔍 Usage Questions

### How do I start LEWIS?
```bash
# CLI mode
lewis

# Web interface
lewis --mode server

# With voice support
lewis --voice

# Debug mode
lewis --debug
```

### What natural language commands can I use?
Examples include:
- "Scan the network 192.168.1.0/24"
- "Check example.com for vulnerabilities"
- "Generate a security report"
- "Show me all open ports on 192.168.1.100"
- "Test the SSL configuration of https://example.com"

### How do I scan a single host?
```bash
lewis> scan 192.168.1.100
# or
lewis> "Perform a security scan of 192.168.1.100"
```

### How do I scan a network range?
```bash
lewis> scan 192.168.1.0/24
# or
lewis> "Discover all devices on 192.168.1.0/24"
```

### How do I generate reports?
```bash
lewis> "Generate a report for the last scan"
lewis> "Create an executive summary of today's findings"
lewis> "Export the report as PDF"
```

### Can I save scan results?
Yes, scan results are automatically saved to the database. You can also export them:
```bash
lewis> "Export scan results as JSON"
lewis data export scan_results.json
```

### How do I view scan history?
```bash
lewis> history
# or via web interface
lewis --mode server
# Visit http://localhost:8000/scans
```

## 🛠️ Tool Integration Questions

### Which security tools does LEWIS support?
LEWIS integrates with 100+ tools including:
- **Network**: Nmap, Masscan, Zmap
- **Web**: Nikto, SQLMap, Burp Suite
- **Vulnerability**: OpenVAS, Nuclei, Nessus
- **Information**: TheHarvester, Subfinder, Amass

### How do I check which tools are available?
```bash
lewis> tools list
lewis tools status
```

### What if a tool is missing?
Install the missing tool:
```bash
# Ubuntu/Debian
sudo apt install nmap nikto

# Or manually configure path
lewis tools config nmap --path /custom/path/to/nmap
```

### Can I add custom tools?
Yes, you can integrate custom tools:
```bash
lewis tools add custom_tool --path /path/to/tool --category scanner
```

### How do I update tool definitions?
```bash
lewis tools update
```

## 🔒 Security Questions

### Is LEWIS secure?
Yes, LEWIS includes multiple security features:
- JWT-based authentication
- Role-based access control
- Audit logging
- Encrypted data storage
- Command validation

### How do I enable two-factor authentication?
```bash
lewis user 2fa enable your_username
```

### Can I integrate with LDAP/Active Directory?
Yes, configure LDAP authentication:
```yaml
security:
  authentication:
    method: "ldap"
    ldap:
      server: "ldap://company.com"
      base_dn: "ou=users,dc=company,dc=com"
```

### How do I create users and assign roles?
```bash
# Create user
lewis user create analyst --role security_analyst

# Assign permissions
lewis user permissions analyst --add scan_network
```

### Are scan targets validated?
Yes, LEWIS includes built-in target validation to prevent scanning unauthorized hosts. Configure allowed ranges in the security settings.

## 🎯 Performance Questions

### How can I improve scan performance?
1. Increase parallel execution:
   ```bash
   lewis config set scanning.defaults.max_concurrent 20
   ```

2. Use faster scan techniques:
   ```bash
   lewis config set scanning.network.quick_mode true
   ```

3. Enable GPU acceleration for AI:
   ```bash
   lewis config set ai.use_gpu true
   ```

### Why are scans taking so long?
Common causes:
- Network latency or firewalls
- Large target ranges
- Comprehensive scan options
- Resource limitations

Try adjusting scan parameters or using quick scan modes.

### How much memory does LEWIS use?
Memory usage depends on:
- Active scans
- AI model size
- Database cache
- Scan history

Typical usage: 1-4GB RAM

### Can I limit resource usage?
Yes, configure resource limits:
```bash
lewis config set performance.memory.max_usage "2GB"
lewis config set performance.cpu.max_usage 50
```

## 🌐 Network Questions

### Can LEWIS work behind a proxy?
Yes, configure proxy settings:
```bash
lewis config set network.proxy.http "http://proxy.company.com:8080"
lewis config set network.proxy.https "https://proxy.company.com:8080"
```

### How do I configure firewall rules?
```bash
# Allow LEWIS web interface
sudo ufw allow 8000

# Allow from specific network
sudo ufw allow from 192.168.1.0/24 to any port 8000
```

### Can I use LEWIS remotely?
Yes, start the web server and access via browser:
```bash
lewis --mode server --host 0.0.0.0 --port 8000
```

Then visit: `http://your-server-ip:8000`

### Does LEWIS support IPv6?
Yes, LEWIS supports both IPv4 and IPv6 scanning:
```bash
lewis> scan 2001:db8::/32
```

## 📊 Reporting Questions

### What report formats are available?
- PDF (executive and technical reports)
- HTML (web-viewable reports)
- JSON (machine-readable data)
- CSV (spreadsheet-compatible)
- XML (structured data)

### How do I customize reports?
Create custom templates:
```bash
lewis template create custom_report.yaml
lewis report generate --template custom_report
```

### Can I schedule automatic reports?
Yes, using the scheduler:
```bash
lewis schedule create "weekly_report" --cron "0 8 * * 1" --command "report generate weekly"
```

### How do I share reports securely?
Reports can be:
- Exported with password protection
- Shared via secure links with expiration
- Integrated with document management systems

## 🔧 Troubleshooting Questions

### LEWIS won't start - what should I check?
1. Check service status:
   ```bash
   sudo systemctl status lewis
   ```

2. View logs:
   ```bash
   lewis logs tail --level ERROR
   ```

3. Test configuration:
   ```bash
   lewis config validate
   ```

4. Check dependencies:
   ```bash
   lewis --health-check
   ```

### Why can't I connect to the database?
Common solutions:
1. Check database service:
   ```bash
   sudo systemctl status mongod
   ```

2. Test connection:
   ```bash
   lewis database test
   ```

3. Verify credentials:
   ```bash
   lewis config show database
   ```

### Scans are failing - how do I debug?
1. Enable debug mode:
   ```bash
   lewis --debug
   ```

2. Test individual tools:
   ```bash
   lewis tools test nmap
   ```

3. Check tool permissions:
   ```bash
   lewis tools permissions check
   ```

### How do I recover from corrupted data?
1. Stop LEWIS:
   ```bash
   sudo systemctl stop lewis
   ```

2. Restore from backup:
   ```bash
   lewis backup restore /backup/latest.tar.gz
   ```

3. Or reset database:
   ```bash
   lewis database reset --confirm
   ```

## 🎓 Learning Questions

### Where can I learn more about using LEWIS?
- **Documentation**: [docs.lewis-security.com](https://docs.lewis-security.com)
- **Video Tutorials**: [YouTube Channel](https://youtube.com/zehrasec)
- **Training Courses**: [ZehraSec Academy](https://www.zehrasec.com/training)
- **Community Forums**: [ZehraSec Discord](https://discord.gg/zehrasec)

### Are there practice labs available?
Yes, ZehraSec provides hands-on labs:
- Home network assessment labs
- Web application testing environments
- Vulnerable systems for practice

### Can I get certification in LEWIS?
ZehraSec offers certification programs:
- LEWIS Certified User (LCU)
- LEWIS Certified Administrator (LCA)
- LEWIS Certified Developer (LCD)

### How do I contribute to LEWIS development?
1. Fork the repository: [github.com/yashab-cyber/lewis](https://github.com/yashab-cyber/lewis)
2. Read the [Contributing Guide](15-contributing.md)
3. Join the developer community on Discord
4. Submit issues and feature requests

## 🤝 Support Questions

### How do I get help with LEWIS?
Multiple support options:
- 📧 **Email**: yashabalam707@gmail.com
- 💬 **Discord**: [ZehraSec Community](https://discord.gg/zehrasec)
- 🐛 **GitHub**: [Submit Issues](https://github.com/yashab-cyber/lewis/issues)
- 📖 **Documentation**: [Complete Manual](README.md)

### Is commercial support available?
Yes, ZehraSec offers:
- Priority support
- Custom training
- Professional services
- Enterprise licensing

Contact: yashabalam707@gmail.com

### How do I report security vulnerabilities?
Report security issues privately to:
- Email: yashabalam707@gmail.com
- Subject: "LEWIS Security Vulnerability"
- Include: Detailed description and reproduction steps

### Can I request new features?
Yes! Submit feature requests:
1. Check existing requests on GitHub
2. Create new issue with detailed description
3. Join community discussions on Discord

## 💰 Licensing Questions

### What license is LEWIS released under?
LEWIS is released under the MIT License, which allows:
- Commercial use
- Modification
- Distribution
- Private use

### Can I use LEWIS in commercial environments?
Yes, the MIT License permits commercial use. For enterprise features and support, consider our commercial licensing options.

### Can I modify LEWIS?
Yes, you can modify LEWIS under the MIT License. We encourage contributions back to the community.

### How do I contribute financially?
Support LEWIS development through:
- **Cryptocurrency**: Solana, Bitcoin
- **PayPal**: [paypal.me/yashab07](https://paypal.me/yashab07)
- **Sponsorship**: Contact yashabalam707@gmail.com

See our [Donation Guide](../DONATE.md) for details.

## 🔮 Future Questions

### What's planned for future LEWIS versions?
Upcoming features include:
- Advanced AI models (GPT-4, Claude)
- Mobile applications
- Cloud deployment options
- Additional language support
- Quantum-resistant cryptography

### How often is LEWIS updated?
- **Major releases**: Quarterly
- **Minor updates**: Monthly
- **Security patches**: As needed
- **Tool definitions**: Weekly

### Will LEWIS support other operating systems?
Currently focused on Linux, but future plans include:
- Windows Subsystem for Linux (WSL)
- macOS support (limited)
- Cloud-native deployments

---

**📝 FAQ Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)

---

**❓ Didn't find your answer?**
- 💬 Ask in [ZehraSec Discord](https://discord.gg/zehrasec)
- 📧 Email: yashabalam707@gmail.com
- 🐛 Create an issue: [GitHub Issues](https://github.com/yashab-cyber/lewis/issues)
