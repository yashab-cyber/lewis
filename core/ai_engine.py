# lewis/core/ai_engine.py

import random
import json
import os
import time
import logging
import joblib
from datetime import datetime

# Set up logging to track the AI's actions and errors.
logging.basicConfig(filename="lewis_ai.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# === Load vectorizer and model ===
VECTORIZER_PATH = 'ml_models/trained_models/vectorizer.pkl'
MODEL_PATH = 'ml_models/trained_models/threat_model.pkl'

if not os.path.exists(VECTORIZER_PATH) or not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ Model or vectorizer not found. Please train the model first.")

vectorizer = joblib.load(VECTORIZER_PATH)
model = joblib.load(MODEL_PATH)

def detect_threat(log_text):
    """
    Detects if a given log is benign or malicious.

    Args:
        log_text (str): A single log entry.

    Returns:
        str: Predicted label ('benign' or 'malicious')
    """
    log_vector = vectorizer.transform([log_text])
    prediction = model.predict(log_vector)[0]
    return prediction

# LewisAI class: Manages the AI's actions, memory, and responses to user input.
class LewisAI:
    def __init__(self):
        """Initialize the AI with basic info and memory."""
        self.name = "LEWIS"  # Name of the AI
        self.version = "1.1"  # Version of the AI
        self.memory_file = "datasets/threat_patterns.json"  # Path to the memory file
        self.load_memory()  # Load any existing memory from the file

    def load_memory(self):
        """Load memory from a file."""
        # Check if the memory file exists and load it.
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as file:
                    self.memory = json.load(file)  # Load data from the file into memory
            except json.JSONDecodeError:
                # Log an error if there was an issue decoding the JSON file
                logging.error("Error decoding JSON in memory file.")
                self.memory = {}  # Initialize memory as empty if an error occurs
        else:
            self.memory = {}  # Start fresh if no memory file is found
            logging.info("No memory file found. Starting fresh.")

    def save_memory(self):
        """Save memory to a file."""
        try:
            with open(self.memory_file, 'w') as file:
                json.dump(self.memory, file, indent=4)  # Save the memory in a JSON format
            logging.info("Memory saved successfully.")
        except Exception as e:
            # Log any errors encountered while saving the memory
            logging.error(f"Error saving memory: {e}")

    def chat(self, user_input):
        """Generate AI response based on user input."""
        user_input = user_input.lower()  # Convert input to lowercase for easier matching
        # Check for specific keywords in the user input to decide on the response
        if "scan" in user_input:
            return "Would you like me to perform a network scan using Nmap or Nikto?"
        elif "threat" in user_input:
            return "Analyzing for threats... Please wait."
        elif "help" in user_input:
            return "You can ask me to perform scans, analyze logs, or suggest tools."
        else:
            # Randomize the response if no specific intent is detected
            return random.choice([
                "Tell me what you'd like to do.",
                "I'm ready. Ask away!",
                "LEWIS is listening..."
            ])

    def learn_from_log(self, log_data):
        """Store log data and add to memory."""
        timestamp = str(int(time.time()))  # Use the current time as a timestamp for the log
        log_entry = {
            "timestamp": timestamp,  # Timestamp of when the log was added
            "log_data": log_data,  # The log data to be stored
            "learned_at": str(datetime.now())  # When the AI learned from the log
        }
        self.memory[timestamp] = log_entry  # Add the new log entry to memory
        self.save_memory()  # Save the updated memory

    def get_threat_insights(self):
        """Return insights on learned threats."""
        # Return the number of learned threat patterns (logs)
        threat_count = len(self.memory)
        return f"Total learned threat patterns: {threat_count}"

    def introduce(self):
        """Introduce the AI to the user."""
        # Return a string introducing LEWIS to the user
        return f"I am LEWIS (Linux Environment Working Intelligence System), your AI cybersecurity assistant."
    
    def clear_memory(self):
        """Clear all memory."""
        self.memory = {}  # Reset memory to an empty state
        self.save_memory()  # Save the cleared memory (empty)

    def interpret_command(self, user_input):
        """ Simple intent detection and command extraction """
        user_input = user_input.lower()

        if "nmap" in user_input:
            ip = user_input.split("on")[-1].strip()
            return f"nmap -T4 {ip}"

        elif "current processes" in user_input or "running processes" in user_input:
            return "ps aux"

        elif "update all packages" in user_input:
            return "sudo apt update && sudo apt upgrade -y"

        elif "scan" in user_input and "malware" in user_input:
            return "clamscan -r ."

        elif "system status" in user_input or "show system info" in user_input:
            return "neofetch || uname -a"

        return None


# Helper function to generate a response based on user input
def generate_response(user_input):
    ai = LewisAI()  # Create an instance of LEWIS AI
    response = ai.chat(user_input)  # Get a response based on the user's input

    # Simple intent detection for CLI (Command Line Interface)
    intent = None
    # Check if the user input contains certain keywords and assign an appropriate intent
    if "nmap" in user_input.lower() or "scan" in user_input.lower():
        intent = "run_nmap"  # User wants to run a network scan (e.g., Nmap)
    elif "nikto" in user_input.lower():
        intent = "run_nikto"  # User wants to run a Nikto scan
    elif "threat" in user_input.lower() or "predict" in user_input.lower():
        intent = "predict_threat"  # User is asking for threat prediction
    elif "fix" in user_input.lower() or "error" in user_input.lower():
        intent = "self_heal"  # User wants LEWIS to fix an error
    elif "clear memory" in user_input.lower():
        intent = "clear_memory"  # User wants to clear LEWIS's memory
    else:
        intent = "general"  # For general queries that don't match specific intents

    return response, intent  # Return the AI's response and the detected intent

def hybrid_threat_analysis(log_text_csv):
    from ml_models.pattern_learner import PatternLearner
    from ml_models.threat_detection import detect_threat
    import pandas as pd
    from io import StringIO

    results = {}

    # Text Classification
    try:
        text_prediction = detect_threat(log_text_csv)
        results['Classifier Result'] = text_prediction
    except Exception as e:
        results['Classifier Result'] = f"Error: {e}"

    # Anomaly Detection
    try:
        learner = PatternLearner()
        learner.load_model()
        df = pd.read_csv(StringIO(log_text_csv))
        if 'timestamp' in df.columns:
            df.drop(columns=['timestamp'], inplace=True)
        preds = learner.predict(df)
        anomaly_count = sum(pred == -1 for pred in preds)
        results['Anomaly Detection'] = f"{anomaly_count} anomalies in {len(preds)} rows"
    except Exception as e:
        results['Anomaly Detection'] = f"Error: {e}"

    return results

# Main function to run the interactive CLI with LEWIS
def main():
    ai = LewisAI()  # Create an instance of LEWIS AI

    print("Welcome to LEWIS. Type 'help' for options.")  # Greet the user
    while True:
        user_input = input("\nUser: ")  # Prompt the user for input
        
        if user_input.lower() == "exit":  # Exit the loop if the user types 'exit'
            print("Goodbye!")
            break
        
        # Handle the user input by generating a response and determining the intent
        response, intent = generate_response(user_input)
        print(f"LEWIS: {response}")  # Print LEWIS's response

        # Execute actions based on detected intent
        if intent == "run_nmap":
            print("[LEWIS] Running Nmap scan...")
            # Add Nmap scanning logic here (or call to nmap_wrapper)

        elif intent == "run_nikto":
            print("[LEWIS] Running Nikto scan...")
            # Add Nikto scanning logic here (or call to nikto_integration)

        elif intent == "predict_threat":
            print("[LEWIS] Predicting threat level using both ML model and anomaly detection...")
            logs = input("Paste system logs or CSV content (text or metrics):\n")
            print("[LEWIS] Running hybrid threat analysis...")
            results = hybrid_threat_analysis(logs)
            for model_type, result in results.items():
                print(f"[{model_type}] {result}")  # Add ML-based threat prediction here

        elif intent == "self_heal":
            print("[LEWIS] Performing self-healing...")
            error_msg = input("Paste the error message for self-healing: ")
            if error_msg:
                print(f"[LEWIS] Error fixed: {error_msg}")  # Integrate auto-fix logic here

        elif intent == "clear_memory":
            ai.clear_memory()  # Clear the AI's memory
            print("[LEWIS] Memory cleared successfully.")

        elif intent == "general":
            print(f"[LEWIS] {response}")  # For general queries, just print the AI's response

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
