# LEWIS Configuration Guide

This guide covers all aspects of configuring LEWIS for optimal performance, security, and functionality in your environment.

## 📁 Configuration File Structure

LEWIS uses YAML configuration files organized hierarchically:

```
/etc/lewis/           # System-wide configuration
├── config.yaml       # Main configuration file
├── security.yaml     # Security-specific settings
├── tools.yaml        # Tool definitions and paths
├── users.yaml        # User accounts and permissions
└── ssl/              # SSL certificates and keys

~/.lewis/             # User-specific configuration
├── config.yaml       # User overrides
├── aliases.yaml      # Custom command aliases
├── scripts/          # Custom scripts
└── templates/        # Scan templates
```

## ⚙️ Core Configuration

### Main Configuration File

#### `/etc/lewis/config.yaml`
```yaml
# LEWIS Core Configuration
lewis:
  version: "1.0.0"
  instance_name: "LEWIS-Production"
  environment: "production"  # development, staging, production
  debug: false

# AI Engine Configuration
ai:
  # Language model settings
  model_name: "microsoft/DialoGPT-medium"
  model_cache_dir: "/var/cache/lewis/models"
  temperature: 0.7
  max_tokens: 512
  use_gpu: true
  gpu_memory_limit: "4GB"
  
  # Natural language processing
  nlp:
    language: "en"
    confidence_threshold: 0.8
    context_window: 10
    enable_entity_extraction: true
  
  # Learning and adaptation
  learning:
    enabled: true
    learning_rate: 0.001
    adaptation_frequency: "daily"
    feedback_collection: true

# Database Configuration
database:
  # Primary database
  primary:
    type: "mongodb"  # mongodb, postgresql, sqlite
    host: "localhost"
    port: 27017
    name: "lewis"
    username: "lewis"
    password: "${LEWIS_DB_PASSWORD}"
    auth_database: "admin"
    ssl_enabled: true
    ssl_cert_path: "/etc/lewis/ssl/mongodb.pem"
    connection_timeout: 30
    max_pool_size: 100
  
  # Cache database
  cache:
    type: "redis"
    host: "localhost"
    port: 6379
    password: "${LEWIS_REDIS_PASSWORD}"
    database: 0
    ssl_enabled: false
    max_connections: 50

# Security Configuration
security:
  # Authentication
  authentication:
    method: "jwt"  # jwt, ldap, oauth2, saml
    jwt_secret: "${LEWIS_JWT_SECRET}"
    jwt_expiration: 3600  # seconds
    jwt_refresh_enabled: true
    jwt_refresh_expiration: 86400
    
    # Multi-factor authentication
    mfa:
      enabled: true
      methods: ["totp", "sms"]  # totp, sms, email
      backup_codes: true
      grace_period: 86400
  
  # Authorization
  authorization:
    rbac_enabled: true
    default_role: "viewer"
    role_inheritance: true
    permission_cache_ttl: 3600
  
  # Session management
  session:
    timeout: 3600
    max_concurrent: 5
    secure_cookies: true
    same_site: "strict"
  
  # Password policy
  password_policy:
    min_length: 12
    require_uppercase: true
    require_lowercase: true
    require_numbers: true
    require_symbols: true
    prevent_reuse: 5
    expiration_days: 90

# Network Configuration
network:
  # Web server settings
  web:
    host: "0.0.0.0"
    port: 8000
    ssl_enabled: true
    ssl_cert_path: "/etc/lewis/ssl/server.crt"
    ssl_key_path: "/etc/lewis/ssl/server.key"
    ssl_protocols: ["TLSv1.2", "TLSv1.3"]
    
    # CORS settings
    cors:
      enabled: true
      origins: ["https://lewis.company.com"]
      credentials: true
    
    # Rate limiting
    rate_limiting:
      enabled: true
      requests_per_minute: 60
      burst_limit: 10
  
  # API settings
  api:
    version: "v1"
    prefix: "/api/v1"
    pagination:
      default_size: 20
      max_size: 100
    
    # API key authentication
    api_keys:
      enabled: true
      require_ip_whitelist: true
      rotation_interval: "30d"

# Scanning Configuration
scanning:
  # Default scan settings
  defaults:
    timeout: 300  # seconds
    max_concurrent: 10
    rate_limit: 100  # packets per second
    retry_attempts: 3
    retry_delay: 5
  
  # Network scanning
  network:
    ping_timeout: 5
    port_scan_timeout: 60
    service_detection: true
    os_detection: true
    script_scanning: true
  
  # Web scanning
  web:
    user_agent: "LEWIS Web Scanner 1.0"
    follow_redirects: true
    max_redirects: 5
    verify_ssl: false
    custom_headers: {}
  
  # Vulnerability scanning
  vulnerability:
    enabled: true
    update_frequency: "daily"
    severity_filter: ["high", "critical"]
    false_positive_learning: true

# Tool Configuration
tools:
  # Tool discovery
  auto_discovery: true
  discovery_paths: ["/usr/bin", "/usr/local/bin", "/opt"]
  
  # Tool execution
  execution:
    timeout: 300
    sandbox_enabled: true
    resource_limits:
      memory: "1GB"
      cpu_percent: 50
  
  # Tool updates
  updates:
    auto_update: false
    check_frequency: "weekly"
    source: "official"

# Logging Configuration
logging:
  # General logging
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "json"  # json, text
  output: "file"  # file, stdout, syslog
  
  # File logging
  file:
    path: "/var/log/lewis/lewis.log"
    max_size: "100MB"
    backup_count: 10
    rotation: "daily"
  
  # Audit logging
  audit:
    enabled: true
    file_path: "/var/log/lewis/audit.log"
    include_request_body: false
    include_response_body: false
  
  # Performance logging
  performance:
    enabled: true
    slow_query_threshold: 1000  # milliseconds
    metrics_collection: true

# Notification Configuration
notifications:
  # Email notifications
  email:
    enabled: true
    smtp_server: "smtp.company.com"
    smtp_port: 587
    smtp_username: "lewis@company.com"
    smtp_password: "${LEWIS_SMTP_PASSWORD}"
    smtp_tls: true
    from_address: "lewis@company.com"
    
    # Email templates
    templates:
      scan_complete: "/etc/lewis/templates/scan_complete.html"
      high_risk_finding: "/etc/lewis/templates/high_risk.html"
  
  # Slack notifications
  slack:
    enabled: true
    webhook_url: "${LEWIS_SLACK_WEBHOOK}"
    channel: "#security-alerts"
    mention_users: ["@security-team"]
  
  # Discord notifications
  discord:
    enabled: false
    webhook_url: "${LEWIS_DISCORD_WEBHOOK}"
  
  # SMS notifications
  sms:
    enabled: false
    provider: "twilio"  # twilio, aws_sns
    api_key: "${LEWIS_SMS_API_KEY}"

# Performance Configuration
performance:
  # Memory management
  memory:
    max_usage: "4GB"
    gc_threshold: 0.8
    cache_size: "1GB"
  
  # CPU optimization
  cpu:
    max_usage: 80  # percentage
    thread_pool_size: 20
    async_task_limit: 100
  
  # I/O optimization
  io:
    max_concurrent_scans: 10
    network_buffer_size: "64KB"
    disk_cache_size: "500MB"

# Backup Configuration
backup:
  # Automatic backups
  enabled: true
  frequency: "daily"
  retention_days: 30
  
  # Backup destinations
  destinations:
    local:
      enabled: true
      path: "/var/backups/lewis"
    
    s3:
      enabled: false
      bucket: "lewis-backups"
      region: "us-east-1"
      access_key: "${AWS_ACCESS_KEY}"
      secret_key: "${AWS_SECRET_KEY}"
  
  # What to backup
  include:
    - "database"
    - "configuration"
    - "user_data"
    - "logs"
  
  exclude:
    - "cache"
    - "temporary_files"
```

