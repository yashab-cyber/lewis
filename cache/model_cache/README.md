# Model Cache Directory

This directory is used by LEWIS to store cached AI/ML models for improved performance and reduced load times.

## Purpose

The model cache serves several important functions:

- **Performance Optimization**: Stores pre-loaded machine learning models to avoid repeated loading
- **Memory Management**: Enables efficient model sharing between different LEWIS components
- **Offline Operation**: Allows LEWIS to function with cached models when internet connectivity is limited
- **Custom Models**: Stores user-trained or custom security models

## Contents

When LEWIS is running, this directory may contain:

- **Transformer Models**: Cached natural language processing models
- **Security Models**: Pre-trained threat detection and classification models
- **Custom Models**: User-defined or organization-specific security models
- **Model Metadata**: Configuration files and model information

## File Structure

```
model_cache/
├── transformers/           # Hugging Face transformer models
├── pytorch/               # PyTorch model files
├── sklearn/               # Scikit-learn models
├── custom/                # Custom user models
└── metadata/              # Model configuration files
```

## Cache Management

- **Automatic Cleanup**: LEWIS automatically manages cache size and removes old models
- **Manual Clearing**: Cache can be cleared using `lewis --clear-cache` command
- **Size Limits**: Configurable cache size limits to prevent disk space issues
- **Versioning**: Models are versioned to ensure compatibility

## Configuration

Cache behavior can be configured in `config/settings.yaml`:

```yaml
cache:
  models:
    max_size: "2GB"
    auto_cleanup: true
    retention_days: 30
```

## Security Considerations

- All cached models are validated for integrity before use
- Models from external sources are sandboxed
- Cache directory permissions are restricted to LEWIS user account

## Maintenance

- Cache is automatically maintained by LEWIS
- Manual maintenance should rarely be necessary
- If issues occur, clear cache and restart LEWIS

---

**Note**: This directory is automatically managed by LEWIS. Do not manually modify files unless you understand the implications.

**LEWIS - Linux Environment Working Intelligence System**  
**© 2024 ZehraSec | Created by Yashab Alam**
