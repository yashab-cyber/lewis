# LEWIS Debugging Guide

This comprehensive guide covers debugging techniques, diagnostic tools, and troubleshooting methods for LEWIS.

## 🔍 Debug Mode Overview

LEWIS provides extensive debugging capabilities to help identify and resolve issues quickly.

### Enabling Debug Mode

#### Global Debug Mode
```bash
# Enable debug mode for current session
lewis --debug

# Enable debug mode permanently
lewis config set debug true

# Set debug level
lewis config set logging.level DEBUG
```

#### Component-Specific Debugging
```bash
# Debug specific components
lewis --debug-ai          # AI engine debugging
lewis --debug-database    # Database operations
lewis --debug-tools       # Tool execution
lewis --debug-network     # Network operations
lewis --debug-security    # Security operations
```

#### Environment Variable Debug
```bash
# Enable debug via environment variable
export LEWIS_DEBUG=true
export LEWIS_LOG_LEVEL=DEBUG

# Start LEWIS
lewis
```

## 🛠️ Diagnostic Tools

### System Diagnostics

#### Comprehensive System Check
```bash
# Full system diagnostic
lewis diagnostics --full

# Component-specific diagnostics
lewis diagnostics --component ai
lewis diagnostics --component database
lewis diagnostics --component tools
lewis diagnostics --component network
lewis diagnostics --component security

# Performance diagnostics
lewis diagnostics --performance

# Health check with detailed output
lewis --health-check --verbose
```

#### Expected Output
```
LEWIS System Diagnostics
========================

Core System:
✅ LEWIS Core Engine: Operational (v1.0.0)
✅ Python Version: 3.9.7 (Compatible)
✅ Operating System: Ubuntu 20.04.3 LTS
✅ Memory Usage: 2.1GB / 8GB (26%)
✅ Disk Space: 45GB / 100GB available

AI Engine:
✅ AI Engine: Ready
✅ NLP Models: Loaded (microsoft/DialoGPT-medium)
✅ GPU Support: Available (CUDA 11.2)
✅ Model Cache: 1.2GB / 2GB used

Database:
✅ MongoDB: Connected (5.0.9)
✅ Database: lewis (47MB, 3 collections)
✅ Redis Cache: Connected (6.2.4)
✅ Connection Pool: 5/50 active

Tools:
✅ Tool Discovery: 47 tools found
✅ Tool Verification: 45/47 operational
⚠️  Missing Tools: masscan, zmap
✅ Tool Updates: All tools current

Network:
✅ Network Connectivity: Available
✅ DNS Resolution: Functional
✅ SSL/TLS: Configured (TLS 1.3)
✅ Firewall: Properly configured

Security:
✅ Authentication: JWT enabled
✅ Authorization: RBAC active
✅ Encryption: AES-256-GCM
✅ Audit Logging: Enabled
```

### Performance Monitoring

#### Real-time Performance Metrics
```bash
# Monitor system performance
lewis monitor --real-time

# Monitor specific components
lewis monitor --component ai --interval 5
lewis monitor --component database --duration 300

# Export performance data
lewis monitor --export performance_data.json
```

#### Performance Profiling
```bash
# Profile scan performance
lewis profile scan 192.168.1.0/24

# Profile AI processing
lewis profile ai "scan the network for vulnerabilities"

# Profile database operations
lewis profile database --operation insert
```

### Network Diagnostics

#### Network Connectivity Testing
```bash
# Test network connectivity
lewis network test

# Test specific endpoints
lewis network test --target google.com
lewis network test --target 192.168.1.1 --port 22

# DNS resolution testing
lewis network dns --domain example.com
lewis network dns --server 8.8.8.8
```

#### Network Configuration Validation
```bash
# Validate network configuration
lewis network config validate

# Test firewall rules
lewis network firewall test

# Check port accessibility
lewis network ports check --local
lewis network ports scan --target 192.168.1.1
```

## 📊 Logging and Log Analysis

### Log Configuration

#### Debug Logging Setup
```yaml
# config/debug.yaml
logging:
  level: "DEBUG"
  format: "detailed"  # detailed, json, simple
  output: "file"
  
  # File configuration
  file:
    path: "/var/log/lewis/debug.log"
    max_size: "500MB"
    backup_count: 20
    rotation: "hourly"
  
  # Component-specific logging
  components:
    ai_engine:
      level: "DEBUG"
      file: "/var/log/lewis/ai_debug.log"
    
    database:
      level: "DEBUG"
      file: "/var/log/lewis/database_debug.log"
    
    tools:
      level: "DEBUG"
      file: "/var/log/lewis/tools_debug.log"
```

#### Real-time Log Monitoring
```bash
# Tail all logs
lewis logs tail

# Tail specific component logs
lewis logs tail --component ai
lewis logs tail --component database

# Filter logs by level
lewis logs tail --level ERROR
lewis logs tail --level WARNING --level ERROR

# Search logs
lewis logs search "connection timeout"
lewis logs search --regex "error.*database"
```

