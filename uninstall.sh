#!/bin/bash

# LEWIS - Linux Environment Working Intelligence System
# Uninstallation Script for Linux Systems

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

# Print banner
print_banner() {
    echo -e "${RED}"
    echo "██╗   ██╗███╗   ██╗██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     "
    echo "██║   ██║████╗  ██║██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     "
    echo "██║   ██║██╔██╗ ██║██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     "
    echo "██║   ██║██║╚██╗██║██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     "
    echo "╚██████╔╝██║ ╚████║██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗"
    echo " ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝"
    echo -e "${NC}"
    echo -e "${CYAN}LEWIS Uninstallation Script${NC}"
    echo ""
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}This script must be run as root (use sudo)${NC}"
        exit 1
    fi
}

# Confirm uninstallation
confirm_uninstall() {
    echo -e "${YELLOW}WARNING: This will completely remove LEWIS from your system!${NC}"
    echo ""
    echo "The following will be removed:"
    echo "• LEWIS service and files"
    echo "• User account: $LEWIS_USER"
    echo "• Configuration files"
    echo "• Log files"
    echo "• Database data (if you choose to)"
    echo ""
    
    read -p "Are you sure you want to uninstall LEWIS? (yes/no): " confirm
    if [[ $confirm != "yes" ]]; then
        echo -e "${BLUE}Uninstallation cancelled${NC}"
        exit 0
    fi
    
    echo ""
    read -p "Do you want to remove all data including databases? (yes/no): " remove_data
}

# Stop and disable service
stop_service() {
    echo -e "${YELLOW}Stopping LEWIS service...${NC}"
    
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        systemctl stop "$SERVICE_NAME"
        echo -e "${GREEN}Service stopped${NC}"
    fi
    
    if systemctl is-enabled --quiet "$SERVICE_NAME"; then
        systemctl disable "$SERVICE_NAME"
        echo -e "${GREEN}Service disabled${NC}"
    fi
    
    # Remove service file
    if [[ -f "/etc/systemd/system/$SERVICE_NAME.service" ]]; then
        rm -f "/etc/systemd/system/$SERVICE_NAME.service"
        systemctl daemon-reload
        echo -e "${GREEN}Service file removed${NC}"
    fi
}

# Remove files and directories
remove_files() {
    echo -e "${YELLOW}Removing LEWIS files...${NC}"
    
    # Remove main installation directory
    if [[ -d "$LEWIS_HOME" ]]; then
        rm -rf "$LEWIS_HOME"
        echo -e "${GREEN}Installation directory removed${NC}"
    fi
    
    # Remove configuration
    if [[ -d "$LEWIS_CONFIG" ]]; then
        rm -rf "$LEWIS_CONFIG"
        echo -e "${GREEN}Configuration files removed${NC}"
    fi
    
    # Remove logs
    if [[ -d "$LEWIS_LOGS" ]]; then
        rm -rf "$LEWIS_LOGS"
        echo -e "${GREEN}Log files removed${NC}"
    fi
    
    # Remove data (if requested)
    if [[ $remove_data == "yes" && -d "$LEWIS_DATA" ]]; then
        rm -rf "$LEWIS_DATA"
        echo -e "${GREEN}Data files removed${NC}"
    elif [[ -d "$LEWIS_DATA" ]]; then
        echo -e "${BLUE}Data files preserved at $LEWIS_DATA${NC}"
    fi
    
    # Remove symlinks
    rm -f "/usr/local/bin/lewis"
    rm -f "/usr/local/bin/lewis-cli"
    rm -f "/usr/local/bin/lewis-gui"
    echo -e "${GREEN}Command symlinks removed${NC}"
    
    # Remove logrotate configuration
    if [[ -f "/etc/logrotate.d/lewis" ]]; then
        rm -f "/etc/logrotate.d/lewis"
        echo -e "${GREEN}Logrotate configuration removed${NC}"
    fi
    
    # Remove nginx configuration (if exists)
    if [[ -f "/etc/nginx/sites-available/lewis" ]]; then
        rm -f "/etc/nginx/sites-available/lewis"
        rm -f "/etc/nginx/sites-enabled/lewis"
        nginx -t && systemctl reload nginx 2>/dev/null || true
        echo -e "${GREEN}Nginx configuration removed${NC}"
    fi
}

# Remove system user
remove_user() {
    echo -e "${YELLOW}Removing LEWIS user...${NC}"
    
    if id "$LEWIS_USER" &>/dev/null; then
        # Kill any running processes by the user
        pkill -u "$LEWIS_USER" 2>/dev/null || true
        sleep 2
        
        # Remove user
        userdel -r "$LEWIS_USER" 2>/dev/null || userdel "$LEWIS_USER" 2>/dev/null || true
        echo -e "${GREEN}User $LEWIS_USER removed${NC}"
    else
        echo -e "${BLUE}User $LEWIS_USER not found${NC}"
    fi
}

