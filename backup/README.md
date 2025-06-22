# LEWIS Backup Directory

This directory contains backup files and backup-related scripts for LEWIS.

## Backup Types

### Configuration Backups
- `config_backup_YYYY-MM-DD.tar.gz` - Configuration files backup
- `settings_backup_YYYY-MM-DD.json` - Settings and preferences backup

### Database Backups
- `database_backup_YYYY-MM-DD.sql` - SQL database backup
- `mongodb_backup_YYYY-MM-DD.gz` - MongoDB backup archive
- `knowledge_base_backup_YYYY-MM-DD.json` - Knowledge base backup

### System Backups
- `full_backup_YYYY-MM-DD.tar.gz` - Complete LEWIS installation backup
- `user_data_backup_YYYY-MM-DD.tar.gz` - User data and customizations

## Automated Backups

LEWIS includes automated backup functionality:
- Daily configuration backups
- Weekly database backups  
- Monthly full system backups
- Retention policy: 30 days for dailies, 12 weeks for weeklies, 12 months for monthlies

## Manual Backup Commands

```bash
# Create configuration backup
python scripts/backup_system.py --config

# Create database backup
python scripts/backup_system.py --database

# Create full backup
python scripts/backup_system.py --full

# Restore from backup
python scripts/restore_system.py --file backup_file.tar.gz
```

## Backup Configuration

Configure backup settings in `config/config.yaml`:
```yaml
backup:
  enabled: true
  schedule:
    config: "0 2 * * *"    # Daily at 2 AM
    database: "0 3 * * 0"  # Weekly on Sunday at 3 AM
    full: "0 4 1 * *"      # Monthly on 1st at 4 AM
  retention:
    config: 30
    database: 84
    full: 365
  storage:
    local: true
    remote: false
    encryption: true
```

## Remote Backup

LEWIS supports remote backup storage:
- AWS S3
- Google Cloud Storage
- FTP/SFTP servers
- Network attached storage (NAS)

## Security

- All backups are encrypted by default
- Use strong encryption keys
- Store backup encryption keys separately
- Test backup restoration regularly
- Secure backup storage locations

## Monitoring

Backup status is monitored via:
- LEWIS dashboard
- Log files in `/var/log/lewis/`
- Email notifications (if configured)
- System health checks

## Disaster Recovery

For disaster recovery:
1. Install LEWIS on new system
2. Restore configuration backup
3. Restore database backup
4. Verify system functionality
5. Update any system-specific settings

## Storage Requirements

Typical backup sizes:
- Configuration: ~10MB
- Database: ~100MB-1GB (depends on usage)
- Full backup: ~2-5GB
- Retention: Plan for 6-12 months of backups