## 🔐 Security Configuration

### Security-Specific Settings

#### `/etc/lewis/security.yaml`
```yaml
# Advanced Security Configuration
security:
  # Encryption settings
  encryption:
    algorithm: "AES-256-GCM"
    key_rotation_interval: "90d"
    key_derivation: "PBKDF2"
    salt_length: 32
  
  # Access control
  access_control:
    # IP whitelist
    ip_whitelist:
      enabled: true
      allowed_ranges:
        - "192.168.0.0/16"
        - "10.0.0.0/8"
        - "172.16.0.0/12"
    
    # Geolocation filtering
    geo_filtering:
      enabled: false
      allowed_countries: ["US", "CA", "GB"]
      blocked_countries: ["CN", "RU", "KP"]
    
    # Time-based access
    time_restrictions:
      enabled: false
      allowed_hours: "09:00-17:00"
      timezone: "UTC"
  
  # Intrusion detection
  intrusion_detection:
    enabled: true
    failed_login_threshold: 5
    lockout_duration: 1800  # seconds
    monitoring_window: 300
    
    # Suspicious activity detection
    anomaly_detection:
      enabled: true
      baseline_learning_period: "7d"
      sensitivity: "medium"  # low, medium, high
  
  # Data loss prevention
  dlp:
    enabled: true
    scan_uploads: true
    block_sensitive_data: true
    patterns:
      - "credit_card"
      - "ssn"
      - "api_keys"
  
  # Compliance
  compliance:
    pci_dss: true
    hipaa: false
    gdpr: true
    sox: false
```

