#!/bin/bash

# LEWIS - Linux Environment Working Intelligence System
# Installation Script for Linux Systems
# Created by Yashab Alam - ZehraSec
# Supports: Ubuntu/Debian, CentOS/RHEL, Arch Linux, Kali Linux, Termux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
LEWIS_USER="lewis"
LEWIS_HOME="/opt/lewis"
LEWIS_CONFIG="/etc/lewis"
LEWIS_LOGS="/var/log/lewis"
LEWIS_DATA="/var/lib/lewis"
SERVICE_NAME="lewis"
GITHUB_REPO="https://github.com/yashab-cyber/lewis.git"
ZEHRASEC_WEBSITE="https://www.zehrasec.com"
CREATOR_EMAIL="yashabalam707@gmail.com"



# System detection
detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    elif [[ -f /etc/redhat-release ]]; then
        OS="Red Hat Enterprise Linux"
        VER=$(cat /etc/redhat-release | sed 's/.*release //;s/ .*//')
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi
    
    echo -e "${BLUE}Detected OS: $OS $VER${NC}"
}

# Print banner
print_banner() {
    echo -e "${CYAN}"
    echo "██╗     ███████╗██╗    ██╗██╗███████╗"
    echo "██║     ██╔════╝██║    ██║██║██╔════╝"
    echo "██║     █████╗  ██║ █╗ ██║██║███████╗"
    echo "██║     ██╔══╝  ██║███╗██║██║╚════██║"
    echo "███████╗███████╗╚███╔███╔╝██║███████║"
    echo "╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝"
    echo -e "${NC}"
    echo -e "${BLUE}Linux Environment Working Intelligence System${NC}"
    echo -e "${GREEN}Version: 1.0.0${NC}"
    echo -e "${PURPLE}Created by Yashab Alam - ZehraSec${NC}"
    echo -e "${CYAN}Website: $ZEHRASEC_WEBSITE${NC}"
    echo ""
    echo "██║     ██╔════╝██║    ██║██║██╔════╝"
    echo "██║     █████╗  ██║ █╗ ██║██║███████╗"
    echo "██║     ██╔══╝  ██║███╗██║██║╚════██║"
    echo "███████╗███████╗╚███╔███╔╝██║███████║"
    echo "╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝"
    echo -e "${NC}"
    echo -e "${CYAN}Linux Environment Working Intelligence System${NC}"
    echo -e "${YELLOW}Installation Script v1.0${NC}"
    echo ""
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}This script must be run as root (use sudo)${NC}"
        exit 1
    fi
}