# Clean up databases
cleanup_databases() {
    if [[ $remove_data == "yes" ]]; then
        echo -e "${YELLOW}Cleaning up databases...${NC}"
        
        # MongoDB cleanup
        if command -v mongo &> /dev/null; then
            mongo --eval "
                use lewis;
                db.dropDatabase();
                use admin;
                db.dropUser('lewis');
            " 2>/dev/null || true
            echo -e "${GREEN}MongoDB data cleaned${NC}"
        fi
        
        # Redis cleanup (if dedicated to LEWIS)
        if command -v redis-cli &> /dev/null; then
            read -p "Clear Redis data? This will affect other applications using Redis (yes/no): " clear_redis
            if [[ $clear_redis == "yes" ]]; then
                redis-cli FLUSHALL 2>/dev/null || true
                echo -e "${GREEN}Redis data cleared${NC}"
            fi
        fi
    fi
}

# Remove firewall rules
remove_firewall_rules() {
    echo -e "${YELLOW}Removing firewall rules...${NC}"
    
    if command -v ufw &> /dev/null; then
        # Ubuntu/Debian UFW
        ufw delete allow 8000/tcp 2>/dev/null || true
        echo -e "${GREEN}UFW rules removed${NC}"
    elif command -v firewall-cmd &> /dev/null; then
        # CentOS/RHEL firewalld
        firewall-cmd --permanent --remove-port=8000/tcp 2>/dev/null || true
        firewall-cmd --reload 2>/dev/null || true
        echo -e "${GREEN}Firewalld rules removed${NC}"
    elif command -v iptables &> /dev/null; then
        # Generic iptables
        iptables -D INPUT -p tcp --dport 8000 -j ACCEPT 2>/dev/null || true
        
        # Save rules
        if command -v iptables-save &> /dev/null; then
            iptables-save > /etc/iptables/rules.v4 2>/dev/null || \
            iptables-save > /etc/sysconfig/iptables 2>/dev/null || true
        fi
        echo -e "${GREEN}Iptables rules removed${NC}"
    fi
}

# Optional: Remove system dependencies
remove_dependencies() {
    echo ""
    read -p "Do you want to remove LEWIS-specific system dependencies? (yes/no): " remove_deps
    
    if [[ $remove_deps == "yes" ]]; then
        echo -e "${YELLOW}Removing system dependencies...${NC}"
        echo -e "${RED}WARNING: This may affect other applications!${NC}"
        
        # Detect OS
        if [[ -f /etc/os-release ]]; then
            . /etc/os-release
            OS=$NAME
        fi
        
        case "$OS" in
            "Ubuntu"*|"Debian"*|"Kali"*)
                apt-get remove -y \
                    mongodb \
                    redis-server \
                    supervisor \
                    nikto \
                    dirb \
                    gobuster \
                    sqlmap \
                    john \
                    hashcat \
                    hydra \
                    espeak \
                    festival 2>/dev/null || true
                apt-get autoremove -y
                ;;
            "CentOS"*|"Red Hat"*|"Rocky"*|"AlmaLinux"*)
                yum remove -y \
                    mongodb-server \
                    redis \
                    supervisor \
                    nikto \
                    john \
                    hydra \
                    espeak \
                    festival 2>/dev/null || true
                ;;
            "Arch"*|"Manjaro"*)
                pacman -Rs --noconfirm \
                    mongodb \
                    redis \
                    supervisor \
                    nikto \
                    dirb \
                    gobuster \
                    sqlmap \
                    metasploit \
                    john \
                    hashcat \
                    hydra \
                    espeak \
                    festival 2>/dev/null || true
                ;;
        esac
        
        echo -e "${GREEN}Dependencies removed${NC}"
    fi
}

# Print completion message
print_completion() {
    echo ""
    echo -e "${CYAN}=========================${NC}"
    echo -e "${CYAN}  UNINSTALL COMPLETE     ${NC}"
    echo -e "${CYAN}=========================${NC}"
    echo ""
    echo -e "${GREEN}LEWIS has been successfully removed from your system!${NC}"
    echo ""
    
    if [[ $remove_data != "yes" && -d "$LEWIS_DATA" ]]; then
        echo -e "${YELLOW}Note: Data files were preserved at:${NC}"
        echo "• $LEWIS_DATA"
        echo ""
        echo "To completely remove all data, run:"
        echo "sudo rm -rf $LEWIS_DATA"
        echo ""
    fi
    
    echo -e "${BLUE}Thank you for using LEWIS!${NC}"
    echo ""
}

# Main uninstallation function
main() {
    print_banner
    check_root
    confirm_uninstall
    
    echo -e "${BLUE}Starting LEWIS uninstallation...${NC}"
    echo ""
    
    stop_service
    remove_files
    remove_user
    cleanup_databases
    remove_firewall_rules
    remove_dependencies
    
    print_completion
}

# Run main function
main "$@"