### SSL/TLS Configuration

#### Certificate Management
```bash
# Generate self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
  -keyout /etc/lewis/ssl/server.key \
  -out /etc/lewis/ssl/server.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=lewis.company.com"

# Set proper permissions
sudo chmod 600 /etc/lewis/ssl/server.key
sudo chmod 644 /etc/lewis/ssl/server.crt
sudo chown lewis:lewis /etc/lewis/ssl/*
```

#### Let's Encrypt Integration
```yaml
# SSL automation
ssl:
  provider: "letsencrypt"
  email: "admin@company.com"
  domains: ["lewis.company.com"]
  auto_renewal: true
  renewal_days_before: 30
```

## 🛠️ Tool Configuration

### Tool Definitions

#### `/etc/lewis/tools.yaml`
```yaml
# Tool Configuration
tools:
  # Network scanners
  nmap:
    name: "Nmap"
    category: "network_scanner"
    path: "/usr/bin/nmap"
    version_command: "--version"
    enabled: true
    default_args: ["-sS", "-sV"]
    timeout: 300
    output_format: "xml"
    
    # Custom options
    options:
      stealth_mode: true
      service_detection: true
      os_detection: false
      script_scanning: false
  
  masscan:
    name: "Masscan"
    category: "network_scanner"
    path: "/usr/bin/masscan"
    enabled: true
    default_args: ["--rate", "1000"]
    timeout: 600
    
    options:
      max_rate: 10000
      exclude_ports: [1900, 5353]
  
  # Web scanners
  nikto:
    name: "Nikto"
    category: "web_scanner"
    path: "/usr/bin/nikto"
    enabled: true
    timeout: 1800
    output_format: "xml"
    
    options:
      follow_redirects: true
      ssl_verify: false
      max_scan_time: 3600
  
  sqlmap:
    name: "SQLMap"
    category: "web_scanner"
    path: "/usr/bin/sqlmap"
    enabled: true
    timeout: 3600
    
    options:
      risk_level: 1
      level: 1
      threads: 5
      batch_mode: true
  
  # Vulnerability scanners
  nuclei:
    name: "Nuclei"
    category: "vulnerability_scanner"
    path: "/usr/bin/nuclei"
    enabled: true
    timeout: 1800
    
    options:
      template_path: "/opt/nuclei-templates"
      rate_limit: 150
      bulk_size: 25
      retries: 1

# Tool categories
categories:
  network_scanner:
    description: "Network discovery and port scanning tools"
    icon: "network-wired"
    color: "#4CAF50"
  
  web_scanner:
    description: "Web application security testing tools"
    icon: "globe"
    color: "#2196F3"
  
  vulnerability_scanner:
    description: "Vulnerability assessment and detection tools"
    icon: "shield-alt"
    color: "#FF9800"
  
  information_gathering:
    description: "Reconnaissance and information gathering tools"
    icon: "search"
    color: "#9C27B0"

# Tool presets
presets:
  quick_scan:
    name: "Quick Network Scan"
    tools: ["nmap"]
    options:
      nmap:
        args: ["-sS", "-T4", "--top-ports", "1000"]
  
  comprehensive_scan:
    name: "Comprehensive Security Scan"
    tools: ["nmap", "nikto", "nuclei"]
    options:
      nmap:
        args: ["-sS", "-sV", "-sC", "-O"]
      parallel_execution: false
  
  web_assessment:
    name: "Web Application Assessment"
    tools: ["nikto", "sqlmap", "dirb"]
    options:
      sequential: true
      timeout: 7200
```