### Log Analysis Tools

#### Log Parsing and Analysis
```bash
# Analyze error patterns
lewis logs analyze --errors --since "1 hour"

# Performance analysis
lewis logs analyze --performance --since "1 day"

# Generate log summary
lewis logs summary --since "1 week"

# Export logs for external analysis
lewis logs export --format json --output logs_export.json
```

#### Common Log Patterns
```bash
# Database connection issues
lewis logs search "database.*connection.*failed"

# AI model loading problems
lewis logs search "model.*load.*error"

# Tool execution failures
lewis logs search "tool.*execution.*failed"

# Security-related events
lewis logs search "authentication.*failed|authorization.*denied"
```

## 🔧 Component-Specific Debugging

### AI Engine Debugging

#### AI Engine Diagnostics
```bash
# Test AI engine functionality
lewis ai test

# Test natural language processing
lewis ai nlp test "scan the network for vulnerabilities"

# Model performance testing
lewis ai model test --input "test query"

# Check model cache
lewis ai cache status
```

#### AI Debug Output
```bash
# Enable verbose AI debugging
lewis --debug-ai --verbose

# AI processing trace
lewis ai trace "perform security scan of 192.168.1.100"
```

Expected debug output:
```
[DEBUG] AI Engine: Processing input: "perform security scan of 192.168.1.100"
[DEBUG] NLP: Tokenizing input...
[DEBUG] NLP: Tokens: ['perform', 'security', 'scan', 'of', '192.168.1.100']
[DEBUG] Intent Recognition: Identified intent: SECURITY_SCAN
[DEBUG] Entity Extraction: Found entities: IP_ADDRESS=192.168.1.100
[DEBUG] Command Generation: nmap -sS -sV 192.168.1.100
[DEBUG] Tool Selection: Selected tool: nmap
[DEBUG] Execution: Starting nmap scan...
```

### Database Debugging

#### Database Connection Testing
```bash
# Test database connectivity
lewis database test

# Connection pool status
lewis database pool status

# Query performance testing
lewis database query test

# Database migration status
lewis database migration status
```

#### Database Query Debugging
```bash
# Enable query logging
lewis config set database.query_logging true

# Slow query analysis
lewis database slow-queries --threshold 1000

# Connection debugging
lewis database connections debug
```

### Tool Execution Debugging

#### Tool Debugging
```bash
# Test individual tools
lewis tools test nmap
lewis tools test --all

# Tool execution tracing
lewis tools trace nmap -sS 192.168.1.1

# Tool output debugging
lewis tools debug nmap --target 192.168.1.1 --verbose
```

#### Tool Execution Environment
```bash
# Check tool environment
lewis tools env

# Verify tool permissions
lewis tools permissions check

# Tool sandbox testing
lewis tools sandbox test
```

## 🚨 Error Handling and Recovery

### Common Error Categories

#### 1. Configuration Errors
```bash
# Invalid configuration
ERROR: Invalid configuration in /etc/lewis/config.yaml
Line 45: Invalid value for 'database.port': 'invalid_port'

# Debug configuration issues
lewis config validate --verbose
lewis config test --component database
```

#### 2. Authentication Errors
```bash
# Authentication failures
ERROR: Authentication failed for user 'analyst'
Reason: Invalid credentials

# Debug authentication
lewis auth debug --user analyst
lewis auth test --method jwt
```

#### 3. Network Errors
```bash
# Network connectivity issues
ERROR: Network unreachable: 192.168.1.100
Timeout: Connection timeout after 30 seconds

# Debug network issues
lewis network debug --target 192.168.1.100
lewis network trace --target 192.168.1.100
```

#### 4. Tool Execution Errors
```bash
# Tool execution failures
ERROR: Tool execution failed: nmap
Exit code: 1
Error: Permission denied

# Debug tool issues
lewis tools debug nmap --verbose
lewis tools permissions fix nmap
```

### Error Recovery Procedures

#### Automatic Recovery
```yaml
# config/recovery.yaml
recovery:
  # Database connection recovery
  database:
    auto_reconnect: true
    max_retries: 5
    retry_delay: 5  # seconds
    
  # Tool execution recovery
  tools:
    retry_on_failure: true
    max_retries: 3
    retry_delay: 2
    
  # Network operation recovery
  network:
    retry_on_timeout: true
    max_retries: 3
    backoff_factor: 2
```

#### Manual Recovery
```bash
# Reset component states
lewis reset --component database
lewis reset --component ai
lewis reset --component tools

# Clear caches
lewis cache clear --all
lewis cache clear --component ai

# Repair corrupted data
lewis repair --database
lewis repair --configuration
```

## 🔬 Advanced Debugging Techniques

