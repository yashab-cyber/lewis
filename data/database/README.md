# Database Directory

This directory contains the LEWIS database files and related database management components.

## Purpose

The database directory serves as the primary data storage location for:

- **Operational Data**: Core LEWIS application data and configurations
- **User Information**: User accounts, profiles, and authentication data
- **Analysis Results**: Stored results from security analyses and scans
- **Threat Intelligence**: Processed and normalized threat intelligence data
- **System Logs**: Structured log data for analysis and reporting
- **Configuration History**: Historical configuration changes and versions

## Contents

When LEWIS is operational, this directory contains:

- **SQLite Databases**: Local database files for development and small deployments
- **PostgreSQL Data**: Data directory for PostgreSQL installations
- **Database Indexes**: Performance optimization indexes
- **Transaction Logs**: Database transaction and recovery logs
- **Schema Files**: Database schema definitions and migration scripts

## File Structure

```
database/
├── lewis_main.db          # Main LEWIS SQLite database
├── users.db               # User authentication database
├── threat_intel.db        # Threat intelligence database
├── analysis_results.db    # Analysis and scan results
├── system_logs.db         # Structured system logs
├── postgres/              # PostgreSQL data directory (if used)
│   ├── base/              # Database files
│   ├── global/            # Global data
│   ├── pg_wal/            # Write-ahead logs
│   └── pg_stat_tmp/       # Temporary statistics
└── migrations/            # Database migration scripts
    ├── 001_initial.sql    # Initial schema
    ├── 002_users.sql      # User management tables
    └── 003_threat_intel.sql # Threat intelligence schema
```

## Database Types

### SQLite (Default)
- **Single-file Databases**: Self-contained database files
- **No Server Required**: Embedded database engine
- **Development Friendly**: Easy setup and maintenance
- **Backup Simple**: Simple file copying for backups
- **Performance**: Suitable for small to medium deployments

### PostgreSQL (Enterprise)
- **Client-Server**: Dedicated database server
- **High Performance**: Optimized for concurrent access
- **Advanced Features**: JSON, full-text search, extensions
- **Scalability**: Suitable for large enterprise deployments
- **ACID Compliance**: Full transaction support

## Database Schema

### Core Tables

#### Users and Authentication
```sql
-- User accounts and authentication
users (id, username, email, password_hash, created_at, last_login)
user_sessions (id, user_id, session_token, expires_at)
user_permissions (user_id, permission, granted_at)
```

#### Security Analysis
```sql
-- Analysis and scan results
scan_jobs (id, user_id, target, scan_type, status, created_at)
scan_results (id, job_id, finding_type, severity, description)
vulnerabilities (id, cve_id, title, severity, description)
```

#### Threat Intelligence
```sql
-- Threat intelligence data
ioc_indicators (id, type, value, source, confidence, created_at)
threat_actors (id, name, description, first_seen, last_seen)
attack_patterns (id, mitre_id, name, description, tactic)
```

#### System Operations
```sql
-- System logs and operations
system_logs (id, level, component, message, timestamp)
configurations (id, key, value, user_id, updated_at)
api_access_logs (id, user_id, endpoint, method, status, timestamp)
```

## Database Configuration

Database settings are configured in `config/database.yaml`:

```yaml
database:
  # Primary database configuration
  primary:
    type: "sqlite"           # sqlite, postgresql, mysql
    host: "localhost"        # For server-based databases
    port: 5432              # Database port
    name: "lewis_main"       # Database name
    file: "database/lewis_main.db"  # SQLite file path
    
  # Connection settings
  connection:
    pool_size: 10           # Connection pool size
    max_overflow: 20        # Maximum overflow connections
    timeout: 30             # Connection timeout
    
  # Performance settings
  performance:
    enable_query_cache: true
    slow_query_log: true
    slow_query_threshold: 1000  # ms
    
  # Backup settings
  backup:
    enabled: true
    schedule: "daily"
    retention: 30           # days
```

## Database Management

### Initialization
```bash
# Initialize new database
lewis db init

# Create database schema
lewis db create-schema

# Run database migrations
lewis db migrate

# Seed initial data
lewis db seed
```