# Install system dependencies based on OS
install_system_dependencies() {
    echo -e "${YELLOW}Installing system dependencies...${NC}"
    
    case "$OS" in
        "Ubuntu"*|"Debian"*|"Kali"*)
            apt-get update
            apt-get install -y \
                python3 \
                python3-pip \
                python3-venv \
                python3-dev \
                build-essential \
                git \
                curl \
                wget \
                unzip \
                sqlite3 \
                mongodb \
                redis-server \
                nginx \
                supervisor \
                nmap \
                masscan \
                nikto \
                dirb \
                gobuster \
                sqlmap \
                metasploit-framework \
                john \
                hashcat \
                hydra \
                wireshark-common \
                tcpdump \
                net-tools \
                htop \
                vim \
                tmux \
                jq \
                libssl-dev \
                libffi-dev \
                libjpeg-dev \
                libpng-dev \
                libfreetype6-dev \
                pkg-config \
                portaudio19-dev \
                espeak \
                festival \
                alsa-utils \
                pulseaudio \
                make \
                libreadline-dev \
                zlib1g-dev \
                libbz2-dev \
                libsqlite3-dev \
                llvm \
                libncurses5-dev \
                libncursesw5-dev \
                xz-utils \
                tk-dev \
                libxml2-dev \
                libxmlsec1-dev \
                libffi-dev \
                liblzma-dev
            ;;
        "CentOS"*|"Red Hat"*|"Rocky"*|"AlmaLinux"*)
            yum update -y
            yum groupinstall -y "Development Tools"
            yum install -y \
                python3 \
                python3-pip \
                python3-devel \
                git \
                curl \
                wget \
                unzip \
                sqlite \
                mongodb-server \
                redis \
                nginx \
                supervisor \
                nmap \
                nikto \
                john \
                hydra \
                wireshark \
                tcpdump \
                net-tools \
                htop \
                vim \
                tmux \
                jq \
                openssl-devel \
                libffi-devel \
                libjpeg-devel \
                libpng-devel \
                freetype-devel \
                pkgconfig \
                portaudio-devel \
                espeak \
                festival \
                alsa-utils \
                pulseaudio \
                make \
                readline-devel \
                zlib-devel \
                bzip2-devel \
                sqlite-devel \
                llvm \
                ncurses-devel \
                xz-devel \
                tk-devel \
                libxml2-devel \
                xmlsec1-devel \
                xz-lzma-compat
            ;;
        "Arch"*|"Manjaro"*)
            pacman -Syu --noconfirm
            pacman -S --noconfirm \
                python \
                python-pip \
                python-virtualenv \
                base-devel \
                git \
                curl \
                wget \
                unzip \
                sqlite \
                mongodb \
                redis \
                nginx \
                supervisor \
                nmap \
                masscan \
                nikto \
                dirb \
                gobuster \
                sqlmap \
                metasploit \
                john \
                hashcat \
                hydra \
                wireshark-cli \
                tcpdump \
                net-tools \
                htop \
                vim \
                tmux \
                jq \
                openssl \
                libffi \
                libjpeg-turbo \
                libpng \
                freetype2 \
                pkgconf \
                portaudio \
                espeak \
                festival \
                alsa-utils \
                pulseaudio \
                make \
                readline \
                zlib \
                bzip2 \
                sqlite \
                llvm \
                ncurses \
                xz \
                tk \
                libxml2 \
                xmlsec
            ;;
        *)
            echo -e "${RED}Unsupported OS: $OS${NC}"
            echo "Please install dependencies manually and run setup.py"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}System dependencies installed successfully${NC}"
}



# Create system user for LEWIS
create_lewis_user() {
    echo -e "${YELLOW}Creating LEWIS system user...${NC}"
    
    if ! id "$LEWIS_USER" &>/dev/null; then
        useradd -r -s /bin/bash -d "$LEWIS_HOME" -m "$LEWIS_USER"
        echo -e "${GREEN}User $LEWIS_USER created${NC}"
    else
        echo -e "${BLUE}User $LEWIS_USER already exists${NC}"
    fi
}

# Create directory structure
create_directories() {
    echo -e "${YELLOW}Creating directory structure...${NC}"
    
    mkdir -p "$LEWIS_HOME"
    mkdir -p "$LEWIS_CONFIG"
    mkdir -p "$LEWIS_LOGS"
    mkdir -p "$LEWIS_DATA"
    mkdir -p "$LEWIS_DATA/database"
    mkdir -p "$LEWIS_DATA/uploads"
    mkdir -p "$LEWIS_DATA/reports"
    mkdir -p "$LEWIS_DATA/backups"
    
    # Set ownership
    chown -R "$LEWIS_USER:$LEWIS_USER" "$LEWIS_HOME"
    chown -R "$LEWIS_USER:$LEWIS_USER" "$LEWIS_LOGS"
    chown -R "$LEWIS_USER:$LEWIS_USER" "$LEWIS_DATA"
    
    # Set permissions
    chmod 755 "$LEWIS_HOME"
    chmod 750 "$LEWIS_CONFIG"
    chmod 755 "$LEWIS_LOGS"
    chmod 750 "$LEWIS_DATA"
    
    echo -e "${GREEN}Directory structure created${NC}"
}

