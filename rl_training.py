import torch
import json

class ReinforcementTrainer:
    def __init__(self, model, tokenizer, training_data):
        self.model = model
        self.tokenizer = tokenizer
        self.training_data = training_data
        self.reward_memory = {}

    def train(self, epochs=3):
        print("🔄 Starting Reinforcement Learning...")
        for epoch in range(epochs):
            for entry in self.training_data["cybersecurity_commands"]:
                command = entry["command"]
                expected_output = entry["expected_output"]

                # Tokenize input
                inputs = self.tokenizer(command, return_tensors="pt")
                output = self.model.generate(**inputs, max_new_tokens=150)
                response = self.tokenizer.decode(output[0], skip_special_tokens=True)

                # Reward-based learning
                reward = self.evaluate_response(response, expected_output)
                self.reward_memory[command] = reward
                print(f"🧠 Learning: {command} | Reward: {reward}")

        print("✅ Training Complete!")

    def evaluate_response(self, response, expected_output):
        """
        Compares AI response with expected output and assigns a reward score.
        """
        return 1.0 if expected_output.lower() in response.lower() else -1.0

    def refine_code(self, code):
        """
        Automatically refines and improves LEWIS's own code.
        """
        improved_code = code.replace("print", "# Optimized print statement")  # Example modification
        return improved_code
