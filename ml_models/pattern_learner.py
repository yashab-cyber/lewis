# trained_model/pattern_learner.py

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class PatternLearner:
    def __init__(self, model_path="trained_models/lewis_pattern_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()

    def load_data(self, log_file_path):
        """
        Load and preprocess the data from log files or CSV format.
        """
        if not os.path.exists(log_file_path):
            raise FileNotFoundError(f"No log data found at {log_file_path}")
        
        df = pd.read_csv(log_file_path)
        if 'timestamp' in df.columns:
            df = df.drop(columns=['timestamp'])

        df.fillna(0, inplace=True)
        data = self.scaler.fit_transform(df)
        return data

    def train_model(self, data):
        """
        Train the pattern detection model.
        """
        print("[+] Training Isolation Forest model for anomaly detection...")
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        self.model.fit(data)
        print("[+] Model training complete.")

    def save_model(self):
        """
        Save the trained model and scaler to disk.
        """
        joblib.dump((self.model, self.scaler), self.model_path)
        print(f"[+] Model saved at {self.model_path}")

    def load_model(self):
        """
        Load the trained model from disk.
        """
        if os.path.exists(self.model_path):
            self.model, self.scaler = joblib.load(self.model_path)
            print("[+] Model loaded successfully.")
        else:
            raise FileNotFoundError("Trained model not found.")

    def predict(self, new_data):
        """
        Predict if new data is normal or an anomaly.
        Returns 1 for normal, -1 for anomaly.
        """
        if self.model is None:
            self.load_model()
        new_data_scaled = self.scaler.transform(new_data)
        return self.model.predict(new_data_scaled)

# Example usage
if __name__ == "__main__":
    learner = PatternLearner()
    try:
        data = learner.load_data("../datasets/system_logs_sample.csv")  # You can replace this with actual logs
        learner.train_model(data)
        learner.save_model()
    except Exception as e:
        print(f"[!] Error: {e}")
