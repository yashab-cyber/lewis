# LEWIS Data Directory

This directory contains runtime data files for the LEWIS system.

## Directory Structure

### `/database/`
- **Purpose**: Local database files (SQLite, JSON stores)
- **Contains**: 
  - `lewis.db` - Main SQLite database (auto-generated)
  - `knowledge_base.json` - Knowledge base cache
  - `user_sessions.json` - User session data

### `/uploads/`
- **Purpose**: User uploaded files for analysis
- **Contains**: 
  - Log files uploaded for analysis
  - Configuration files
  - Scripts and code samples
  - Network capture files

### `/reports/`
- **Purpose**: Generated security reports and analyses
- **Contains**: 
  - PDF reports
  - HTML dashboards
  - CSV data exports
  - Analysis results

### `/backups/`
- **Purpose**: Automated backups of critical data
- **Contains**: 
  - Database backups
  - Configuration backups
  - User data exports

## File Management

- Files are automatically organized by date and type
- Old files are cleaned up based on retention policies
- Sensitive data is encrypted at rest

## Security Notes

- This directory may contain sensitive security data
- Ensure proper file permissions (600/700)
- Include in backup procedures
- Exclude from version control (already in .gitignore)

## Storage Limits

Default storage limits (configurable in settings):
- Uploads: 1GB per user, 10GB total
- Reports: 5GB total
- Backups: 30 days retention
- Database: No specific limit

## Permissions

Recommended file permissions:
```bash
chmod 700 data/
chmod 600 data/database/*
chmod 644 data/reports/*.pdf
chmod 600 data/backups/*
```
