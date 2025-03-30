# LEWIS: Linux Environment Working Intelligence System
# Enhanced AI with Self-Learning, Cybersecurity Tools, and Web-Based UI
# Now includes Self-Modification with User Permission

import os
import joblib
import pandas as pd
import numpy as np
import subprocess
import shutil
from flask import Flask, request, render_template, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Initialize Flask App
app = Flask(__name__)

# Load or Create AI Model
def load_or_create_model():
    if os.path.exists("lewis_model.pkl"):
        return joblib.load("lewis_model.pkl")
    else:
        return RandomForestClassifier(n_estimators=100)

# Load or Create Training Data
def load_or_create_data():
    if os.path.exists("lewis_data.csv"):
        return pd.read_csv("lewis_data.csv")
    else:
        return pd.DataFrame(columns=["Command", "Response"])

model = load_or_create_model()
data = load_or_create_data()

# Train Model
def train_model():
    if len(data) > 0:
        X = data["Command"].values.reshape(-1, 1)
        y = data["Response"].values
        model.fit(X, y)
        joblib.dump(model, "lewis_model.pkl")

# Function to Handle Cybersecurity Commands
def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

# LEWIS Chat Function
def lewis_chat(prompt):
    if prompt.lower() in data["Command"].values:
        return data[data["Command"] == prompt]["Response"].values[0]
    else:
        response = execute_command(prompt)
        new_entry = pd.DataFrame({"Command": [prompt], "Response": [response]})
        global data
        data = pd.concat([data, new_entry], ignore_index=True)
        data.to_csv("lewis_data.csv", index=False)
        train_model()
        return response

# Self-Modification Function
def self_modify(code_change, user_confirmation):
    if user_confirmation.lower() == "yes":
        with open("lewis.py", "r") as f:
            lines = f.readlines()
        
        if "# Self-Modification Area" in lines:
            index = lines.index("# Self-Modification Area\n") + 1
            lines.insert(index, f"{code_change}\n")
        else:
            lines.append(f"\n# Self-Modification Area\n{code_change}\n")
        
        with open("lewis.py", "w") as f:
            f.writelines(lines)
        return "Modification applied successfully. Restart required."
    else:
        return "Modification denied by user."

# Flask Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = lewis_chat(user_input)
    return jsonify({"response": response})

@app.route("/modify", methods=["POST"])
def modify():
    code_change = request.json["code"]
    user_confirmation = request.json["confirm"]
    result = self_modify(code_change, user_confirmation)
    return jsonify({"result": result})

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
