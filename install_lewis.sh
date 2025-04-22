#!/bin/bash

echo "==== Installing LEWIS Cybersecurity Assistant ===="

# Update and install basic dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip sqlite3 git curl

# Optional: Install additional security tools if on Kali
if command -v apt &> /dev/null; then
    echo "Installing optional security tools (nmap, nikto, metasploit)"
    sudo apt install -y nmap nikto metasploit-framework
fi

# Set working directory
mkdir -p ~/lewis
cd ~/lewis

# Clone or copy files from unzipped archive (Assume files already present)
echo "Copying LEWIS files..."
# For now, we assume files are extracted into ~/lewis

# Create virtual environment (optional)
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Setup database
echo "Setting up SQLite database..."
sqlite3 database/lewis.db < database/setup_db.sql

# Final message
echo "LEWIS setup complete!"
echo "To launch LEWIS, run: python3 main.py or ./lewis-cli.py"
