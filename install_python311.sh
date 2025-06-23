#!/bin/bash

# LEWIS pyenv Python 3.11.9 Installation Script
# Use this script if you need to manually install Python 3.11.9 via pyenv

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.11.9"
PYENV_ROOT="/opt/pyenv"
LEWIS_HOME="/opt/lewis"

echo -e "${BLUE}LEWIS Python 3.11.9 Installation via pyenv${NC}"
echo "=============================================="

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}This script must be run as root (use sudo)${NC}"
    exit 1
fi

# Install pyenv dependencies based on OS
install_pyenv_dependencies() {
    echo -e "${YELLOW}Installing pyenv dependencies...${NC}"
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        apt-get update
        apt-get install -y \
            make \
            build-essential \
            libssl-dev \
            zlib1g-dev \
            libbz2-dev \
            libreadline-dev \
            libsqlite3-dev \
            wget \
            curl \
            llvm \
            libncurses5-dev \
            libncursesw5-dev \
            xz-utils \
            tk-dev \
            libffi-dev \
            liblzma-dev \
            python3-openssl \
            git
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        yum groupinstall -y "Development Tools"
        yum install -y \
            make \
            gcc \
            openssl-devel \
            zlib-devel \
            bzip2-devel \
            readline-devel \
            sqlite-devel \
            wget \
            curl \
            llvm \
            ncurses-devel \
            xz-devel \
            tk-devel \
            libffi-devel \
            git
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        pacman -S --noconfirm \
            base-devel \
            openssl \
            zlib \
            bzip2 \
            readline \
            sqlite \
            curl \
            llvm \
            ncurses \
            xz \
            tk \
            libffi \
            git
    else
        echo -e "${RED}Unsupported package manager. Install dependencies manually.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Dependencies installed successfully${NC}"
}

# Install pyenv
install_pyenv() {
    echo -e "${YELLOW}Installing pyenv...${NC}"
    
    if [[ -d "$PYENV_ROOT" ]]; then
        echo -e "${BLUE}pyenv already exists at $PYENV_ROOT${NC}"
        cd "$PYENV_ROOT"
        git pull origin master
    else
        git clone https://github.com/pyenv/pyenv.git "$PYENV_ROOT"
    fi
    
    # Set up environment
    export PYENV_ROOT="$PYENV_ROOT"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    
    echo -e "${GREEN}pyenv installed successfully${NC}"
}

# Install Python 3.11.9
install_python() {
    echo -e "${YELLOW}Installing Python $PYTHON_VERSION...${NC}"
    
    # Check if already installed
    if [[ -d "$PYENV_ROOT/versions/$PYTHON_VERSION" ]]; then
        echo -e "${BLUE}Python $PYTHON_VERSION already installed${NC}"
        return 0
    fi
    
    # Install Python with optimized configuration
    echo -e "${BLUE}Building Python $PYTHON_VERSION (this may take 10-15 minutes)...${NC}"
    
    # Configure build options for better compatibility
    export PYTHON_CONFIGURE_OPTS="--enable-shared --enable-optimizations"
    export CFLAGS="-O2"
    export LDFLAGS="-Wl,-rpath,$PYENV_ROOT/versions/$PYTHON_VERSION/lib"
    
    if ! pyenv install "$PYTHON_VERSION"; then
        echo -e "${YELLOW}Build with optimizations failed, trying standard build...${NC}"
        unset PYTHON_CONFIGURE_OPTS CFLAGS LDFLAGS
        pyenv install "$PYTHON_VERSION"
    fi
    
    # Verify installation
    if [[ -x "$PYENV_ROOT/versions/$PYTHON_VERSION/bin/python" ]]; then
        echo -e "${GREEN}Python $PYTHON_VERSION installed successfully${NC}"
        "$PYENV_ROOT/versions/$PYTHON_VERSION/bin/python" --version
    else
        echo -e "${RED}Python installation failed${NC}"
        exit 1
    fi
}

# Set up global configuration
setup_global_config() {
    echo -e "${YELLOW}Setting up global pyenv configuration...${NC}"
    
    # Create profile script
    cat > "/etc/profile.d/pyenv.sh" << 'EOF'
# pyenv initialization
export PYENV_ROOT="/opt/pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
EOF
    
    chmod +x "/etc/profile.d/pyenv.sh"
    
    # Set ownership
    chown -R root:root "$PYENV_ROOT"
    chmod -R 755 "$PYENV_ROOT"
    
    echo -e "${GREEN}Global configuration completed${NC}"
}

# Test installation
test_installation() {
    echo -e "${YELLOW}Testing Python installation...${NC}"
    
    export PYENV_ROOT="$PYENV_ROOT"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    
    # Test Python
    python_path="$PYENV_ROOT/versions/$PYTHON_VERSION/bin/python"
    
    if [[ -x "$python_path" ]]; then
        echo -e "${BLUE}Testing Python executable...${NC}"
        "$python_path" --version
        "$python_path" -c "import sys; print(f'Python path: {sys.executable}')"
        "$python_path" -c "import ssl; print('SSL support: OK')"
        "$python_path" -c "import sqlite3; print('SQLite support: OK')"
        
        echo -e "${GREEN}Python $PYTHON_VERSION is working correctly!${NC}"
    else
        echo -e "${RED}Python executable not found${NC}"
        exit 1
    fi
}

# Create LEWIS-specific setup
setup_lewis_python() {
    echo -e "${YELLOW}Setting up Python for LEWIS...${NC}"
    
    # Create LEWIS directory if it doesn't exist
    mkdir -p "$LEWIS_HOME"
    
    # Set local Python version for LEWIS
    cd "$LEWIS_HOME"
    pyenv local "$PYTHON_VERSION"
    
    # Create activation script
    cat > "$LEWIS_HOME/activate_python.sh" << EOF
#!/bin/bash
# LEWIS Python Activation Script

export PYENV_ROOT="$PYENV_ROOT"
export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init -)"
cd "$LEWIS_HOME"
pyenv local "$PYTHON_VERSION"

echo "LEWIS Python Environment Activated"
echo "Python version: \$(python --version)"
echo "Python path: \$(which python)"
EOF
    
    chmod +x "$LEWIS_HOME/activate_python.sh"
    
    echo -e "${GREEN}LEWIS Python setup completed${NC}"
}

# Main function
main() {
    echo -e "${BLUE}Starting pyenv and Python $PYTHON_VERSION installation...${NC}"
    
    install_pyenv_dependencies
    install_pyenv
    install_python
    setup_global_config
    test_installation
    setup_lewis_python
    
    echo ""
    echo -e "${GREEN}✅ Installation completed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "1. Reload your shell: source /etc/profile.d/pyenv.sh"
    echo "2. Verify installation: pyenv versions"
    echo "3. Use Python 3.11.9: pyenv global $PYTHON_VERSION"
    echo "4. For LEWIS: cd $LEWIS_HOME && source activate_python.sh"
    echo ""
    echo -e "${BLUE}You can now run the main LEWIS installation script!${NC}"
}

# Run main function
main "$@"