### Memory Debugging

#### Memory Usage Analysis
```bash
# Monitor memory usage
lewis debug memory --monitor

# Memory leak detection
lewis debug memory --leak-detection

# Garbage collection analysis
lewis debug memory --gc-analysis

# Memory dump for analysis
lewis debug memory --dump memory_dump.hprof
```

#### Memory Optimization
```bash
# Optimize memory usage
lewis optimize memory

# Clear memory caches
lewis memory clear-cache

# Adjust memory limits
lewis config set performance.memory.max_usage "6GB"
```

### CPU Profiling

#### CPU Performance Analysis
```bash
# CPU profiling
lewis profile cpu --duration 60

# Thread analysis
lewis debug threads

# CPU bottleneck identification
lewis debug cpu --bottlenecks

# Performance optimization suggestions
lewis optimize cpu
```

### Database Debugging

#### Query Analysis
```bash
# Slow query identification
lewis database slow-queries --top 10

# Query execution plan analysis
lewis database explain --query "scan_results"

# Index usage analysis
lewis database indexes analyze

# Database optimization
lewis database optimize
```

#### Connection Pool Debugging
```bash
# Connection pool status
lewis database pool status

# Connection leaks detection
lewis database pool debug --leaks

# Connection pool optimization
lewis database pool optimize
```

## 🧪 Testing and Validation

### Unit Testing

#### Component Testing
```bash
# Test individual components
lewis test ai
lewis test database
lewis test tools
lewis test security

# Integration testing
lewis test integration

# End-to-end testing
lewis test e2e
```

#### Custom Test Cases
```bash
# Create custom test
lewis test create --name "network_scan_test" --type integration

# Run specific test
lewis test run network_scan_test

# Test report generation
lewis test report --format html
```

### Performance Testing

#### Load Testing
```bash
# Simulate concurrent users
lewis load-test --users 50 --duration 300

# Scan performance testing
lewis load-test scan --concurrent 10

# API endpoint testing
lewis load-test api --endpoint "/api/v1/scan" --requests 1000
```

#### Stress Testing
```bash
# Memory stress testing
lewis stress-test memory --duration 600

# CPU stress testing
lewis stress-test cpu --cores 4

# Database stress testing
lewis stress-test database --connections 100
```

## 📋 Debugging Checklists

### Pre-Debug Checklist
- [ ] Collect error messages and timestamps
- [ ] Note system resources (CPU, memory, disk)
- [ ] Check recent configuration changes
- [ ] Review system logs for patterns
- [ ] Verify network connectivity
- [ ] Check service status

### Debug Process Checklist
- [ ] Enable appropriate debug modes
- [ ] Reproduce the issue
- [ ] Collect debug logs
- [ ] Analyze log patterns
- [ ] Test individual components
- [ ] Validate configuration
- [ ] Check dependencies

### Post-Debug Checklist
- [ ] Document the issue and resolution
- [ ] Update monitoring if needed
- [ ] Review configuration for optimization
- [ ] Create preventive measures
- [ ] Update documentation
- [ ] Disable debug mode if not needed

## 🛡️ Security Debug Considerations

### Sensitive Information Handling

#### Debug Data Sanitization
```yaml
# debug.yaml
debug:
  sanitization:
    enabled: true
    sensitive_fields:
      - "password"
      - "api_key"
      - "token"
      - "secret"
    
    # Mask patterns
    masking:
      credit_card: "****-****-****-####"
      ssn: "***-**-####"
      api_key: "****...####"
```

#### Secure Debug Sessions
```bash
# Start secure debug session
lewis debug --secure --encrypt-logs

# Debug with user context
lewis debug --as-user analyst --permissions-check

# Audit debug activities
lewis debug --audit --session-id DEBUG_001
```

## 📞 Getting Debug Help

### Debug Information Collection

#### Automatic Debug Report
```bash
# Generate comprehensive debug report
lewis debug report --full

# Anonymized debug report for support
lewis debug report --anonymize --output debug_report.zip
```

#### Debug Report Contents
- System information and configuration
- Component status and health checks
- Recent error logs and patterns
- Performance metrics
- Network configuration
- Security status

### Community Debug Support

#### Debug Information Sharing
```bash
# Create shareable debug info (anonymized)
lewis debug share --create-link

# Submit debug report to support
lewis debug submit --ticket-id 12345
```

#### Support Channels
- 📧 **Email**: yashabalam707@gmail.com
- 💬 **Discord**: [ZehraSec Community](https://discord.gg/zehrasec)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yashab-cyber/lewis/issues)
- 📖 **Documentation**: [docs.lewis-security.com](https://docs.lewis-security.com)

### Debug Documentation

#### Contributing Debug Information
```bash
# Add debug information to docs
lewis debug docs contribute

# Update troubleshooting guide
lewis debug docs update
```

---

**📝 Debugging Guide Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)
