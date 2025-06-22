# LEWIS Installation Guide

This comprehensive guide covers all installation methods and platforms supported by LEWIS.

## 📋 Prerequisites

### System Requirements

#### Minimum Requirements
- **Operating System**: Linux-based (Ubuntu 18.04+, Debian 10+, CentOS 7+, Kali Linux)
- **Python**: Version 3.8 or higher
- **Memory**: 4GB RAM
- **Storage**: 10GB free disk space
- **Network**: Internet connection for downloads and updates

#### Recommended Requirements
- **Operating System**: Ubuntu 20.04 LTS or Kali Linux 2023.1+
- **Python**: Version 3.9 or higher
- **Memory**: 8GB RAM or more
- **Storage**: 20GB free disk space
- **GPU**: NVIDIA GPU with CUDA support (optional, for AI acceleration)
- **Network**: Stable broadband connection

### Software Dependencies

#### Essential Packages
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git curl wget

# CentOS/RHEL
sudo yum install -y python3 python3-pip git curl wget
# or for newer versions
sudo dnf install -y python3 python3-pip git curl wget

# Arch Linux
sudo pacman -S python python-pip git curl wget
```

#### Optional Packages (Recommended)
```bash
# For enhanced functionality
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y mongodb postgresql redis-server
sudo apt install -y nmap masscan zmap nikto sqlmap
```

## 🚀 Installation Methods

### Method 1: Automated Installation (Recommended)

The easiest way to install LEWIS is using our automated installation script:

```bash
# Download and run installation script
curl -fsSL https://raw.githubusercontent.com/yashab-cyber/lewis/main/install.sh | sudo bash
```

**What the script does:**
- Detects your Linux distribution
- Installs required system dependencies
- Downloads and installs LEWIS
- Configures system services
- Sets up initial configuration
- Creates necessary user accounts

### Method 2: Manual Installation

#### Step 1: Clone Repository
```bash
# Clone the official repository
git clone https://github.com/yashab-cyber/lewis.git
cd lewis
```

#### Step 2: Create Virtual Environment
```bash
# Create isolated Python environment
python3 -m venv lewis-env
source lewis-env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

#### Step 3: Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

#### Step 4: Install LEWIS
```bash
# Install LEWIS package
python setup.py install

# Or install in development mode
pip install -e .
```

#### Step 5: Initial Configuration
```bash
# Initialize LEWIS configuration
lewis --init

# Configure basic settings
lewis config --setup
```

### Method 3: Docker Installation

#### Prerequisites
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Run LEWIS in Docker
```bash
# Pull official image
docker pull yashab/lewis:latest

# Run LEWIS container
docker run -it --rm \
  --name lewis \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  yashab/lewis:latest
```

#### Docker Compose (Recommended for Production)
```yaml
# docker-compose.yml
version: '3.8'
services:
  lewis:
    image: yashab/lewis:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    environment:
      - LEWIS_MODE=server
      - LEWIS_DEBUG=false
    depends_on:
      - mongodb
      - redis

  mongodb:
    image: mongo:latest
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=lewis
      - MONGO_INITDB_ROOT_PASSWORD=secure_password

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  mongodb_data:
  redis_data:
```

```bash
# Start services
docker-compose up -d
```

### Method 4: Package Manager Installation

#### Ubuntu/Debian (APT)
```bash
# Add LEWIS repository
curl -fsSL https://packages.lewis-security.com/gpg | sudo apt-key add -
echo "deb https://packages.lewis-security.com/apt stable main" | sudo tee /etc/apt/sources.list.d/lewis.list

# Install LEWIS
sudo apt update
sudo apt install lewis
```

#### CentOS/RHEL (YUM/DNF)
```bash
# Add LEWIS repository
sudo yum-config-manager --add-repo https://packages.lewis-security.com/yum/lewis.repo

# Install LEWIS
sudo yum install lewis
```

#### Arch Linux (AUR)
```bash
# Install using yay
yay -S lewis-git

# Or using makepkg
git clone https://aur.archlinux.org/lewis-git.git
cd lewis-git
makepkg -si
```

## ⚙️ Post-Installation Configuration

### 1. System Configuration

