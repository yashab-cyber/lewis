# Temporary Uploads Directory

This directory is used by LEWIS to store temporarily uploaded files during processing and analysis.

## Purpose

The temporary uploads directory serves as a secure staging area for:

- **File Analysis**: Temporary storage of files being analyzed for security threats
- **Report Uploads**: User-uploaded files for custom analysis and reporting
- **Configuration Files**: Temporarily uploaded configuration files for processing
- **Log Files**: User-submitted log files for analysis and parsing

## Contents

During operation, this directory may contain:

- **Analysis Files**: Files uploaded for malware analysis, vulnerability scanning
- **Configuration Imports**: Uploaded configuration files being processed
- **Log Analysis**: Log files uploaded for threat detection and analysis
- **Temporary Data**: Intermediate processing files and extracted data

## File Structure

```
temp_uploads/
├── analysis/              # Files for security analysis
├── configs/               # Configuration file uploads
├── logs/                  # Log file uploads
├── reports/               # Report-related uploads
└── processing/            # Files currently being processed
```

## File Lifecycle

1. **Upload**: Files are uploaded via web interface or API
2. **Validation**: Files are scanned and validated for safety
3. **Processing**: Files are processed according to their type
4. **Cleanup**: Files are automatically removed after processing

## Security Features

- **Automatic Scanning**: All uploads are scanned for malware before processing
- **Sandboxing**: File processing occurs in isolated environments
- **Access Control**: Directory access is restricted to LEWIS processes
- **Encryption**: Sensitive files are encrypted at rest
- **Audit Logging**: All file operations are logged for security auditing

## Configuration

Upload behavior is configured in `config/settings.yaml`:

```yaml
uploads:
  temp_directory: "cache/temp_uploads"
  max_file_size: "100MB"
  allowed_extensions: [".txt", ".log", ".conf", ".json", ".xml"]
  retention_hours: 24
  scan_uploads: true
```

## Cleanup Policy

- **Automatic Cleanup**: Files are automatically removed after processing
- **Time-based Cleanup**: Files older than 24 hours are automatically deleted
- **Size-based Cleanup**: Directory size is monitored and managed
- **Manual Cleanup**: Use `lewis --cleanup-uploads` for manual cleanup

## File Size Limits

- **Individual Files**: 100MB maximum by default
- **Total Directory**: 1GB maximum total size
- **Rate Limiting**: Upload rate limits prevent abuse

## Supported File Types

### Analysis Files
- Executable files (for malware analysis)
- Configuration files
- Log files
- Network captures

### Document Types
- Text files (.txt, .log)
- Configuration files (.conf, .ini, .yaml, .json)
- XML files (.xml)
- CSV files (.csv)

## Error Handling

- **Invalid Files**: Rejected files are logged and user is notified
- **Size Exceeded**: Large files are rejected with appropriate error message
- **Disk Space**: Cleanup is triggered when disk space is low
- **Permissions**: Permission errors are logged and reported

## Monitoring

- Upload activity is monitored and logged
- Unusual upload patterns trigger security alerts
- File processing times are tracked for performance optimization

---

**Warning**: This directory is automatically managed. Do not store permanent files here as they will be automatically deleted.

**LEWIS - Linux Environment Working Intelligence System**  
**© 2024 ZehraSec | Created by Yashab Alam**
