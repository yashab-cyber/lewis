# LEWIS Models Directory

This directory contains AI/ML models used by LEWIS.

## Model Types

### Voice Recognition Models
- **Vosk Models**: Speech-to-text models for voice interface
  - `vosk-model-en-us-0.22/` - English language model
  - `vosk-model-small-en-us-0.15/` - Lightweight English model

### NLP Models
- **Transformers**: Natural language processing models
  - `bert-base-uncased/` - BERT model for text analysis
  - `sentence-transformers/` - Sentence embedding models

### Threat Detection Models
- **Custom Models**: LEWIS-specific ML models
  - `threat_classifier.pkl` - Threat classification model
  - `anomaly_detector.pkl` - Network anomaly detection model
  - `log_analyzer.pkl` - Log analysis model

### Knowledge Base Models
- **Embeddings**: Pre-trained embeddings for knowledge retrieval
  - `security_embeddings.bin` - Security domain embeddings
  - `command_embeddings.bin` - Command similarity embeddings

## Model Management

### Download Script
Use the model download script to get required models:
```bash
python scripts/download_models.py
```

### Manual Installation
For manual model installation:

1. **Vosk Models**:
   ```bash
   cd models/
   wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
   unzip vosk-model-en-us-0.22.zip
   ```

2. **Transformers Models**:
   ```python
   from transformers import AutoModel, AutoTokenizer
   model = AutoModel.from_pretrained("bert-base-uncased")
   model.save_pretrained("models/bert-base-uncased/")
   ```

### Configuration
Model paths are configured in `config/config.yaml`:
```yaml
ai:
  models:
    voice: "models/vosk-model-en-us-0.22"
    nlp: "models/bert-base-uncased"
    threat_detection: "models/threat_classifier.pkl"
```

## Storage Requirements

Typical model sizes:
- Vosk English model: ~1.8GB
- BERT base model: ~440MB
- Custom models: ~10-100MB each

Total: ~3-5GB for full model suite

## Performance Notes

- Models are loaded into memory on first use
- Consider SSD storage for better loading times
- GPU acceleration available for supported models
- Models can be cached in `cache/model_cache/`

## Licensing

- Vosk models: Apache 2.0 License
- Hugging Face models: Individual model licenses
- Custom LEWIS models: MIT License (same as project)

## Updating Models

Models are automatically updated based on:
- Version compatibility checks
- Performance improvements
- Security updates
- New threat intelligence

## Troubleshooting

Common issues:
- **Model not found**: Run download script or check paths
- **Memory errors**: Use smaller model variants
- **Loading slow**: Move to SSD or increase cache size
- **Version conflicts**: Update model versions in config
