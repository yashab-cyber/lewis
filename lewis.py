import openai
import os
import joblib
import pandas as pd
from flask import Flask, request, render_template, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load or create ML model
def load_or_create_model():
    if os.path.exists("lewis_model.pkl"):
        return joblib.load("lewis_model.pkl")
    else:
        return RandomForestClassifier(n_estimators=100)

model = load_or_create_model()

def train_model(data, labels):
    global model
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "lewis_model.pkl")
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return accuracy

def lewis_chat(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = lewis_chat(user_input)
    return jsonify({"LEWIS": response})

@app.route('/train', methods=['POST'])
def train():
    data = pd.DataFrame(request.json["data"])
    labels = request.json["labels"]
    accuracy = train_model(data, labels)
    return jsonify({"message": "Model trained successfully", "accuracy": accuracy})

if __name__ == '__main__':
    print("LEWIS (Linux Environment Working Intelligence System) is now running...")
    app.run(host='0.0.0.0', port=5000, debug=True)
