#!/bin/bash

echo "==== Installing LEWIS Cybersecurity Assistant ===="

# Update and install basic dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip sqlite3 git curl python3-tk

# Optional: Install additional security tools if on Kali
if command -v apt &> /dev/null; then
    echo "Installing optional security tools (nmap, nikto, metasploit)"
    sudo apt install -y nmap nikto metasploit-framework
fi

# Set working directory
mkdir -p ~/lewis
cd ~/lewis

# Create virtual environment (optional)
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Setup database
echo "Setting up SQLite database..."
sqlite3 database/lewis.db < database/setup_db.sql

# Create application launcher
echo "Creating application shortcut..."
cat <<EOF > ~/.local/share/applications/lewis_ai.desktop
[Desktop Entry]
Name=LEWIS AI Assistant
Comment=Advanced Cybersecurity Tool
Exec=python3 ~/lewis/lewis_gui.py
Icon=~/lewis/components/lewis_icon.png
Terminal=false
Type=Application
Categories=Utility;Security;AI;
EOF

chmod +x ~/.local/share/applications/lewis_ai.desktop
update-desktop-database ~/.local/share/applications/

echo "LEWIS installed successfully! You can find it in your app menu."

# Create uninstall script
cat <<EOF > ~/lewis/uninstall.sh
#!/bin/bash
echo "Uninstalling LEWIS..."
rm -rf ~/lewis
rm ~/.local/share/applications/lewis_ai.desktop
update-desktop-database ~/.local/share/applications/
echo "LEWIS has been removed."
EOF

chmod +x ~/lewis/uninstall.sh

echo "To uninstall LEWIS later, run: ~/lewis/uninstall.sh"

# Make lewis_cli.py executable from anywhere using 'lewis' command
echo "Setting up 'lewis' global command..."

# Ensure shebang exists
LEWIS_CLI="$HOME/lewis/lewis_cli.py"
if ! grep -q "#!/usr/bin/env python3" "$LEWIS_CLI"; then
    sed -i '1i#!/usr/bin/env python3' "$LEWIS_CLI"
fi

chmod +x "$LEWIS_CLI"
sudo ln -sf "$LEWIS_CLI" /usr/local/bin/lewis

echo "You can now run LEWIS CLI from anywhere using: lewis -q"