### Maintenance
```bash
# Database health check
lewis db health

# Optimize database performance
lewis db optimize

# Vacuum and analyze (SQLite)
lewis db vacuum

# Backup database
lewis db backup

# Restore from backup
lewis db restore --backup <backup_file>
```

### Migration Management
```bash
# Create new migration
lewis db create-migration --name "add_new_feature"

# Apply pending migrations
lewis db migrate

# Rollback last migration
lewis db rollback

# Show migration status
lewis db migration-status
```

## Performance Optimization

### Indexing Strategy
- **Primary Keys**: All tables have optimized primary keys
- **Foreign Keys**: Proper foreign key indexes for relationships
- **Search Indexes**: Full-text search indexes for log analysis
- **Composite Indexes**: Multi-column indexes for complex queries
- **Partial Indexes**: Conditional indexes for filtered queries

### Query Optimization
- **Query Plans**: Regular analysis of query execution plans
- **Slow Query Monitoring**: Identification and optimization of slow queries
- **Connection Pooling**: Efficient database connection management
- **Prepared Statements**: Use of prepared statements for security and performance
- **Batch Operations**: Optimized batch inserts and updates

## Security Features

### Access Control
- **Database Users**: Separate database users with minimal privileges
- **Connection Security**: Encrypted database connections (TLS/SSL)
- **Authentication**: Strong authentication for database access
- **Authorization**: Role-based access control for database operations
- **Audit Logging**: Complete audit trail of database operations

### Data Protection
- **Encryption at Rest**: Database file encryption for sensitive data
- **Encryption in Transit**: Encrypted communication with database server
- **Password Hashing**: Secure password hashing with salt
- **Sensitive Data Masking**: PII and sensitive data protection
- **Backup Encryption**: Encrypted database backups

## Monitoring and Health

### Database Monitoring
- **Performance Metrics**: Query performance and resource utilization
- **Connection Monitoring**: Database connection health and usage
- **Storage Monitoring**: Database size and growth trends
- **Error Tracking**: Database errors and connection issues
- **Availability Monitoring**: Database uptime and responsiveness

### Health Checks
- **Connectivity Tests**: Regular database connectivity verification
- **Performance Tests**: Database performance benchmarking
- **Integrity Checks**: Data integrity and consistency verification
- **Backup Verification**: Regular backup integrity testing
- **Recovery Testing**: Periodic disaster recovery testing

## Backup and Recovery

### Backup Strategy
- **Automated Backups**: Scheduled database backups
- **Incremental Backups**: Efficient incremental backup strategy
- **Point-in-Time Recovery**: Transaction log-based recovery
- **Cross-Platform Backups**: Backups compatible across platforms
- **Offsite Storage**: Remote backup storage for disaster recovery

### Recovery Procedures
- **Full Recovery**: Complete database restoration from backup
- **Point-in-Time Recovery**: Recovery to specific timestamp
- **Selective Recovery**: Recovery of specific tables or data
- **Disaster Recovery**: Complete system recovery procedures
- **Testing**: Regular recovery testing and validation

## Migration and Upgrades

### Schema Migrations
- **Version Control**: Database schema version management
- **Automated Migrations**: Scripted database schema updates
- **Rollback Support**: Safe rollback of failed migrations
- **Testing**: Migration testing in development environment
- **Documentation**: Complete migration documentation

### Data Migration
- **Import Tools**: Tools for importing external data
- **Export Tools**: Data export in various formats
- **Transformation**: Data transformation and cleaning tools
- **Validation**: Data validation and integrity checking
- **Progress Tracking**: Migration progress monitoring

## Troubleshooting

### Common Issues
- **Connection Errors**: Database connection troubleshooting
- **Performance Issues**: Query optimization and tuning
- **Lock Contention**: Database locking and deadlock resolution
- **Storage Issues**: Database size and storage management
- **Corruption**: Database corruption detection and repair

### Diagnostic Tools
- **Log Analysis**: Database log file analysis
- **Performance Profiling**: Database performance profiling
- **Query Analysis**: SQL query analysis and optimization
- **Connection Debugging**: Database connection debugging
- **Health Monitoring**: Comprehensive database health monitoring

---

**Important**: This directory contains critical LEWIS operational data. Ensure proper backups and security measures are in place.

**LEWIS - Linux Environment Working Intelligence System**  
**© 2024 ZehraSec | Created by Yashab Alam**
