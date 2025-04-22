#!/data/data/com.termux/files/usr/bin/bash
# LEWIS Termux Setup Script

echo "[+] Updating packages..."
pkg update && pkg upgrade -y

echo "[+] Installing Python & Pip..."
pkg install python -y
pip install --upgrade pip

echo "[+] Installing required libraries..."
pip install flask flask-cors openai scikit-learn pandas joblib speechrecognition pyttsx3 sqlite3

echo "[+] Installing Node.js for frontend..."
pkg install nodejs -y
npm install -g create-react-app

echo "[+] Setting executable permissions..."
chmod +x lewis-cli.py

echo "[+] Creating initial database..."
python setup_db.py

echo "[✓] LEWIS installed in Termux!"
