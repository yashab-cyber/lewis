# lewis/core/ai_engine.py

import random
import json
import os
import time

class LewisAI:
    def __init__(self):
        self.name = "LEWIS"
        self.version = "1.0"
        self.memory_file = "datasets/threat_patterns.json"
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                self.memory = json.load(file)
        else:
            self.memory = {}

    def save_memory(self):
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file, indent=4)

    def chat(self, user_input):
        if "scan" in user_input.lower():
            return "Would you like me to perform a network scan using Nmap or Nikto?"
        elif "threat" in user_input.lower():
            return "Analyzing for threats... Please wait."
        elif "help" in user_input.lower():
            return "You can ask me to perform scans, analyze logs, or suggest tools."
        else:
            return random.choice([
                "Tell me what you'd like to do.",
                "I'm ready. Ask away!",
                "LEWIS is listening..."
            ])

    def learn_from_log(self, log_data):
        timestamp = str(int(time.time()))
        self.memory[timestamp] = log_data
        self.save_memory()

    def get_threat_insights(self):
        return f"Total learned threat patterns: {len(self.memory)}"

    def introduce(self):
        return f"I am LEWIS (Linux Environment Working Intelligence System), your AI cybersecurity assistant."
