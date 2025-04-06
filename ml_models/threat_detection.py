import joblib
import re
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_models", "baseline_model.pkl")

def clean_input(log_data):
    return re.sub(r'[^\w\s]', '', log_data.lower())

def predict_threat(log_data):
    try:
        model = joblib.load(MODEL_PATH)
        cleaned = clean_input(log_data)
        features = [cleaned]  # Simplified input
        prediction = model.predict(features)
        return prediction[0]
    except Exception as e:
        return f"[ERROR] ML model failed: {str(e)}"