## 👥 User Management

### User Configuration

#### `/etc/lewis/users.yaml`
```yaml
# User Management Configuration
users:
  # User authentication
  authentication:
    password_hashing: "bcrypt"
    hash_rounds: 12
    session_management: "jwt"
  
  # Default roles
  roles:
    administrator:
      name: "Administrator"
      description: "Full system access"
      permissions:
        - "*"  # All permissions
      
    security_analyst:
      name: "Security Analyst"
      description: "Security testing and analysis"
      permissions:
        - "scan:*"
        - "report:*"
        - "tools:use"
        - "dashboard:view"
      
    junior_analyst:
      name: "Junior Analyst"
      description: "Limited security testing"
      permissions:
        - "scan:network"
        - "scan:web:basic"
        - "report:view"
        - "dashboard:view"
      
    viewer:
      name: "Viewer"
      description: "Read-only access"
      permissions:
        - "report:view"
        - "dashboard:view"
    
    auditor:
      name: "Auditor"
      description: "Audit and compliance access"
      permissions:
        - "audit:view"
        - "logs:view"
        - "compliance:*"
        - "report:view"

  # Permission definitions
  permissions:
    scan:
      network: "Perform network scans"
      web: "Perform web application scans"
      vulnerability: "Perform vulnerability scans"
      "*": "All scanning operations"
    
    report:
      view: "View reports"
      create: "Create reports"
      delete: "Delete reports"
      export: "Export reports"
      "*": "All report operations"
    
    tools:
      use: "Use security tools"
      configure: "Configure tools"
      install: "Install new tools"
      "*": "All tool operations"
    
    system:
      configure: "Configure system settings"
      backup: "Create system backups"
      update: "Update system"
      "*": "All system operations"
    
    user:
      view: "View user information"
      create: "Create users"
      modify: "Modify users"
      delete: "Delete users"
      "*": "All user operations"

  # Account policies
  account_policies:
    lockout:
      enabled: true
      failed_attempts: 5
      lockout_duration: 1800
      reset_attempts_after: 3600
    
    password_expiration:
      enabled: true
      max_age_days: 90
      warning_days: 14
      grace_logins: 3
    
    session_limits:
      max_concurrent_sessions: 3
      idle_timeout: 1800
      absolute_timeout: 28800
```

### Creating Users

#### Command Line User Management
```bash
# Create administrator
lewis user create admin \
  --role administrator \
  --email admin@company.com \
  --full-name "System Administrator"

# Create security analyst
lewis user create analyst1 \
  --role security_analyst \
  --email analyst1@company.com \
  --full-name "Security Analyst"

# Set password (will prompt securely)
lewis user password admin
lewis user password analyst1

# Enable two-factor authentication
lewis user 2fa enable analyst1

# Set account expiration
lewis user expire analyst1 --days 90
```

#### Bulk User Import
```yaml
# users_import.yaml
users:
  - username: "john.doe"
    email: "john.doe@company.com"
    full_name: "John Doe"
    role: "security_analyst"
    department: "Security"
    
  - username: "jane.smith"
    email: "jane.smith@company.com"
    full_name: "Jane Smith"
    role: "junior_analyst"
    department: "Security"
```

```bash
# Import users
lewis user import users_import.yaml
```

## 🔧 Advanced Configuration

### Environment-Specific Configuration

#### Development Environment
```yaml
# config/development.yaml
lewis:
  environment: "development"
  debug: true

database:
  primary:
    name: "lewis_dev"
    host: "localhost"

security:
  authentication:
    jwt_expiration: 86400  # Longer sessions for development

logging:
  level: "DEBUG"
  output: "stdout"
```

#### Production Environment
```yaml
# config/production.yaml
lewis:
  environment: "production"
  debug: false

database:
  primary:
    name: "lewis_prod"
    host: "prod-db.company.com"
    ssl_enabled: true

security:
  authentication:
    mfa:
      enabled: true
    jwt_expiration: 3600

logging:
  level: "INFO"
  audit:
    enabled: true
```

### Configuration Management

