#!/bin/bash
# LEWIS Kali Tool Integration Script

echo "[+] Checking for required tools: Nmap, Nikto, Metasploit..."

which nmap > /dev/null || sudo apt install nmap -y
which nikto > /dev/null || sudo apt install nikto -y
which msfconsole > /dev/null || sudo apt install metasploit-framework -y

echo "[+] Setting up symlinks if needed..."

if [ ! -d "/usr/share/metasploit-framework" ]; then
    echo "[-] Metasploit not found or misconfigured"
else
    echo "[✓] Metasploit installed"
fi

echo "[✓] Kali integration complete!"
