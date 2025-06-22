# LEWIS Template Files

This directory contains template files used by LEWIS for various configurations and outputs.

## Template Types

### Service Templates
- `lewis.service.template` - Systemd service template
- `lewis.init.template` - SysV init script template

### Configuration Templates  
- `config.yaml.template` - Default configuration template
- `nginx.conf.template` - Nginx configuration for web interface
- `apache.conf.template` - Apache configuration template

### Report Templates
- `security_report.html.template` - HTML security report template
- `threat_analysis.md.template` - Markdown threat analysis template
- `executive_summary.docx.template` - Executive summary template

### Extension Templates
- `extension_manifest.json.template` - Extension manifest template
- `extension_structure/` - Complete extension template directory

## Usage

Templates are used by LEWIS to generate:
- System service configurations
- Configuration files for new installations
- Standardized reports and outputs
- Extension boilerplate code

## Template Variables

Common template variables:
- `{LEWIS_HOME}` - LEWIS installation directory
- `{LEWIS_USER}` - LEWIS system user
- `{LEWIS_CONFIG}` - Configuration directory
- `{DATE}` - Current date
- `{VERSION}` - LEWIS version
- `{HOSTNAME}` - System hostname

## Template Processing

Templates are processed by the LEWIS template engine which:
- Substitutes variables with actual values
- Supports conditional blocks
- Handles file inclusion
- Validates template syntax

## Creating Templates

When creating new templates:
1. Use `.template` extension
2. Document required variables
3. Include example values in comments
4. Test with different variable sets
5. Update this README
