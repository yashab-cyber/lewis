import os
import json
import subprocess
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

CONFIG = {
    "knowledge_base": "knowledge.json",
    "code_archive": "code_evolution/",
    "sources": [
        "https://www.kali.org/docs/",
        "https://owasp.org/www-project-top-ten/"
    ]
}

class LewisAI:
    def __init__(self):
        self.knowledge = self.load_knowledge()

    def load_knowledge(self):
        try:
            with open(CONFIG['knowledge_base'], 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"patterns": [], "vulnerabilities": [], "techniques": []}

    def scrape_security_data(self):
        for source in CONFIG['sources']:
            try:
                response = requests.get(source, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                if "kali.org" in source:
                    self.process_kali_docs(soup)
            except Exception as e:
                print(f"Error processing {source}: {str(e)}")
        self.save_knowledge()

    def process_kali_docs(self, soup):
        tools = soup.find_all('div', class_='tool-card')
        for tool in tools:
            metadata = {
                'name': tool.h3.text.strip(),
                'description': tool.p.text
            }
            if metadata not in self.knowledge['patterns']:
                self.knowledge['patterns'].append(metadata)

    def save_knowledge(self):
        with open(CONFIG['knowledge_base'], 'w') as f:
            json.dump(self.knowledge, f, indent=4)

    def execute_cyber_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e)

lewis_ai = LewisAI()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    command = data.get("command")
    result = lewis_ai.execute_cyber_command(command)
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(debug=True)

# Frontend UI/UX (index.html)
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEWIS AI - Cybersecurity Assistant</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="container">
        <h1>LEWIS AI - Cybersecurity Assistant</h1>
        <textarea id="command" placeholder="Enter command..."></textarea>
        <button onclick="executeCommand()">Execute</button>
        <pre id="output"></pre>
    </div>
    <script src="static/script.js"></script>
</body>
</html>
'''

with open("templates/index.html", "w") as f:
    f.write(html_content)

# CSS (static/style.css)
css_content = '''
body {
    font-family: Arial, sans-serif;
    background-color: #121212;
    color: white;
    text-align: center;
}
.container {
    margin: 50px auto;
    width: 50%;
    padding: 20px;
    background-color: #1e1e1e;
    border-radius: 10px;
}
textarea {
    width: 100%;
    height: 100px;
    background-color: #333;
    color: white;
    border: none;
    padding: 10px;
}
button {
    margin-top: 10px;
    padding: 10px;
    background-color: #007BFF;
    color: white;
    border: none;
    cursor: pointer;
}
pre {
    background-color: black;
    color: #00FF00;
    padding: 10px;
    height: 200px;
    overflow-y: auto;
    text-align: left;
}
'''

with open("static/style.css", "w") as f:
    f.write(css_content)

# JavaScript (static/script.js)
js_content = '''
function executeCommand() {
    const command = document.getElementById("command").value;
    fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = data.output;
    });
}
'''

with open("static/script.js", "w") as f:
    f.write(js_content)
