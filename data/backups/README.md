# Database Backups Directory

This directory is used by LEWIS to store automated database backups for data protection and disaster recovery.

## Purpose

The database backups directory provides:

- **Data Protection**: Regular backups of LEWIS databases and configurations
- **Disaster Recovery**: Backup data for system recovery and restoration
- **Point-in-Time Recovery**: Multiple backup points for selective restoration
- **Migration Support**: Backup files for system migration and upgrades
- **Compliance**: Data retention for audit and compliance requirements

## Contents

This directory will contain:

- **Database Dumps**: SQL dumps of LEWIS operational databases
- **Configuration Backups**: Snapshots of system configurations
- **User Data Backups**: Backed up user profiles and custom settings
- **Report Archives**: Archived reports and analysis results
- **System State Backups**: Complete system state snapshots

## File Structure

```
backups/
├── daily/                 # Daily automated backups
│   ├── database/          # Daily database dumps
│   ├── config/            # Daily configuration backups
│   └── reports/           # Daily report archives
├── weekly/                # Weekly full system backups
│   ├── full_system/       # Complete system backups
│   └── user_data/         # User data backups
├── monthly/               # Monthly long-term backups
│   └── archives/          # Long-term archive storage
└── manual/                # Manual backup snapshots
    └── pre_upgrade/       # Pre-upgrade system snapshots
```

## Backup Types

### Automated Backups

#### Daily Backups
- **Database Dumps**: Complete PostgreSQL/SQLite database exports
- **Configuration Files**: Backup of all LEWIS configuration files
- **User Profiles**: User settings and custom configurations
- **Recent Reports**: Latest generated reports and analysis results

#### Weekly Backups
- **Full System State**: Complete system configuration and data
- **Log Archives**: Compressed log file archives
- **Threat Feed Data**: Cached threat intelligence data
- **Model Snapshots**: AI/ML model state backups

#### Monthly Backups
- **Long-term Archives**: Compressed long-term storage backups
- **Compliance Data**: Data required for regulatory compliance
- **Historical Analysis**: Historical analysis data and trends
- **System Metrics**: Performance and usage metrics archives

### Manual Backups
- **Pre-upgrade Snapshots**: System state before major updates
- **Configuration Changes**: Backups before significant configuration changes
- **Custom Snapshots**: User-initiated backup points
- **Migration Backups**: Data exports for system migration

## Backup Configuration

Backup settings are configured in `config/backup.yaml`:

```yaml
backup:
  enabled: true
  schedule:
    daily: "02:00"           # Daily backup at 2 AM
    weekly: "Sunday 03:00"   # Weekly backup on Sunday at 3 AM
    monthly: "1st 04:00"     # Monthly backup on 1st at 4 AM
  
  retention:
    daily: 7                 # Keep 7 daily backups
    weekly: 4                # Keep 4 weekly backups
    monthly: 12              # Keep 12 monthly backups
  
  compression: true          # Compress backup files
  encryption: true           # Encrypt sensitive backups
  
  destinations:
    local: true              # Store locally in this directory
    remote: false            # Remote storage (S3, FTP, etc.)
    
  exclude:                   # Exclude from backups
    - "cache/temp_uploads/"
    - "logs/debug.log"
```

## Backup Process

### Automatic Backup Workflow
1. **Pre-backup Checks**: Verify system health and available space
2. **Database Lock**: Safely lock databases for consistent backup
3. **Data Export**: Export databases and configuration files
4. **Compression**: Compress backup data to save space
5. **Encryption**: Encrypt sensitive backup data
6. **Verification**: Verify backup integrity and completeness
7. **Cleanup**: Remove old backups according to retention policy

### Manual Backup Commands
```bash
# Create manual backup
lewis backup create --name "pre-upgrade-$(date +%Y%m%d)"

# List available backups
lewis backup list

# Restore from backup
lewis backup restore --backup daily-20241201-020000

# Verify backup integrity
lewis backup verify --backup weekly-20241201-030000
```

## Restoration Process

