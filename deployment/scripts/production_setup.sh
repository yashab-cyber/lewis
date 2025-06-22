#!/bin/bash
# LEWIS Production Setup Script
# Author: Yashab Alam (ZehraSec)
# Project: LEWIS - Linux Environment Working Intelligence System

set -euo pipefail

# Configuration
LEWIS_USER="lewis"
LEWIS_HOME="/opt/lewis"
LEWIS_DATA="/var/lib/lewis"
LEWIS_LOGS="/var/log/lewis"
LEWIS_CONFIG="/etc/lewis"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1" >&2; exit 1; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root"
    fi
}

# Update system packages
update_system() {
    log "Updating system packages..."
    
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update
        apt-get upgrade -y
        apt-get install -y curl wget gnupg2 software-properties-common
    elif command -v yum >/dev/null 2>&1; then
        yum update -y
        yum install -y curl wget gnupg2
    elif command -v dnf >/dev/null 2>&1; then
        dnf update -y
        dnf install -y curl wget gnupg2
    else
        error "Unsupported package manager"
    fi
    
    success "System packages updated"
}

# Install Python 3.9+
install_python() {
    log "Installing Python 3.9+..."
    
    if command -v apt-get >/dev/null 2>&1; then
        add-apt-repository -y ppa:deadsnakes/ppa
        apt-get update
        apt-get install -y python3.9 python3.9-venv python3.9-dev python3-pip
    elif command -v yum >/dev/null 2>&1; then
        yum install -y python39 python39-pip python39-devel
    elif command -v dnf >/dev/null 2>&1; then
        dnf install -y python3.9 python3-pip python3-devel
    fi
    
    # Create symlink
    ln -sf /usr/bin/python3.9 /usr/bin/python3
    ln -sf /usr/bin/pip3 /usr/bin/pip
    
    success "Python installed"
}

# Install Node.js
install_nodejs() {
    log "Installing Node.js..."
    
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    
    if command -v apt-get >/dev/null 2>&1; then
        apt-get install -y nodejs
    elif command -v yum >/dev/null 2>&1; then
        yum install -y nodejs npm
    elif command -v dnf >/dev/null 2>&1; then
        dnf install -y nodejs npm
    fi
    
    success "Node.js installed"
}

# Install Docker
install_docker() {
    log "Installing Docker..."
    
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    
    # Install Docker Compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Start Docker service
    systemctl enable docker
    systemctl start docker
    
    success "Docker installed"
}

# Install PostgreSQL
install_postgresql() {
    log "Installing PostgreSQL..."
    
    if command -v apt-get >/dev/null 2>&1; then
        apt-get install -y postgresql postgresql-contrib
    elif command -v yum >/dev/null 2>&1; then
        yum install -y postgresql-server postgresql-contrib
        postgresql-setup initdb
    elif command -v dnf >/dev/null 2>&1; then
        dnf install -y postgresql-server postgresql-contrib
        postgresql-setup --initdb
    fi
    
    systemctl enable postgresql
    systemctl start postgresql
    
    # Create LEWIS database and user
    sudo -u postgres psql << EOF
CREATE DATABASE lewis;
CREATE USER lewis WITH ENCRYPTED PASSWORD 'lewis_secure_password_$(openssl rand -hex 8)';
GRANT ALL PRIVILEGES ON DATABASE lewis TO lewis;
\q
EOF

    success "PostgreSQL installed and configured"
}

# Install Redis
install_redis() {
    log "Installing Redis..."
    
    if command -v apt-get >/dev/null 2>&1; then
        apt-get install -y redis-server
    elif command -v yum >/dev/null 2>&1; then
        yum install -y redis
    elif command -v dnf >/dev/null 2>&1; then
        dnf install -y redis
    fi
    
    systemctl enable redis
    systemctl start redis
    
    success "Redis installed"
}

# Install Nginx
install_nginx() {
    log "Installing Nginx..."
    
    if command -v apt-get >/dev/null 2>&1; then
        apt-get install -y nginx
    elif command -v yum >/dev/null 2>&1; then
        yum install -y nginx
    elif command -v dnf >/dev/null 2>&1; then
        dnf install -y nginx
    fi
    
    systemctl enable nginx
    systemctl start nginx
    
    success "Nginx installed"
}