#### Create LEWIS User (Production)
```bash
# Create dedicated user
sudo useradd -r -s /bin/false lewis
sudo mkdir -p /opt/lewis /etc/lewis /var/log/lewis /var/lib/lewis
sudo chown -R lewis:lewis /opt/lewis /var/log/lewis /var/lib/lewis
sudo chmod 750 /opt/lewis /etc/lewis
```

#### Configure Systemd Service
```bash
# Enable and start LEWIS service
sudo systemctl enable lewis
sudo systemctl start lewis
sudo systemctl status lewis
```

### 2. Database Setup

#### MongoDB Configuration
```bash
# Install MongoDB
curl -fsSL https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl enable mongod
sudo systemctl start mongod

# Create LEWIS database user
mongo --eval "
db.getSiblingDB('admin').createUser({
  user: 'lewis',
  pwd: 'secure_password',
  roles: [{role: 'readWrite', db: 'lewis'}]
})
"
```

#### PostgreSQL Configuration (Alternative)
```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Create database and user
sudo -u postgres createdb lewis
sudo -u postgres createuser --superuser lewis
sudo -u postgres psql -c "ALTER USER lewis PASSWORD 'secure_password';"
```

### 3. Network Configuration

#### Firewall Setup
```bash
# UFW (Ubuntu)
sudo ufw allow 8000/tcp
sudo ufw allow from 192.168.1.0/24 to any port 8000

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-rich-rule="rule family='ipv4' source address='192.168.1.0/24' port protocol='tcp' port='8000' accept"
sudo firewall-cmd --reload

# IPTables
sudo iptables -A INPUT -p tcp --dport 8000 -s 192.168.1.0/24 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

#### SSL/TLS Certificate
```bash
# Generate self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/lewis/ssl/lewis.key \
  -out /etc/lewis/ssl/lewis.crt

# Or use Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d lewis.yourcompany.com
```

## 🔍 Verification

### Installation Verification
```bash
# Check LEWIS installation
lewis --version
lewis --health-check

# Verify all components
lewis diagnostics --full

# Check service status
sudo systemctl status lewis
```

### Functional Testing
```bash
# Test CLI interface
lewis --mode cli --test

# Test web interface
curl -k https://localhost:8000/api/v1/health

# Test database connection
lewis config test-database

# Test tool integration
lewis tools --list --verify
```

## 🚨 Troubleshooting Installation

### Common Issues

#### Permission Denied Errors
```bash
# Fix ownership issues
sudo chown -R $USER:$USER ~/.lewis
sudo chmod -R 755 ~/.lewis

# Fix Python path issues
export PYTHONPATH="${PYTHONPATH}:/opt/lewis"
echo 'export PYTHONPATH="${PYTHONPATH}:/opt/lewis"' >> ~/.bashrc
```

#### Missing Dependencies
```bash
# Install missing Python packages
pip install --upgrade -r requirements.txt

# Install missing system packages
sudo apt install -y $(lewis dependencies --missing)
```

#### Database Connection Issues
```bash
# Check database status
sudo systemctl status mongod
sudo systemctl status postgresql

# Test database connection
telnet localhost 27017  # MongoDB
telnet localhost 5432   # PostgreSQL

# Check database logs
sudo tail -f /var/log/mongodb/mongod.log
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### Network Configuration Issues
```bash
# Check port availability
sudo netstat -tulpn | grep :8000
sudo ss -tulpn | grep :8000

# Test firewall rules
sudo ufw status verbose
sudo iptables -L -n -v

# Check DNS resolution
nslookup lewis.yourcompany.com
dig lewis.yourcompany.com
```

### Getting Help

If you encounter issues not covered here:

1. **Check Logs**: `sudo journalctl -u lewis -f`
2. **Enable Debug Mode**: `lewis --debug`
3. **Run Diagnostics**: `lewis diagnostics --verbose`
4. **Search Issues**: [GitHub Issues](https://github.com/yashab-cyber/lewis/issues)
5. **Ask Community**: [ZehraSec Discord](https://discord.gg/zehrasec)
6. **Contact Support**: yashabalam707@gmail.com

## 📚 Next Steps

After successful installation:

1. **[Getting Started](02-getting-started.md)** - Learn basic LEWIS usage
2. **[Configuration](04-configuration.md)** - Customize LEWIS settings
3. **[Security](08-security.md)** - Secure your LEWIS installation
4. **[User Guide](03-user-guide.md)** - Comprehensive usage guide

---

**📝 Installation Guide Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)