### Full System Restoration
1. **Stop LEWIS Services**: Safely stop all LEWIS components
2. **Backup Current State**: Create backup of current system (if possible)
3. **Extract Backup**: Extract and decrypt backup data
4. **Database Restoration**: Restore database from backup dumps
5. **Configuration Restoration**: Restore configuration files
6. **Service Restart**: Restart LEWIS services
7. **Verification**: Verify system functionality after restoration

### Selective Restoration
- **Database Only**: Restore only database components
- **Configuration Only**: Restore configuration files
- **User Data Only**: Restore user profiles and settings
- **Reports Only**: Restore specific reports or analysis data

## Security Features

### Encryption
- **AES-256 Encryption**: Strong encryption for sensitive backup data
- **Key Management**: Secure key storage and rotation
- **Access Control**: Encrypted backups require proper credentials
- **Transport Security**: Encrypted transmission for remote backups

### Access Control
- **File Permissions**: Restricted access to backup files
- **User Authentication**: Authentication required for backup operations
- **Audit Logging**: All backup operations are logged
- **Integrity Checks**: Backup integrity is verified regularly

## Storage Management

### Space Optimization
- **Compression**: Backup files are compressed to save space
- **Deduplication**: Eliminate duplicate data across backups
- **Incremental Backups**: Only backup changed data when possible
- **Cleanup Policies**: Automatic cleanup of old backups

### Storage Monitoring
- **Disk Usage**: Monitor backup directory disk usage
- **Growth Trends**: Track backup size growth over time
- **Capacity Planning**: Plan for future storage needs
- **Alerts**: Alert when storage limits are approached

## Remote Backup Options

### Supported Destinations
- **AWS S3**: Amazon S3 bucket storage
- **Google Cloud**: Google Cloud Storage
- **Azure Blob**: Microsoft Azure Blob Storage
- **FTP/SFTP**: Remote FTP/SFTP servers
- **Network Shares**: SMB/NFS network shares

### Configuration Example
```yaml
backup:
  destinations:
    s3:
      enabled: true
      bucket: "lewis-backups"
      region: "us-east-1"
      access_key: "${AWS_ACCESS_KEY}"
      secret_key: "${AWS_SECRET_KEY}"
      encryption: true
```

## Monitoring and Alerting

### Backup Monitoring
- **Success/Failure Tracking**: Monitor backup job success rates
- **Performance Metrics**: Track backup completion times
- **Storage Utilization**: Monitor backup storage usage
- **Data Integrity**: Regular integrity checks on backup data

### Alert Conditions
- **Failed Backups**: Alert when backup jobs fail
- **Long-running Backups**: Alert for unusually long backup times
- **Storage Issues**: Alert when storage space is low
- **Integrity Failures**: Alert when backup verification fails

## Compliance and Retention

### Data Retention Policy
- **Regulatory Requirements**: Meet compliance data retention requirements
- **Business Continuity**: Ensure adequate backup retention for recovery
- **Storage Optimization**: Balance retention needs with storage costs
- **Legal Holds**: Support for legal hold requirements

### Audit Requirements
- **Backup Logs**: Detailed logs of all backup operations
- **Access Tracking**: Track who accesses backup data
- **Retention Proof**: Demonstrate compliance with retention policies
- **Recovery Testing**: Regular testing of backup restoration procedures

## Troubleshooting

### Common Issues
- **Insufficient Space**: Ensure adequate disk space for backups
- **Permission Errors**: Verify backup directory permissions
- **Database Locks**: Resolve database locking issues
- **Network Issues**: Check network connectivity for remote backups

### Recovery Scenarios
- **Corrupted Database**: Restore from most recent clean backup
- **Configuration Loss**: Restore configuration from backup
- **System Failure**: Full system restoration from backup
- **Data Corruption**: Selective restoration of affected components

---

**Important**: This directory contains critical backup data. Ensure adequate protection and access controls are in place.

**LEWIS - Linux Environment Working Intelligence System**  
**© 2024 ZehraSec | Created by Yashab Alam**