# Create LEWIS user and directories
setup_lewis_user() {
    log "Setting up LEWIS user and directories..."
    
    # Create user
    useradd -r -m -d $LEWIS_HOME -s /bin/bash $LEWIS_USER || true
    
    # Create directories
    mkdir -p $LEWIS_HOME $LEWIS_DATA $LEWIS_LOGS $LEWIS_CONFIG
    mkdir -p $LEWIS_DATA/{uploads,cache,backups}
    mkdir -p $LEWIS_LOGS/{access,error,debug}
    
    # Set permissions
    chown -R $LEWIS_USER:$LEWIS_USER $LEWIS_HOME $LEWIS_DATA $LEWIS_LOGS
    chmod 755 $LEWIS_HOME
    chmod 750 $LEWIS_DATA $LEWIS_LOGS
    chmod 644 $LEWIS_CONFIG
    
    success "LEWIS user and directories created"
}

# Install LEWIS application
install_lewis() {
    log "Installing LEWIS application..."
    
    # Clone repository
    if [ ! -d "$LEWIS_HOME/lewis" ]; then
        sudo -u $LEWIS_USER git clone https://github.com/ZehraSec/LEWIS.git $LEWIS_HOME/lewis
    fi
    
    cd $LEWIS_HOME/lewis
    
    # Create virtual environment
    sudo -u $LEWIS_USER python3 -m venv $LEWIS_HOME/venv
    
    # Install Python dependencies
    sudo -u $LEWIS_USER $LEWIS_HOME/venv/bin/pip install --upgrade pip
    sudo -u $LEWIS_USER $LEWIS_HOME/venv/bin/pip install -r requirements.txt
    
    # Install Node.js dependencies (if applicable)
    if [ -f "package.json" ]; then
        sudo -u $LEWIS_USER npm install
    fi
    
    success "LEWIS application installed"
}

# Configure LEWIS
configure_lewis() {
    log "Configuring LEWIS..."
    
    cat > $LEWIS_CONFIG/lewis.conf << EOF
# LEWIS Production Configuration
[server]
host = 0.0.0.0
port = 8080
workers = 4
debug = false

[database]
type = postgresql
host = localhost
port = 5432
name = lewis
user = lewis
password = lewis_secure_password

[redis]
host = localhost
port = 6379
db = 0

[security]
secret_key = $(openssl rand -hex 32)
jwt_secret = $(openssl rand -hex 32)
cors_origins = *
max_upload_size = 100MB

[logging]
level = INFO
access_log = $LEWIS_LOGS/access/access.log
error_log = $LEWIS_LOGS/error/error.log
debug_log = $LEWIS_LOGS/debug/debug.log

[paths]
data_dir = $LEWIS_DATA
upload_dir = $LEWIS_DATA/uploads
cache_dir = $LEWIS_DATA/cache
backup_dir = $LEWIS_DATA/backups
EOF

    chown $LEWIS_USER:$LEWIS_USER $LEWIS_CONFIG/lewis.conf
    chmod 600 $LEWIS_CONFIG/lewis.conf
    
    success "LEWIS configured"
}

# Create systemd service
create_systemd_service() {
    log "Creating systemd service..."
    
    cat > /etc/systemd/system/lewis.service << EOF
[Unit]
Description=LEWIS - Linux Environment Working Intelligence System
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service

[Service]
Type=exec
User=$LEWIS_USER
Group=$LEWIS_USER
WorkingDirectory=$LEWIS_HOME/lewis
Environment=PATH=$LEWIS_HOME/venv/bin
Environment=LEWIS_CONFIG=$LEWIS_CONFIG/lewis.conf
ExecStart=$LEWIS_HOME/venv/bin/python app.py
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=lewis

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$LEWIS_DATA $LEWIS_LOGS

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable lewis
    
    success "Systemd service created"
}

