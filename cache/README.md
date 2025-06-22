# LEWIS Cache Directory

This directory contains cached data to improve LEWIS performance.

## Cache Types

### AI Model Cache
- **Purpose**: Cached AI models and embeddings
- **Files**: 
  - `model_cache/` - Downloaded and processed AI models
  - `embeddings/` - Pre-computed text embeddings
  - `transformers_cache/` - Hugging Face model cache

### Threat Intelligence Cache
- **Purpose**: Cached threat intelligence data
- **Files**:
  - `threat_feeds/` - Downloaded threat intelligence feeds
  - `cve_data/` - CVE database cache
  - `ioc_cache/` - Indicators of Compromise cache

### Analysis Cache
- **Purpose**: Cached analysis results
- **Files**:
  - `scan_results/` - Cached network scan results
  - `log_analysis/` - Cached log analysis results
  - `report_cache/` - Cached report components

### Session Cache
- **Purpose**: User session and temporary data
- **Files**:
  - `user_sessions/` - Active user session data
  - `temp_uploads/` - Temporary uploaded files
  - `work_dir/` - Temporary working directories

## Cache Management

- Cache files are automatically cleaned based on age and size limits
- Cache can be manually cleared using: `python lewis.py --clear-cache`
- Configure cache settings in `config/config.yaml`

## Storage Limits

Default cache limits (configurable):
- AI models: 2GB total
- Threat intelligence: 500MB
- Analysis results: 1GB
- Session data: 100MB per user

## Performance Notes

- Larger cache improves performance but uses more disk space
- SSD storage recommended for cache directory
- Consider cache directory location for performance optimization

## Security

- Cache may contain sensitive analysis data
- Ensure proper file permissions
- Consider encryption for sensitive cache data
- Exclude from backups if data is regenerable
