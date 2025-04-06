import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

def train_model():
    # Load data
    df = pd.read_csv("datasets/training_logs.csv")

    # Preprocess
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df["log"])
    y = df["threat_level"]

    # Train
    model = MultinomialNB()
    model.fit(X, y)

    # Save model and vectorizer
    model_dir = os.path.join(os.path.dirname(__file__), "trained_models")
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(model, os.path.join(model_dir, "baseline_model.pkl"))
    joblib.dump(vectorizer, os.path.join(model_dir, "vectorizer.pkl"))

    print("[+] ML model trained and saved.")

if __name__ == "__main__":
    train_model()