# Clone or copy LEWIS source code
install_lewis_source() {
    echo -e "${YELLOW}Installing LEWIS source code...${NC}"
    
    if [[ -d "$(pwd)/lewis.py" ]]; then
        # Running from source directory
        echo "Copying source files..."
        cp -r "$(pwd)"/* "$LEWIS_HOME/"
    else
        # Clone from repository
        echo "Cloning from repository..."
        git clone "$GITHUB_REPO" "$LEWIS_HOME"
    fi
    
    chown -R "$LEWIS_USER:$LEWIS_USER" "$LEWIS_HOME"
    echo -e "${GREEN}LEWIS source code installed${NC}"
}

# Create Python virtual environment and install dependencies
setup_python_environment() {
    echo -e "${YELLOW}Setting up Python environment with pyenv Python $PYTHON_VERSION...${NC}"
    
    # Ensure pyenv is available
    export PYENV_ROOT="$PYENV_ROOT"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    
    # Verify Python installation
    if [[ ! -x "$LEWIS_PYTHON_PATH" ]]; then
        echo -e "${RED}Python $PYTHON_VERSION not found at $LEWIS_PYTHON_PATH${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Using Python: $LEWIS_PYTHON_PATH${NC}"
    "$LEWIS_PYTHON_PATH" --version
    
    # Create virtual environment using pyenv Python
    echo -e "${BLUE}Creating virtual environment...${NC}"
    sudo -u "$LEWIS_USER" "$LEWIS_PYTHON_PATH" -m venv "$LEWIS_HOME/venv"
    
    # Verify virtual environment
    if [[ ! -f "$LEWIS_HOME/venv/bin/python" ]]; then
        echo -e "${RED}Failed to create virtual environment${NC}"
        exit 1
    fi
    
    # Upgrade pip and install dependencies
    echo -e "${BLUE}Installing Python dependencies...${NC}"
    sudo -u "$LEWIS_USER" bash -c "
        source '$LEWIS_HOME/venv/bin/activate'
        python --version
        pip --version
        
        echo 'Upgrading pip and setuptools...'
        pip install --upgrade pip setuptools wheel
        
        echo 'Installing LEWIS dependencies...'
        pip install -r '$LEWIS_HOME/requirements.txt'
        
        echo 'Verifying critical dependencies...'
        python -c 'import torch; print(f\"PyTorch version: {torch.__version__}\")'
        python -c 'import transformers; print(f\"Transformers version: {transformers.__version__}\")'
        python -c 'import flask; print(f\"Flask version: {flask.__version__}\")'
        python -c 'import numpy; print(f\"NumPy version: {numpy.__version__}\")'
    "
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}Python environment configured successfully${NC}"
    else
        echo -e "${RED}Failed to install Python dependencies${NC}"
        echo -e "${YELLOW}Trying with alternative approach...${NC}"
        
        # Try installing with no-cache and individual packages
        sudo -u "$LEWIS_USER" bash -c "
            source '$LEWIS_HOME/venv/bin/activate'
            pip install --no-cache-dir --upgrade pip setuptools wheel
            
            # Install core dependencies first
            pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
            pip install --no-cache-dir transformers sentence-transformers
            pip install --no-cache-dir flask flask-cors flask-socketio
            pip install --no-cache-dir fastapi uvicorn
            pip install --no-cache-dir numpy pandas scikit-learn
            
            # Install remaining dependencies
            if [[ -f '$LEWIS_HOME/requirements-python311.txt' ]]; then
                pip install --no-cache-dir -r '$LEWIS_HOME/requirements-python311.txt' || true
            else
                pip install --no-cache-dir -r '$LEWIS_HOME/requirements.txt' || true
            fi
        "
    fi
    
    # Create Python activation script for LEWIS user
    cat > "$LEWIS_HOME/activate_lewis_python.sh" << EOF
#!/bin/bash
# LEWIS Python Environment Activation Script

# Set up pyenv
export PYENV_ROOT="$PYENV_ROOT"
export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init -)"

# Set Python version
cd "$LEWIS_HOME"
pyenv local "$PYTHON_VERSION"

# Activate virtual environment
source "$LEWIS_HOME/venv/bin/activate"

# Show Python info
echo "LEWIS Python Environment Activated"
echo "Python version: \$(python --version)"
echo "Python path: \$(which python)"
echo "Virtual environment: $LEWIS_HOME/venv"
EOF

    chmod +x "$LEWIS_HOME/activate_lewis_python.sh"
    chown "$LEWIS_USER:$LEWIS_USER" "$LEWIS_HOME/activate_lewis_python.sh"
    
    echo -e "${GREEN}Python environment setup completed${NC}"
}

# Configure databases
setup_databases() {
    echo -e "${YELLOW}Configuring databases...${NC}"
    
    # MongoDB setup
    if command -v mongod &> /dev/null; then
        systemctl enable mongod
        systemctl start mongod
        
        # Create LEWIS database and user
        mongo --eval "
            use lewis;
            db.createUser({
                user: 'lewis',
                pwd: 'lewis_secure_password',
                roles: [{role: 'readWrite', db: 'lewis'}]
            });
        " || true
    fi
    
    # Redis setup
    if command -v redis-server &> /dev/null; then
        systemctl enable redis
        systemctl start redis
    fi
    
    # SQLite setup (backup database)
    sudo -u "$LEWIS_USER" sqlite3 "$LEWIS_DATA/database/lewis.db" "
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        INSERT OR REPLACE INTO system_info (key, value) VALUES ('version', '1.0.0');
        INSERT OR REPLACE INTO system_info (key, value) VALUES ('installed_at', datetime('now'));
    "
    
    echo -e "${GREEN}Databases configured${NC}"
}

# Create configuration files
create_configuration() {
    echo -e "${YELLOW}Creating configuration files...${NC}"
    
    # Main configuration file
    cat > "$LEWIS_CONFIG/config.yaml" << 'EOF'
# LEWIS Configuration File
version: "1.0.0"
environment: "production"

# Server Configuration
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  debug: false

# Database Configuration
database:
  mongodb:
    host: "localhost"
    port: 27017
    database: "lewis"
    username: "lewis"
    password: "lewis_secure_password"
  
  redis:
    host: "localhost"
    port: 6379
    database: 0
  
  sqlite:
    path: "/var/lib/lewis/database/lewis.db"

# AI Configuration
ai:
  model_name: "microsoft/DialoGPT-medium"
  temperature: 0.7
  max_tokens: 512
  cache_models: true

# Security Configuration
security:
  jwt_secret: "change_this_secret_key_in_production"
  session_timeout: 3600
  max_failed_attempts: 5
  rate_limit: 100
  api_key_required: true

# Logging Configuration
logging:
  level: "INFO"
  file: "/var/log/lewis/lewis.log"
  max_size: "100MB"
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Tools Configuration
tools:
  nmap_path: "/usr/bin/nmap"
  nikto_path: "/usr/bin/nikto"
  sqlmap_path: "/usr/bin/sqlmap"
  gobuster_path: "/usr/bin/gobuster"
  output_dir: "/var/lib/lewis/outputs"
  timeout: 300

# Voice Configuration
voice:
  enabled: false
  wake_word: "lewis"
  language: "en-US"
  speech_recognition: "google"
  text_to_speech: "espeak"

# Analytics Configuration
analytics:
  enabled: true
  update_interval: 60
  retention_days: 30
  dashboard_refresh: 30

# Notifications Configuration
notifications:
  email:
    enabled: false
    smtp_server: "localhost"
    smtp_port: 587
    username: ""
    password: ""
  
  slack:
    enabled: false
    webhook_url: ""
  
  discord:
    enabled: false
    webhook_url: ""

# Report Configuration
reports:
  output_dir: "/var/lib/lewis/reports"
  formats: ["pdf", "html", "json"]
  auto_cleanup: true
  cleanup_days: 90

# Detection Configuration
detection:
  enabled: true
  real_time: true
  threat_intel: true
  custom_rules: "/etc/lewis/detection_rules.yaml"
EOF

    # Detection rules file
    cat > "$LEWIS_CONFIG/detection_rules.yaml" << 'EOF'
# LEWIS Threat Detection Rules
rules:
  - name: "Brute Force Detection"
    type: "authentication"
    threshold: 5
    timeframe: 300
    action: "alert"
  
  - name: "SQL Injection Pattern"
    type: "web_attack"
    pattern: "(?i)(union|select|insert|delete|update).*(\s|%20)"
    action: "block"
  
  - name: "Suspicious Network Scan"
    type: "network"
    threshold: 100
    timeframe: 60
    action: "alert"
  
  - name: "Malware Communication"
    type: "malware"
    pattern: "(?i)(download|upload).*\.(exe|bat|ps1|sh)"
    action: "quarantine"
EOF

    # Systemd service file
    cat > "/etc/systemd/system/$SERVICE_NAME.service" << EOF
[Unit]
Description=LEWIS - Linux Environment Working Intelligence System
After=network.target mongodb.service redis.service
Wants=mongodb.service redis.service

[Service]
Type=simple
User=$LEWIS_USER
Group=$LEWIS_USER
WorkingDirectory=$LEWIS_HOME
Environment=PYENV_ROOT=$PYENV_ROOT
Environment=PATH=$PYENV_ROOT/bin:$LEWIS_HOME/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStartPre=/bin/bash -c 'cd $LEWIS_HOME && export PYENV_ROOT=$PYENV_ROOT && export PATH=$PYENV_ROOT/bin:\$PATH && eval "\$(pyenv init -)" && pyenv local $PYTHON_VERSION'
ExecStart=/bin/bash -c 'source $LEWIS_HOME/activate_lewis_python.sh && python lewis.py --mode server --config /etc/lewis/config.yaml'
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=lewis

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=$LEWIS_DATA $LEWIS_LOGS
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOF

    # Nginx configuration (if needed)
    if command -v nginx &> /dev/null; then
        cat > "/etc/nginx/sites-available/lewis" << 'EOF'
server {
    listen 80;
    server_name lewis.local;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /static/ {
        alias /opt/lewis/interfaces/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
        
        ln -sf /etc/nginx/sites-available/lewis /etc/nginx/sites-enabled/
        nginx -t && systemctl reload nginx
    fi
    
    # Set proper permissions
    chown root:root "$LEWIS_CONFIG/config.yaml"
    chmod 640 "$LEWIS_CONFIG/config.yaml"
    chown root:root "$LEWIS_CONFIG/detection_rules.yaml"
    chmod 640 "$LEWIS_CONFIG/detection_rules.yaml"
    
    echo -e "${GREEN}Configuration files created${NC}"
}

# Create startup scripts
create_startup_scripts() {
    echo -e "${YELLOW}Creating startup scripts...${NC}"
    
    # Main startup script
    cat > "$LEWIS_HOME/start_lewis.sh" << EOF
#!/bin/bash
# LEWIS Startup Script with pyenv Python $PYTHON_VERSION

LEWIS_HOME="$LEWIS_HOME"
LEWIS_USER="$LEWIS_USER"
CONFIG_FILE="/etc/lewis/config.yaml"
PYENV_ROOT="$PYENV_ROOT"
PYTHON_VERSION="$PYTHON_VERSION"

# Check if running as LEWIS user
if [[ \$(whoami) != "$LEWIS_USER" ]]; then
    echo "Switching to $LEWIS_USER user..."
    sudo -u "$LEWIS_USER" "\$0" "\$@"
    exit \$?
fi

# Set up pyenv environment
export PYENV_ROOT="\$PYENV_ROOT"
export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init -)"

# Change to LEWIS directory and set Python version
cd "\$LEWIS_HOME"
pyenv local "\$PYTHON_VERSION"

# Activate virtual environment
source "\$LEWIS_HOME/venv/bin/activate"

# Verify Python version
echo "Using Python: \$(python --version)"
echo "Python path: \$(which python)"

# Start LEWIS
python lewis.py --config "\$CONFIG_FILE" "\$@"
EOF

    # CLI launcher
    cat > "$LEWIS_HOME/lewis-cli" << EOF
#!/bin/bash
# LEWIS CLI Launcher
exec "$LEWIS_HOME/start_lewis.sh" --mode cli "\$@"
EOF

    # GUI launcher
    cat > "$LEWIS_HOME/lewis-gui" << EOF
#!/bin/bash
# LEWIS GUI Launcher
exec "$LEWIS_HOME/start_lewis.sh" --mode gui "\$@"
EOF

    # Make scripts executable
    chmod +x "$LEWIS_HOME/start_lewis.sh"
    chmod +x "$LEWIS_HOME/lewis-cli"
    chmod +x "$LEWIS_HOME/lewis-gui"
    chown "$LEWIS_USER:$LEWIS_USER" "$LEWIS_HOME/start_lewis.sh"
    chown "$LEWIS_USER:$LEWIS_USER" "$LEWIS_HOME/lewis-cli"
    chown "$LEWIS_USER:$LEWIS_USER" "$LEWIS_HOME/lewis-gui"
    
    # Create symlinks in /usr/local/bin
    ln -sf "$LEWIS_HOME/lewis-cli" "/usr/local/bin/lewis"
    ln -sf "$LEWIS_HOME/lewis-cli" "/usr/local/bin/lewis-cli"
    ln -sf "$LEWIS_HOME/lewis-gui" "/usr/local/bin/lewis-gui"
    
    echo -e "${GREEN}Startup scripts created${NC}"
}

# Setup log rotation
setup_log_rotation() {
    echo -e "${YELLOW}Setting up log rotation...${NC}"
    
    cat > "/etc/logrotate.d/lewis" << EOF
$LEWIS_LOGS/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $LEWIS_USER $LEWIS_USER
    postrotate
        systemctl reload lewis >/dev/null 2>&1 || true
    endscript
}
EOF

    echo -e "${GREEN}Log rotation configured${NC}"
}

# Setup firewall rules
setup_firewall() {
    echo -e "${YELLOW}Configuring firewall...${NC}"
    
    if command -v ufw &> /dev/null; then
        # Ubuntu/Debian UFW
        ufw allow 8000/tcp comment "LEWIS Web Interface"
        ufw allow 22/tcp comment "SSH"
        echo -e "${GREEN}UFW firewall rules added${NC}"
    elif command -v firewall-cmd &> /dev/null; then
        # CentOS/RHEL firewalld
        firewall-cmd --permanent --add-port=8000/tcp
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --reload
        echo -e "${GREEN}Firewalld rules added${NC}"
    elif command -v iptables &> /dev/null; then
        # Generic iptables
        iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
        iptables -A INPUT -p tcp --dport 22 -j ACCEPT
        
        # Save rules (varies by distribution)
        if command -v iptables-save &> /dev/null; then
            iptables-save > /etc/iptables/rules.v4 2>/dev/null || \
            iptables-save > /etc/sysconfig/iptables 2>/dev/null || true
        fi
        echo -e "${GREEN}Iptables rules added${NC}"
    else
        echo -e "${YELLOW}No supported firewall found, please configure manually${NC}"
    fi
}

# Setup extension system
setup_extension_system() {
    echo -e "${YELLOW}Setting up extension system...${NC}"
    
    # Install Flask and extension dependencies
    echo -e "${BLUE}Installing extension dependencies...${NC}"
    pip3 install flask flask-socketio
    
    # Create extension directories
    mkdir -p "$LEWIS_DATA/extensions"
    mkdir -p "$LEWIS_LOGS/extensions" 
    mkdir -p "$LEWIS_CONFIG/extensions"
    
    # Set proper permissions for examples directory
    if [ -d "$LEWIS_HOME/examples" ]; then
        echo -e "${GREEN}✅ Examples directory found${NC}"
        chown -R $LEWIS_USER:$LEWIS_USER "$LEWIS_HOME/examples"
        chmod -R 755 "$LEWIS_HOME/examples"
        
        # Check example extensions
        for ext in "network_security_extension" "custom_interface_extension"; do
            if [ -f "$LEWIS_HOME/examples/$ext/extension.py" ]; then
                echo -e "${GREEN}✅ $ext found${NC}"
            else
                echo -e "${RED}❌ $ext missing${NC}"
            fi
        done
    else
        echo -e "${RED}❌ Examples directory not found${NC}"
        return 1
    fi
    
    # Test extension system
    echo -e "${BLUE}Testing extension system...${NC}"
    cd "$LEWIS_HOME"
    if python3 -c "from core.extension_manager import ExtensionManager; em = ExtensionManager(); em.discover_extensions(); print(f'Found {len(em.available_extensions)} extensions')" 2>/dev/null; then
        echo -e "${GREEN}✅ Extension system working${NC}"
    else
        echo -e "${YELLOW}⚠️ Extension system test failed (may work after full installation)${NC}"
    fi
    
    echo -e "${GREEN}Extension system setup complete${NC}"
}

# Finalize installation
finalize_installation() {
    echo -e "${YELLOW}Finalizing installation...${NC}"
    
    # Enable and start services
    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    
    # Start required services
    systemctl start mongodb 2>/dev/null || true
    systemctl start redis 2>/dev/null || true
    
    # Test installation
    echo -e "${BLUE}Testing installation with pyenv Python $PYTHON_VERSION...${NC}"
    sudo -u "$LEWIS_USER" bash -c "
        source '$LEWIS_HOME/activate_lewis_python.sh'
        cd '$LEWIS_HOME'
        python --version
        python -c 'import sys; print(f\"Python executable: {sys.executable}\")'
        python -c 'import lewis; print(\"LEWIS modules imported successfully\")'
    "
    
    echo -e "${GREEN}Installation completed successfully!${NC}"
}

# Print post-installation information
print_post_install_info() {
    echo ""
    echo -e "${CYAN}=========================${NC}"
    echo -e "${CYAN}  INSTALLATION COMPLETE  ${NC}"
    echo -e "${CYAN}=========================${NC}"
    echo ""
    echo -e "${GREEN}LEWIS has been successfully installed!${NC}"
    echo ""
    echo -e "${YELLOW}Installation Details:${NC}"
    echo "• Installation Directory: $LEWIS_HOME"
    echo "• Configuration: $LEWIS_CONFIG"
    echo "• Logs: $LEWIS_LOGS"
    echo "• Data: $LEWIS_DATA"
    echo "• Service User: $LEWIS_USER"
    echo "• Python Version: $PYTHON_VERSION (via pyenv)"
    echo "• Python Path: $LEWIS_PYTHON_PATH"
    echo "• pyenv Root: $PYENV_ROOT"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "• Start LEWIS service: sudo systemctl start lewis"
    echo "• Stop LEWIS service: sudo systemctl stop lewis"
    echo "• Check status: sudo systemctl status lewis"
    echo "• View logs: sudo journalctl -u lewis -f"
    echo ""
    echo -e "${YELLOW}Command Line Access:${NC}"
    echo "• CLI Mode: lewis"
    echo "• GUI Mode: lewis-gui"
    echo "• Direct access: $LEWIS_HOME/start_lewis.sh"
    echo "• Python environment: source $LEWIS_HOME/activate_lewis_python.sh"
    echo ""
    echo -e "${YELLOW}Web Interface:${NC}"
    echo "• URL: http://$(hostname -I | awk '{print $1}'):8000"
    echo "• Local: http://localhost:8000"
    echo ""
    echo -e "${YELLOW}Configuration:${NC}"
    echo "• Main config: $LEWIS_CONFIG/config.yaml"
    echo "• Detection rules: $LEWIS_CONFIG/detection_rules.yaml"
    echo ""
    echo -e "${RED}Security Notice:${NC}"
    echo "• Change default passwords in $LEWIS_CONFIG/config.yaml"
    echo "• Review firewall settings"
    echo "• Configure SSL/TLS for production use"
    echo ""
    echo -e "${BLUE}For support: https://github.com/yashab-cyber/lewis/issues${NC}"
    echo ""
}

# Cleanup function
cleanup() {
    echo -e "${RED}Installation interrupted${NC}"
    exit 1
}

# Main installation function
main() {
    trap cleanup INT TERM
    
    print_banner
    
    echo -e "${BLUE}Starting LEWIS installation...${NC}"
    echo ""
    
    # Pre-installation checks
    check_root
    detect_os
    
    # Installation steps
    install_system_dependencies
    create_lewis_user
    create_directories
    install_lewis_source
    setup_python_environment
    setup_databases
    create_configuration
    create_startup_scripts
    setup_log_rotation
    setup_firewall
    setup_extension_system
    finalize_installation
    
    print_post_install_info
    
    echo -e "${GREEN}🎉 LEWIS installation completed successfully!${NC}"
    echo -e "${YELLOW}You can now start LEWIS with: sudo systemctl start lewis${NC}"
}

# Run main function
main "$@"
