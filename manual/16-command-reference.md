# LEWIS Command Reference

Complete reference for all LEWIS commands, options, and parameters.

## 📖 Overview

This reference provides comprehensive documentation for all LEWIS command-line interface (CLI) commands, web interface actions, and API endpoints.

## 📋 Table of Contents

1. [Core Commands](#core-commands)
2. [Scanning Commands](#scanning-commands)
3. [Analysis Commands](#analysis-commands)
4. [Reporting Commands](#reporting-commands)
5. [Configuration Commands](#configuration-commands)
6. [System Commands](#system-commands)
7. [Utility Commands](#utility-commands)
8. [Advanced Commands](#advanced-commands)

## 🔧 Core Commands

### `lewis` - Main Command

**Usage:** `python lewis.py [OPTIONS] [COMMAND]`

**Description:** Main LEWIS command entry point.

**Global Options:**
```bash
--config, -c        Configuration file path
--verbose, -v       Enable verbose output
--quiet, -q         Suppress output
--debug            Enable debug mode
--log-level        Set logging level (DEBUG, INFO, WARNING, ERROR)
--output, -o       Output file path
--format, -f       Output format (json, xml, csv, html)
--help, -h         Show help message
--version          Show version information
```

**Examples:**
```bash
# Basic usage
python lewis.py --help

# Run with custom config
python lewis.py -c /path/to/config.yaml

# Enable debug mode
python lewis.py --debug --log-level DEBUG
```

### `init` - Initialize LEWIS

**Usage:** `python lewis.py init [OPTIONS]`

**Description:** Initialize LEWIS configuration and setup.

**Options:**
```bash
--config-dir       Configuration directory (default: ./config)
--force           Force initialization (overwrite existing)
--template        Use configuration template
--interactive     Interactive setup mode
```

**Examples:**
```bash
# Initialize with defaults
python lewis.py init

# Interactive setup
python lewis.py init --interactive

# Force reinitialize
python lewis.py init --force
```

## 🔍 Scanning Commands

### `scan` - Perform Security Scan

**Usage:** `python lewis.py scan [OPTIONS] TARGET`

**Description:** Perform security scan on specified target.

**Options:**
```bash
--type, -t         Scan type (full, quick, custom, vulnerability)
--profile, -p      Scan profile (web, network, host, api)
--threads          Number of threads (default: 10)
--timeout          Scan timeout in seconds
--exclude          Exclude patterns/ports
--include          Include patterns/ports
--rate-limit       Rate limiting (requests per second)
--user-agent       Custom user agent string
--cookies          Cookie file or string
--headers          Custom HTTP headers
--proxy            Proxy configuration
--output-dir       Output directory for results
--no-cache         Disable caching
--resume           Resume previous scan
```

**Scan Types:**
- `full` - Comprehensive security scan
- `quick` - Fast vulnerability scan
- `custom` - User-defined scan parameters
- `vulnerability` - Focus on vulnerability detection
- `compliance` - Compliance-focused scan

**Scan Profiles:**
- `web` - Web application scanning
- `network` - Network infrastructure scanning
- `host` - Host-based scanning
- `api` - API security scanning
- `mobile` - Mobile application scanning

**Examples:**
```bash
# Full scan of web application
python lewis.py scan --type full --profile web https://example.com

# Quick network scan
python lewis.py scan --type quick --profile network 192.168.1.0/24

# Custom scan with specific options
python lewis.py scan --type custom --threads 20 --timeout 300 example.com

# Scan with proxy
python lewis.py scan --proxy http://proxy:8080 https://example.com

# Resume previous scan
python lewis.py scan --resume scan_id_12345
```

### `multi-scan` - Multiple Target Scanning

**Usage:** `python lewis.py multi-scan [OPTIONS] [TARGETS...]`

**Description:** Scan multiple targets simultaneously.

**Options:**
```bash
--input-file, -i   File containing target list
--max-concurrent   Maximum concurrent scans
--batch-size       Batch processing size
--delay           Delay between batches (seconds)
--continue-on-error Continue on individual scan failures
```

**Examples:**
```bash
# Scan multiple targets
python lewis.py multi-scan site1.com site2.com site3.com

# Scan from file
python lewis.py multi-scan -i targets.txt --max-concurrent 5

# Batch processing
python lewis.py multi-scan -i large_targets.txt --batch-size 10 --delay 30
```

### `scheduled-scan` - Schedule Scans

**Usage:** `python lewis.py scheduled-scan [OPTIONS] SCHEDULE TARGET`

**Description:** Schedule recurring scans.

**Options:**
```bash
--name            Schedule name
--description     Schedule description
--type            Scan type
--profile         Scan profile
--enabled         Enable schedule (default: true)
--notification    Notification settings
```

**Schedule Formats:**
- Cron format: `"0 2 * * *"` (daily at 2 AM)
- Interval: `"every 6h"` (every 6 hours)
- Specific: `"2023-12-25 10:00"` (one-time)

**Examples:**
```bash
# Daily scan at 2 AM
python lewis.py scheduled-scan "0 2 * * *" https://example.com

# Weekly scan on Sundays
python lewis.py scheduled-scan "0 2 * * 0" --name "Weekly Scan" example.com

# Hourly quick scans
python lewis.py scheduled-scan "0 * * * *" --type quick example.com
```

## 📊 Analysis Commands

### `analyze` - Analyze Scan Results

**Usage:** `python lewis.py analyze [OPTIONS] SCAN_ID_OR_FILE`

**Description:** Analyze and process scan results.

**Options:**
```bash
--format          Output format (json, html, pdf, xml)
--filter          Filter by severity/type
--sort            Sort results
--limit           Limit number of results
--include-details Include detailed information
--risk-threshold  Risk threshold for filtering
--compliance      Compliance framework analysis
```

**Examples:**
```bash
# Analyze specific scan
python lewis.py analyze scan_12345

# Analyze with filtering
python lewis.py analyze --filter "severity:high" --sort "risk_score" scan_12345

# Compliance analysis
python lewis.py analyze --compliance "OWASP" scan_12345

# Export to PDF
python lewis.py analyze --format pdf --output report.pdf scan_12345
```

### `compare` - Compare Scan Results

**Usage:** `python lewis.py compare [OPTIONS] SCAN1 SCAN2`

**Description:** Compare two scan results to identify changes.

**Options:**
```bash
--format          Output format
--show-new        Show only new findings
--show-fixed      Show only fixed findings
--show-changed    Show changed findings
--baseline        Set baseline scan
```

**Examples:**
```bash
# Compare two scans
python lewis.py compare scan_12345 scan_12346

# Show only new issues
python lewis.py compare --show-new scan_12345 scan_12346

# Set baseline for future comparisons
python lewis.py compare --baseline scan_12345
```

### `trend` - Trend Analysis

**Usage:** `python lewis.py trend [OPTIONS] TARGET`

**Description:** Analyze security trends over time.

**Options:**
```bash
--period          Time period (days, weeks, months)
--metric          Metric to analyze
--chart-type      Chart type (line, bar, pie)
--export          Export chart image
```

**Examples:**
```bash
# Weekly trend analysis
python lewis.py trend --period "30 days" --metric "vulnerabilities" example.com

# Export trend chart
python lewis.py trend --period "3 months" --export trend.png example.com
```

## 📋 Reporting Commands

### `report` - Generate Reports

**Usage:** `python lewis.py report [OPTIONS] TEMPLATE SCAN_ID`

**Description:** Generate reports from scan results.

**Options:**
```bash
--template, -t    Report template
--format          Output format (html, pdf, docx, json)
--output, -o      Output file path
--include         Sections to include
--exclude         Sections to exclude
--branding        Custom branding
--language        Report language
```

**Report Templates:**
- `executive` - Executive summary report
- `technical` - Technical detailed report
- `compliance` - Compliance-focused report
- `trend` - Trend analysis report
- `custom` - Custom template

**Examples:**
```bash
# Generate executive report
python lewis.py report executive scan_12345 --format pdf

# Technical report with branding
python lewis.py report technical scan_12345 --branding company_logo.png

# Compliance report
python lewis.py report compliance scan_12345 --include "SOC2,GDPR"

# Custom report template
python lewis.py report custom scan_12345 --template custom_template.html
```

### `export` - Export Data

**Usage:** `python lewis.py export [OPTIONS] DATA_TYPE`

**Description:** Export various data types from LEWIS.

**Options:**
```bash
--format          Export format
--filter          Data filter criteria
--date-range      Date range for export
--include-raw     Include raw scan data
```

**Data Types:**
- `scans` - Scan results
- `findings` - Security findings
- `targets` - Target information
- `reports` - Generated reports
- `configs` - Configuration data

**Examples:**
```bash
# Export all scans as JSON
python lewis.py export scans --format json

# Export high-severity findings
python lewis.py export findings --filter "severity:high" --format csv

# Export data for date range
python lewis.py export scans --date-range "2023-01-01:2023-12-31"
```

## ⚙️ Configuration Commands

### `config` - Configuration Management

**Usage:** `python lewis.py config [OPTIONS] [COMMAND]`

**Description:** Manage LEWIS configuration.

**Subcommands:**
```bash
show              Show current configuration
set               Set configuration value
get               Get configuration value
list              List all configuration keys
validate          Validate configuration
backup            Backup configuration
restore           Restore configuration
reset             Reset to defaults
```

**Examples:**
```bash
# Show current configuration
python lewis.py config show

# Set configuration value
python lewis.py config set scanning.max_threads 20

# Get specific value
python lewis.py config get database.host

# Validate configuration
python lewis.py config validate

# Backup configuration
python lewis.py config backup --output config_backup.yaml
```

### `plugin` - Plugin Management

**Usage:** `python lewis.py plugin [OPTIONS] [COMMAND]`

**Description:** Manage LEWIS plugins.

**Subcommands:**
```bash
list              List installed plugins
install           Install plugin
uninstall         Uninstall plugin
enable            Enable plugin
disable           Disable plugin
update            Update plugin
info              Show plugin information
```

**Examples:**
```bash
# List all plugins
python lewis.py plugin list

# Install plugin
python lewis.py plugin install plugin_name

# Enable/disable plugin
python lewis.py plugin enable plugin_name
python lewis.py plugin disable plugin_name

# Update all plugins
python lewis.py plugin update --all
```

## 🖥️ System Commands

### `status` - System Status

**Usage:** `python lewis.py status [OPTIONS]`

**Description:** Show LEWIS system status and health.

**Options:**
```bash
--detailed        Show detailed status
--format          Output format
--check-deps      Check dependencies
--performance     Include performance metrics
```

**Examples:**
```bash
# Basic status
python lewis.py status

# Detailed system information
python lewis.py status --detailed --performance

# Check dependencies
python lewis.py status --check-deps
```

### `health` - Health Check

**Usage:** `python lewis.py health [OPTIONS]`

**Description:** Perform comprehensive health check.

**Options:**
```bash
--components      Components to check
--timeout         Health check timeout
--fix             Attempt to fix issues
--report          Generate health report
```

**Examples:**
```bash
# Full health check
python lewis.py health

# Check specific components
python lewis.py health --components "database,cache,network"

# Health check with auto-fix
python lewis.py health --fix
```

### `service` - Service Management

**Usage:** `python lewis.py service [OPTIONS] COMMAND`

**Description:** Manage LEWIS services.

**Commands:**
```bash
start             Start LEWIS services
stop              Stop LEWIS services
restart           Restart LEWIS services
reload            Reload configuration
status            Show service status
```

**Examples:**
```bash
# Start all services
python lewis.py service start

# Restart web interface
python lewis.py service restart web

# Check service status
python lewis.py service status
```

## 🛠️ Utility Commands

### `db` - Database Management

**Usage:** `python lewis.py db [OPTIONS] COMMAND`

**Description:** Database management operations.

**Commands:**
```bash
init              Initialize database
migrate           Run database migrations
backup            Backup database
restore           Restore database
cleanup           Clean up old data
optimize          Optimize database
```

**Examples:**
```bash
# Initialize database
python lewis.py db init

# Run migrations
python lewis.py db migrate

# Backup database
python lewis.py db backup --output backup.sql

# Clean up data older than 30 days
python lewis.py db cleanup --older-than 30d
```

### `cache` - Cache Management

**Usage:** `python lewis.py cache [OPTIONS] COMMAND`

**Description:** Cache management operations.

**Commands:**
```bash
clear             Clear all cache
flush             Flush specific cache
stats             Show cache statistics
warm              Warm up cache
```

**Examples:**
```bash
# Clear all cache
python lewis.py cache clear

# Show cache stats
python lewis.py cache stats

# Warm up vulnerability cache
python lewis.py cache warm vulnerabilities
```

### `log` - Log Management

**Usage:** `python lewis.py log [OPTIONS] [COMMAND]`

**Description:** Log file management and analysis.

**Commands:**
```bash
tail              Tail log files
search            Search log files
rotate            Rotate log files
analyze           Analyze log patterns
```

**Options:**
```bash
--level           Log level filter
--since           Show logs since timestamp
--follow          Follow log output
--lines           Number of lines to show
```

**Examples:**
```bash
# Tail all logs
python lewis.py log tail --follow

# Search for errors
python lewis.py log search --level ERROR --since "1 hour ago"

# Analyze log patterns
python lewis.py log analyze --period "24 hours"
```

## 🚀 Advanced Commands

### `api` - API Operations

**Usage:** `python lewis.py api [OPTIONS] COMMAND`

**Description:** Direct API operations and testing.

**Commands:**
```bash
test              Test API endpoints
docs              Generate API documentation
validate          Validate API responses
benchmark         Benchmark API performance
```

**Examples:**
```bash
# Test all API endpoints
python lewis.py api test

# Generate API documentation
python lewis.py api docs --output api_docs.html

# Benchmark API performance
python lewis.py api benchmark --endpoints "/scan,/analyze"
```

### `integration` - Integration Testing

**Usage:** `python lewis.py integration [OPTIONS] COMMAND`

**Description:** Test external integrations.

**Commands:**
```bash
test              Test all integrations
validate          Validate integration configs
sync              Sync with external systems
```

**Examples:**
```bash
# Test all integrations
python lewis.py integration test

# Test specific integration
python lewis.py integration test --name splunk

# Sync with threat intelligence feeds
python lewis.py integration sync --type threat_intel
```

### `benchmark` - Performance Benchmarking

**Usage:** `python lewis.py benchmark [OPTIONS] [COMPONENT]`

**Description:** Run performance benchmarks.

**Options:**
```bash
--duration        Benchmark duration
--threads         Number of threads
--iterations      Number of iterations
--profile         Enable profiling
--report          Generate benchmark report
```

**Examples:**
```bash
# Benchmark scan performance
python lewis.py benchmark scan --duration 300

# Full system benchmark
python lewis.py benchmark --report benchmark_report.html

# Profile scanning engine
python lewis.py benchmark scan --profile --iterations 100
```

## 💡 Usage Tips

### Command Chaining

Commands can be chained for complex operations:

```bash
# Scan, analyze, and generate report
python lewis.py scan example.com | python lewis.py analyze | python lewis.py report executive
```

### Configuration Overrides

Override configuration values for specific commands:

```bash
# Override scan timeout for single command
python lewis.py --config.scanning.timeout=600 scan example.com
```

### Output Formatting

Format output for different use cases:

```bash
# JSON output for scripting
python lewis.py scan example.com --format json

# Human-readable table format
python lewis.py status --format table

# CSV for data analysis
python lewis.py export findings --format csv
```

### Environment Variables

Set environment variables for common options:

```bash
export LEWIS_CONFIG=/path/to/config.yaml
export LEWIS_LOG_LEVEL=DEBUG
export LEWIS_OUTPUT_FORMAT=json
```

## 🔍 Exit Codes

LEWIS uses standard exit codes:

- `0` - Success
- `1` - General error
- `2` - Misuse of command
- `3` - Configuration error
- `4` - Network error
- `5` - Permission error
- `126` - Command not found
- `130` - Script terminated by Control-C

## 📚 See Also

- [User Guide](03-user-guide.md) - Complete usage guide
- [Configuration Guide](04-configuration.md) - Configuration options
- [API Reference](05-api-reference.md) - API documentation
- [Troubleshooting](10-troubleshooting.md) - Common issues and solutions

---

**Next:** [Tool Integration](17-tool-integration.md) | **Previous:** [Contributing Guide](15-contributing.md)

---
*This guide is part of the LEWIS documentation. For more information, visit the [main documentation](README.md).*
