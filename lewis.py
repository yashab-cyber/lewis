# LEWIS - Linux Environment Working Intelligence System
# Ethical Hacking AI Assistant with Self-Learning & Modification
# Features: Custom LLM, Cybersecurity Tools, Hacker-Themed UI, Self-Modification

import os
import json
import subprocess
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuration
CONFIG = {
    "knowledge_base": "knowledge.json",
    "scripts_directory": "cybersec_scripts/",
    "self_modifying": True
}

# Load knowledge base
try:
    with open(CONFIG['knowledge_base'], 'r') as f:
        KNOWLEDGE = json.load(f)
except FileNotFoundError:
    KNOWLEDGE = {"threats": [], "tools": []}

# Self-Learning & Modification Engine
def update_knowledge(new_data):
    KNOWLEDGE["threats"].append(new_data)
    with open(CONFIG['knowledge_base'], 'w') as f:
        json.dump(KNOWLEDGE, f, indent=4)

def self_modify():
    if CONFIG["self_modifying"]:
        with open(__file__, 'r+') as f:
            code = f.read()
            # Example modification: Inject a comment
            modified_code = code.replace("# Self-Learning & Modification Engine", "# AI just modified itself!")
            f.seek(0)
            f.write(modified_code)
            f.truncate()

# AI Command Execution
def execute_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return str(e.output.decode("utf-8"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def run_command():
    data = request.json
    command = data.get('command')
    result = execute_command(command)
    return jsonify({"output": result})

@app.route('/train', methods=['POST'])
def train_model():
    data = request.json
    update_knowledge(data)
    return jsonify({"message": "Knowledge updated!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
