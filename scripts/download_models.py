#!/usr/bin/env python3
"""
Model Download Script for LEWIS
Downloads and sets up required AI/ML models
"""

import os
import sys
import wget
import zipfile
import subprocess
from pathlib import Path
import hashlib

# Model configurations
MODELS = {
    "vosk-en-us": {
        "url": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
        "filename": "vosk-model-en-us-0.22.zip",
        "extract_to": "vosk-model-en-us-0.22",
        "size": "1.8GB",
        "description": "English voice recognition model"
    },
    "vosk-en-us-small": {
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "filename": "vosk-model-small-en-us-0.15.zip", 
        "extract_to": "vosk-model-small-en-us-0.15",
        "size": "40MB",
        "description": "Lightweight English voice recognition model"
    }
}

def print_banner():
    """Print script banner"""
    print("=" * 60)
    print("LEWIS Model Download Script")
    print("=" * 60)

def download_model(model_name, model_config):
    """Download and extract a model"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / model_config["extract_to"]
    
    # Check if model already exists
    if model_path.exists():
        print(f"✅ {model_name} already exists at {model_path}")
        return True
    
    print(f"📥 Downloading {model_name} ({model_config['size']})...")
    print(f"   Description: {model_config['description']}")
    
    try:
        # Download the model
        zip_path = models_dir / model_config["filename"]
        wget.download(model_config["url"], str(zip_path))
        print(f"\n✅ Downloaded {model_config['filename']}")
        
        # Extract the model
        print(f"📂 Extracting to {model_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(models_dir)
        
        # Clean up zip file
        zip_path.unlink()
        print(f"✅ {model_name} installed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {model_name}: {e}")
        return False

def download_transformers_models():
    """Download Hugging Face transformer models"""
    print("📥 Downloading transformer models...")
    
    try:
        from transformers import AutoModel, AutoTokenizer
        
        models_to_download = [
            "bert-base-uncased",
            "sentence-transformers/all-MiniLM-L6-v2"
        ]
        
        for model_name in models_to_download:
            print(f"   Downloading {model_name}...")
            model_path = Path("models") / model_name.replace("/", "_")
            
            if model_path.exists():
                print(f"   ✅ {model_name} already exists")
                continue
                
            # Download model
            model = AutoModel.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Save locally
            model_path.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(model_path)
            tokenizer.save_pretrained(model_path)
            
            print(f"   ✅ {model_name} downloaded")
        
        return True
        
    except ImportError:
        print("   ⚠️ Transformers library not installed. Skipping transformer models.")
        print("   Install with: pip install transformers")
        return False
    except Exception as e:
        print(f"   ❌ Failed to download transformer models: {e}")
        return False

def main():
    """Main download function"""
    print_banner()
    
    # Change to LEWIS root directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir.parent)
    
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Download Vosk models
    success_count = 0
    total_models = len(MODELS)
    
    for model_name, model_config in MODELS.items():
        if download_model(model_name, model_config):
            success_count += 1
        print()
    
    # Download transformer models
    if download_transformers_models():
        print("✅ Transformer models downloaded successfully")
    
    print()
    print("=" * 60)
    print(f"Model Download Complete: {success_count}/{total_models} Vosk models installed")
    print("=" * 60)
    
    if success_count == total_models:
        print("🎉 All models downloaded successfully!")
        print("You can now use LEWIS with full AI capabilities.")
    else:
        print("⚠️ Some models failed to download.")
        print("LEWIS will work with reduced functionality.")
    
    print("\nNext steps:")
    print("1. Run: python lewis.py --mode cli")
    print("2. Try voice commands or text analysis features")

if __name__ == "__main__":
    main()