#### Environment Variables
```bash
# Required environment variables
export LEWIS_DB_PASSWORD="secure_database_password"
export LEWIS_JWT_SECRET="32_character_random_string"
export LEWIS_REDIS_PASSWORD="redis_password"
export LEWIS_SMTP_PASSWORD="email_password"

# Optional environment variables
export LEWIS_CONFIG_PATH="/etc/lewis/config.yaml"
export LEWIS_LOG_LEVEL="INFO"
export LEWIS_DEBUG="false"
```

#### Configuration Validation
```bash
# Validate configuration files
lewis config validate

# Check specific configuration section
lewis config validate --section security

# Test database connection
lewis config test database

# Verify tool paths
lewis config test tools
```

#### Configuration Backup and Restore
```bash
# Backup configuration
lewis config backup /backup/lewis-config-$(date +%Y%m%d).tar.gz

# Restore configuration
lewis config restore /backup/lewis-config-20250621.tar.gz

# Compare configurations
lewis config diff current /backup/lewis-config-20250621.tar.gz
```

### Performance Tuning

#### Database Optimization
```yaml
database:
  primary:
    # Connection pooling
    min_pool_size: 5
    max_pool_size: 100
    connection_timeout: 30
    
    # Query optimization
    query_timeout: 60
    bulk_write_size: 1000
    
    # Indexing
    auto_indexing: true
    index_background: true
```

#### Memory Management
```yaml
performance:
  memory:
    # JVM-style memory management
    initial_heap: "1GB"
    max_heap: "4GB"
    
    # Garbage collection
    gc_algorithm: "G1GC"
    gc_threads: 4
    
    # Cache tuning
    cache_size: "1GB"
    cache_ttl: 3600
```

#### Network Optimization
```yaml
network:
  # Connection limits
  max_connections: 1000
  connection_timeout: 30
  
  # Buffer sizes
  send_buffer: "64KB"
  receive_buffer: "64KB"
  
  # Keep-alive settings
  keep_alive: true
  keep_alive_timeout: 60
```

## 📊 Monitoring Configuration

### Metrics Collection
```yaml
monitoring:
  metrics:
    enabled: true
    collection_interval: 60  # seconds
    retention_days: 30
    
    # Prometheus integration
    prometheus:
      enabled: true
      port: 9090
      endpoint: "/metrics"
    
    # Custom metrics
    custom_metrics:
      - name: "scans_per_hour"
        type: "counter"
      - name: "scan_duration"
        type: "histogram"
      - name: "active_users"
        type: "gauge"

  # Health checks
  health:
    enabled: true
    endpoint: "/health"
    checks:
      - "database"
      - "cache"
      - "tools"
      - "ai_engine"
```

### Alerting Configuration
```yaml
alerting:
  # Alert conditions
  conditions:
    high_error_rate:
      metric: "error_rate"
      threshold: 5  # percentage
      duration: "5m"
      severity: "warning"
    
    database_down:
      metric: "database_status"
      condition: "down"
      severity: "critical"
      immediate: true
    
    disk_space_low:
      metric: "disk_usage"
      threshold: 90  # percentage
      severity: "warning"
  
  # Alert destinations
  destinations:
    email:
      enabled: true
      recipients: ["admin@company.com"]
    
    slack:
      enabled: true
      channel: "#alerts"
    
    pagerduty:
      enabled: false
      service_key: "${PAGERDUTY_SERVICE_KEY}"
```

## 🔄 Configuration Updates

### Dynamic Configuration Updates
```bash
# Reload configuration without restart
lewis config reload

# Update specific configuration section
lewis config update security.session.timeout 7200

# Apply configuration changes
lewis config apply
```

### Configuration Versioning
```bash
# Show configuration history
lewis config history

# Rollback to previous version
lewis config rollback --version 1.2.3

# Create configuration checkpoint
lewis config checkpoint "before_security_update"
```

### Configuration Templates
```yaml
# templates/high_security.yaml
security:
  authentication:
    mfa:
      enabled: true
      methods: ["totp"]
    jwt_expiration: 1800
  
  encryption:
    algorithm: "AES-256-GCM"
    key_rotation_interval: "30d"
```

```bash
# Apply configuration template
lewis config template apply high_security
```

---

**📝 Configuration Guide Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)
