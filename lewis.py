import os
import json
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

CONFIG = {
    "knowledge_base": "learning_data.json",
    "self_modify": True,
    "scripts_dir": "cyber_scripts"
}

# Ensure required directories exist
os.makedirs(CONFIG["scripts_dir"], exist_ok=True)

def load_knowledge():
    if not os.path.exists(CONFIG['knowledge_base']):
        return {}
    with open(CONFIG['knowledge_base'], 'r') as f:
        return json.load(f)

def save_knowledge(data):
    with open(CONFIG['knowledge_base'], 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get("target")
    result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True)
    return {"output": result.stdout}

@app.route('/learn', methods=['POST'])
def learn():
    data = request.json
    knowledge = load_knowledge()
    knowledge.update(data)
    save_knowledge(knowledge)
    return {"message": "Data learned successfully."}

@app.route('/self_modify', methods=['POST'])
def self_modify():
    if not CONFIG["self_modify"]:
        return {"error": "Self-modification is disabled."}
    
    script_path = os.path.join(CONFIG["scripts_dir"], "auto_update.py")
    if os.path.exists(script_path):
        subprocess.run(["python3", script_path])
    return {"message": "Self-modification executed."}

if __name__ == '__main__':
    app.run(debug=True)
