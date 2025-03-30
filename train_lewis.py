import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
from huggingface_hub import login
from flask import Flask, render_template, request, jsonify

# Authenticate with Hugging Face
token = "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"
login(token)

# Model and Dataset Configuration
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
DATASET_PATH = "./datasets/cybersecurity_data.json"

# Load Dataset
try:
    dataset = load_dataset('json', data_files=DATASET_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load dataset: {e}")

# Load Tokenizer and Model
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, use_auth_token=True)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Tokenization Function
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Training Configuration
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=5,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=10,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets.get("validation"),
)

# Flask Web UI Setup
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["question"]
    inputs = tokenizer(user_input, return_tensors="pt")
    output = model.generate(**inputs, max_length=150)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return jsonify({"response": response})

if __name__ == "__main__":
    trainer.train()
    model.save_pretrained("./trained_model")
    tokenizer.save_pretrained("./trained_model")
    app.run(host="0.0.0.0", port=5000)