# Configure Nginx
configure_nginx() {
    log "Configuring Nginx..."
    
    cat > $NGINX_AVAILABLE/lewis << EOF
server {
    listen 80;
    server_name _;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name _;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/lewis.crt;
    ssl_certificate_key /etc/ssl/private/lewis.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    
    # Logging
    access_log $LEWIS_LOGS/access/nginx_access.log;
    error_log $LEWIS_LOGS/error/nginx_error.log;
    
    # File upload limit
    client_max_body_size 100M;
    
    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Static files
    location /static/ {
        alias $LEWIS_HOME/lewis/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

    # Enable site
    ln -sf $NGINX_AVAILABLE/lewis $NGINX_ENABLED/lewis
    
    # Remove default site
    rm -f $NGINX_ENABLED/default
    
    # Generate self-signed certificate
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/ssl/private/lewis.key \
        -out /etc/ssl/certs/lewis.crt \
        -subj "/C=US/ST=State/L=City/O=LEWIS/CN=lewis.local"
    
    # Test configuration
    nginx -t
    systemctl reload nginx
    
    success "Nginx configured"
}

# Setup firewall
setup_firewall() {
    log "Setting up firewall..."
    
    if command -v ufw >/dev/null 2>&1; then
        ufw --force enable
        ufw default deny incoming
        ufw default allow outgoing
        ufw allow ssh
        ufw allow 80/tcp
        ufw allow 443/tcp
        ufw status
    elif command -v firewall-cmd >/dev/null 2>&1; then
        systemctl enable firewalld
        systemctl start firewalld
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --reload
    fi
    
    success "Firewall configured"
}

# Setup monitoring
setup_monitoring() {
    log "Setting up monitoring..."
    
    # Create monitoring directories
    mkdir -p /opt/monitoring/{prometheus,grafana}
    
    # Install Prometheus
    wget https://github.com/prometheus/prometheus/releases/latest/download/prometheus-*linux-amd64.tar.gz
    tar xf prometheus-*linux-amd64.tar.gz
    mv prometheus-*linux-amd64/* /opt/monitoring/prometheus/
    
    # Create Prometheus configuration
    cat > /opt/monitoring/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'lewis'
    static_configs:
      - targets: ['localhost:8080']
        
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
EOF

    # Create Prometheus service
    cat > /etc/systemd/system/prometheus.service << EOF
[Unit]
Description=Prometheus
After=network.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecStart=/opt/monitoring/prometheus/prometheus --config.file=/opt/monitoring/prometheus/prometheus.yml --storage.tsdb.path=/opt/monitoring/prometheus/data
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    useradd -r -s /bin/false prometheus
    chown -R prometheus:prometheus /opt/monitoring/prometheus
    systemctl daemon-reload
    systemctl enable prometheus
    systemctl start prometheus
    
    success "Monitoring setup completed"
}

# Main installation function
main() {
    log "Starting LEWIS production setup..."
    
    check_root
    update_system
    install_python
    install_nodejs
    install_docker
    install_postgresql
    install_redis
    install_nginx
    setup_lewis_user
    install_lewis
    configure_lewis
    create_systemd_service
    configure_nginx
    setup_firewall
    setup_monitoring
    
    # Start services
    systemctl start lewis
    
    success "LEWIS production setup completed!"
    log "LEWIS is now available at https://$(hostname -I | awk '{print $1}')"
    log "Default credentials and configuration are in $LEWIS_CONFIG/lewis.conf"
    log "Logs are available in $LEWIS_LOGS/"
    log "To check status: systemctl status lewis"
    log "To view logs: journalctl -u lewis -f"
}

# Show help
show_help() {
    cat << EOF
LEWIS Production Setup Script

This script installs and configures LEWIS for production use.

Requirements:
- Ubuntu 20.04+ or CentOS 8+ or RHEL 8+
- Root access
- Internet connection

The script will install:
- Python 3.9+
- Node.js 18+
- PostgreSQL
- Redis
- Nginx
- Docker
- LEWIS application
- Monitoring (Prometheus)

Usage: sudo $0

For more information, visit: https://github.com/ZehraSec/LEWIS
EOF
}

# Parse arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main
        ;;
esac
