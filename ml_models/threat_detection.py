import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# === File paths ===
DATASET_PATH = "datasets/training_logs.csv"
MODEL_DIR = "ml_models/trained_models"
MODEL_FILE = os.path.join(MODEL_DIR, "threat_model.pkl")
VECTORIZER_FILE = os.path.join(MODEL_DIR, "vectorizer.pkl")

# === Training the AI model ===
def train_threat_model():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)

    if 'log' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must contain 'log' and 'label' columns")

    X = df['log']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000, C=1.0)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    print("\n🎯 Classification Report:\n")
    print(classification_report(y_test, y_pred))
    print(f"✅ Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print(f"\n📦 Model saved to: {MODEL_FILE}")
    print(f"📦 Vectorizer saved to: {VECTORIZER_FILE}")

# === Predicting using trained model ===
def detect_threat(log_text):
    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)
    input_vec = vectorizer.transform([log_text])
    prediction = model.predict(input_vec)
    return prediction[0]

# === For CLI or real-time integration ===
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        train_threat_model()
    elif len(sys.argv) > 2 and sys.argv[1] == "predict":
        result = detect_threat(sys.argv[2])
        print(f"🧠 Threat Prediction: {result}")
    else:
        print("Usage:\n python threat_detection.py train\n python threat_detection.py predict \"<log text>\"")
