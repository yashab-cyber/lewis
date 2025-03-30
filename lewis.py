import os
import flask
import json
import shutil
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")

# AI Self-Learning: Logs system changes and improves performance
LEARNING_PATH = "learning_data.json"

# Load Learning Data
def load_learning():
    if os.path.exists(LEARNING_PATH):
        with open(LEARNING_PATH, "r") as file:
            return json.load(file)
    return {"improvements": []}

# Save Learning Data
def save_learning(data):
    with open(LEARNING_PATH, "w") as file:
        json.dump(data, file, indent=4)

learning_data = load_learning()

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# AI Self-Modification: Updates itself based on feedback
@app.route('/learn', methods=['POST'])
def learn():
    feedback = request.json.get("feedback")
    if feedback:
        learning_data["improvements"].append(feedback)
        save_learning(learning_data)
        return jsonify({"status": "success", "message": "Learning data updated!"})
    return jsonify({"status": "error", "message": "No feedback received."})

# Execute Cybersecurity Commands
@app.route('/execute', methods=['POST'])
def execute():
    command = request.json.get("command")
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": result})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e.output)})

if __name__ == '__main__':
    app.run(debug=True)

# Frontend: HTML, CSS, JS
frontend_code = """
<!DOCTYPE html>
<html>
<head>
    <title>LEWIS AI</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <h1>Welcome to LEWIS</h1>
    <textarea id="command" placeholder="Enter Command..."></textarea>
    <button onclick="executeCommand()">Run</button>
    <pre id="output"></pre>
    
    <script>
        function executeCommand() {
            let command = document.getElementById("command").value;
            fetch('/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: command })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("output").innerText = data.output || data.error;
            });
        }
    </script>
</body>
</html>
"""

# Save Frontend Files
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
with open("templates/index.html", "w") as f:
    f.write(frontend_code)
with open("static/style.css", "w") as f:
    f.write("body { font-family: Arial, sans-serif; background-color: #121212; color: white; text-align: center; }")
