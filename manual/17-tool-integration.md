# LEWIS Tool Integration Guide

Comprehensive guide for integrating LEWIS with external security tools, platforms, and workflows.

## 🔗 Overview

LEWIS is designed to integrate seamlessly with existing security tools and platforms. This guide covers supported integrations and how to configure them.

## 📋 Table of Contents

1. [Security Scanners](#security-scanners)
2. [Vulnerability Management](#vulnerability-management)
3. [SIEM Platforms](#siem-platforms)
4. [Threat Intelligence](#threat-intelligence)
5. [Development Tools](#development-tools)
6. [Cloud Platforms](#cloud-platforms)
7. [Monitoring & Alerting](#monitoring--alerting)
8. [Custom Integrations](#custom-integrations)

## 🔍 Security Scanners

### Nmap Integration

**Description:** Network discovery and security auditing

**Configuration:**
```yaml
# config/integrations/nmap.yaml
nmap:
  enabled: true
  path: "/usr/bin/nmap"
  default_options: "-T4 -A"
  max_scan_time: 3600
  output_format: "xml"
  
  profiles:
    quick: "-T4 -F"
    comprehensive: "-T4 -A -sC -sV"
    stealth: "-sS -T2 -f"
    udp: "-sU --top-ports 1000"
```

**Usage:**
```python
from integrations.nmap_integration import NmapScanner

scanner = NmapScanner()
results = scanner.scan_target("192.168.1.0/24", profile="comprehensive")
```

**Features:**
- Automated port scanning
- Service version detection
- OS fingerprinting
- Vulnerability script scanning
- Custom scan profiles

### OpenVAS Integration

**Description:** Comprehensive vulnerability scanner

**Configuration:**
```yaml
# config/integrations/openvas.yaml
openvas:
  enabled: true
  host: "openvas.local"
  port: 9390
  username: "admin"
  password_env: "OPENVAS_PASSWORD"
  ssl_verify: true
  
  scan_configs:
    default: "daba56c8-73ec-11df-a475-002264764cea"
    full_fast: "8715c877-47a0-438d-98a3-27c7a6ab2196"
```

**Features:**
- Authenticated scanning
- Custom scan configurations
- Report generation
- Scheduled scanning
- Integration with LEWIS findings

### Burp Suite Integration

**Description:** Web application security testing

**Configuration:**
```yaml
# config/integrations/burp.yaml
burp:
  enabled: true
  api_url: "http://localhost:1337"
  api_key_env: "BURP_API_KEY"
  scan_timeout: 3600
  
  scan_settings:
    crawl_and_audit: true
    passive_crawl: false
    light_crawl: false
```

**Features:**
- Automated web app scanning
- Custom scan configurations
- Issue tracking integration
- Report generation
- Session handling

### Nikto Integration

**Description:** Web server scanner

**Configuration:**
```yaml
# config/integrations/nikto.yaml
nikto:
  enabled: true
  path: "/usr/bin/nikto"
  config_file: "/etc/nikto.conf"
  max_scan_time: 1800
  
  options:
    format: "xml"
    evasion: "1,2,3,4"
    tuning: "1,2,3,4,5,6,7,8,9,0"
```

**Features:**
- Web server vulnerability scanning
- CGI scanning
- SSL/TLS testing
- Custom plugins
- Output parsing

## 🛡️ Vulnerability Management

### Qualys VMDR Integration

**Description:** Cloud-based vulnerability management

**Configuration:**
```yaml
# config/integrations/qualys.yaml
qualys:
  enabled: true
  api_url: "https://qualysguard.qg2.apps.qualys.com"
  username: "api_user"
  password_env: "QUALYS_PASSWORD"
  
  settings:
    default_option_profile: "Initial Options"
    scan_priority: 5
    notification_list: "security@company.com"
```

**Features:**
- Asset discovery and tracking
- Vulnerability scanning
- Compliance reporting
- Risk-based prioritization
- Patch management

### Rapid7 Nexpose Integration

**Description:** Vulnerability risk management

**Configuration:**
```yaml
# config/integrations/nexpose.yaml
nexpose:
  enabled: true
  host: "nexpose.company.com"
  port: 3780
  username: "nxadmin"
  password_env: "NEXPOSE_PASSWORD"
  
  scan_templates:
    discovery: "discovery-scan"
    full_audit: "full-audit-without-web-spider"
    exhaustive: "exhaustive-scan"
```

**Features:**
- Asset discovery
- Vulnerability assessment
- Risk scoring
- Remediation planning
- Integration with patch management

### Tenable Nessus Integration

**Description:** Vulnerability scanner

**Configuration:**
```yaml
# config/integrations/nessus.yaml
nessus:
  enabled: true
  host: "nessus.company.com"
  port: 8834
  access_key: "access_key"
  secret_key_env: "NESSUS_SECRET_KEY"
  
  policies:
    basic: "Basic Network Scan"
    credentialed: "Credentialed Patch Audit"
    web_app: "Web Application Tests"
```

**Features:**
- Network vulnerability scanning
- Web application testing
- Compliance auditing
- Malware detection
- Custom policies

## 📊 SIEM Platforms

### Splunk Integration

**Description:** Security information and event management

**Configuration:**
```yaml
# config/integrations/splunk.yaml
splunk:
  enabled: true
  host: "splunk.company.com"
  port: 8089
  username: "lewis_integration"
  password_env: "SPLUNK_PASSWORD"
  
  settings:
    index: "lewis_findings"
    sourcetype: "lewis:scan"
    verify_ssl: true
```

**Implementation:**
```python
# integrations/splunk_integration.py
import splunklib.client as client

class SplunkIntegration:
    def __init__(self, config):
        self.service = client.connect(
            host=config['host'],
            port=config['port'],
            username=config['username'],
            password=config['password']
        )
        self.index = config['settings']['index']
    
    def send_findings(self, findings):
        index = self.service.indexes[self.index]
        for finding in findings:
            index.submit(json.dumps(finding))
```

**Features:**
- Real-time event streaming
- Custom dashboards
- Alerting and correlation
- Search and analytics
- Report automation

### IBM QRadar Integration

**Description:** Security intelligence platform

**Configuration:**
```yaml
# config/integrations/qradar.yaml
qradar:
  enabled: true
  console_ip: "192.168.1.100"
  sec_token_env: "QRADAR_SEC_TOKEN"
  version: "15.0"
  
  settings:
    verify_ssl: false
    timeout: 60
    offense_creation: true
```

**Features:**
- Event correlation
- Threat detection
- Incident response
- Compliance reporting
- Custom rules

### ArcSight Integration

**Description:** Enterprise security management

**Configuration:**
```yaml
# config/integrations/arcsight.yaml
arcsight:
  enabled: true
  manager_host: "arcsight.company.com"
  manager_port: 8443
  username: "lewis_user"
  password_env: "ARCSIGHT_PASSWORD"
  
  settings:
    destination: "LEWIS Connector"
    event_category: "Security/Vulnerability"
```

**Features:**
- Event correlation
- Real-time monitoring
- Compliance management
- Threat intelligence
- Custom connectors

## 🔍 Threat Intelligence

### VirusTotal Integration

**Description:** File and URL analysis service

**Configuration:**
```yaml
# config/integrations/virustotal.yaml
virustotal:
  enabled: true
  api_key_env: "VIRUSTOTAL_API_KEY"
  api_version: "v3"
  rate_limit: 4  # requests per minute for free tier
  
  settings:
    file_scanning: true
    url_scanning: true
    ip_scanning: true
    domain_scanning: true
```

**Features:**
- File hash analysis
- URL reputation checking
- IP/domain intelligence
- Malware detection
- Community contributions

### AlienVault OTX Integration

**Description:** Open threat exchange

**Configuration:**
```yaml
# config/integrations/otx.yaml
otx:
  enabled: true
  api_key_env: "OTX_API_KEY"
  base_url: "https://otx.alienvault.com/api/v1"
  
  settings:
    indicators: ["IPv4", "domain", "hostname", "URL", "FileHash-MD5"]
    pulse_subscription: true
```

**Features:**
- Threat intelligence feeds
- IOC analysis
- Pulse subscriptions
- Community sharing
- Custom indicators

### MISP Integration

**Description:** Malware information sharing platform

**Configuration:**
```yaml
# config/integrations/misp.yaml
misp:
  enabled: true
  url: "https://misp.company.com"
  api_key_env: "MISP_API_KEY"
  verify_ssl: true
  
  settings:
    event_creation: true
    attribute_sharing: true
    tag_prefix: "lewis:"
```

**Features:**
- Event management
- Attribute sharing
- Taxonomy support
- Federation
- API integration

## 💻 Development Tools

### Jenkins Integration

**Description:** Continuous integration/deployment

**Configuration:**
```yaml
# config/integrations/jenkins.yaml
jenkins:
  enabled: true
  url: "https://jenkins.company.com"
  username: "lewis_bot"
  api_token_env: "JENKINS_API_TOKEN"
  
  settings:
    build_trigger: true
    security_gate: true
    report_publishing: true
```

**Pipeline Integration:**
```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Security Scan') {
            steps {
                script {
                    def scanResult = sh(
                        script: "python lewis.py scan ${TARGET_URL}",
                        returnStdout: true
                    ).trim()
                    
                    if (scanResult.contains('CRITICAL')) {
                        error("Critical security issues found!")
                    }
                }
            }
        }
    }
}
```

### GitLab CI Integration

**Description:** DevOps platform integration

**Configuration:**
```yaml
# .gitlab-ci.yml
lewis_security_scan:
  stage: test
  script:
    - python lewis.py scan $CI_PROJECT_URL
    - python lewis.py report --format json > security_report.json
  artifacts:
    reports:
      junit: security_report.xml
    paths:
      - security_report.json
  only:
    - merge_requests
    - master
```

### GitHub Actions Integration

**Description:** CI/CD workflow automation

**Configuration:**
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install LEWIS
        run: pip install lewis-security
      - name: Run Security Scan
        run: lewis scan ${{ github.event.repository.html_url }}
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: security-results
          path: security_report.json
```

## ☁️ Cloud Platforms

### AWS Integration

**Description:** Amazon Web Services security

**Configuration:**
```yaml
# config/integrations/aws.yaml
aws:
  enabled: true
  access_key_id_env: "AWS_ACCESS_KEY_ID"
  secret_access_key_env: "AWS_SECRET_ACCESS_KEY"
  region: "us-east-1"
  
  services:
    ec2: true
    s3: true
    rds: true
    iam: true
    cloudtrail: true
    config: true
```

**Features:**
- EC2 instance scanning
- S3 bucket security analysis
- IAM policy review
- CloudTrail log analysis
- Config compliance checking
- Security Hub integration

### Azure Integration

**Description:** Microsoft Azure security

**Configuration:**
```yaml
# config/integrations/azure.yaml
azure:
  enabled: true
  subscription_id_env: "AZURE_SUBSCRIPTION_ID"
  tenant_id_env: "AZURE_TENANT_ID"
  client_id_env: "AZURE_CLIENT_ID"
  client_secret_env: "AZURE_CLIENT_SECRET"
  
  services:
    virtual_machines: true
    storage_accounts: true
    key_vault: true
    network_security_groups: true
```

**Features:**
- VM security assessment
- Storage account analysis
- Network security review
- Key Vault auditing
- Azure Security Center integration

### Google Cloud Integration

**Description:** Google Cloud Platform security

**Configuration:**
```yaml
# config/integrations/gcp.yaml
gcp:
  enabled: true
  project_id: "my-project"
  credentials_path_env: "GOOGLE_APPLICATION_CREDENTIALS"
  
  services:
    compute: true
    storage: true
    iam: true
    cloud_sql: true
    gke: true
```

**Features:**
- Compute Engine analysis
- Cloud Storage security
- IAM policy review
- Cloud SQL assessment
- GKE cluster security

## 📈 Monitoring & Alerting

### Prometheus Integration

**Description:** Monitoring and alerting toolkit

**Configuration:**
```yaml
# config/integrations/prometheus.yaml
prometheus:
  enabled: true
  pushgateway_url: "http://prometheus-pushgateway:9091"
  job_name: "lewis"
  
  metrics:
    scan_duration: true
    finding_counts: true
    system_metrics: true
```

**Implementation:**
```python
# monitoring/prometheus_metrics.py
from prometheus_client import Counter, Histogram, Gauge

scan_counter = Counter('lewis_scans_total', 'Total scans performed')
scan_duration = Histogram('lewis_scan_duration_seconds', 'Scan duration')
active_scans = Gauge('lewis_active_scans', 'Currently active scans')
```

### Grafana Integration

**Description:** Analytics and monitoring dashboards

**Configuration:**
```yaml
# config/integrations/grafana.yaml
grafana:
  enabled: true
  url: "http://grafana:3000"
  api_key_env: "GRAFANA_API_KEY"
  
  dashboards:
    security_overview: true
    scan_metrics: true
    threat_trends: true
```

**Dashboard Configuration:**
```json
{
  "dashboard": {
    "title": "LEWIS Security Dashboard",
    "panels": [
      {
        "title": "Scan Rate",
        "type": "graph",
        "targets": [{"expr": "rate(lewis_scans_total[5m])"}]
      },
      {
        "title": "Finding Severity",
        "type": "piechart", 
        "targets": [{"expr": "lewis_findings_by_severity"}]
      }
    ]
  }
}
```

### Slack Integration

**Description:** Team collaboration and notifications

**Configuration:**
```yaml
# config/integrations/slack.yaml
slack:
  enabled: true
  webhook_url_env: "SLACK_WEBHOOK_URL"
  
  channels:
    security_alerts: "#security-alerts"
    scan_results: "#security-scans"
    critical_findings: "#critical-security"
  
  settings:
    severity_threshold: "medium"
    mention_team: "@security-team"
```

**Features:**
- Real-time notifications
- Custom alert channels
- Severity-based routing
- Interactive messages
- Report sharing

## 🔧 Custom Integrations

### Integration Framework

**Base Integration Class:**
```python
# integrations/base_integration.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseIntegration(ABC):
    def __init__(self, config: Dict):
        self.config = config
        self.name = self.__class__.__name__
        self.enabled = config.get('enabled', False)
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the integration"""
        pass
    
    @abstractmethod
    def send_data(self, data: Any) -> bool:
        """Send data to external system"""
        pass
    
    @abstractmethod
    def receive_data(self, query: Dict) -> List[Dict]:
        """Receive data from external system"""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Check integration health"""
        pass
    
    def validate_config(self) -> bool:
        """Validate integration configuration"""
        required_fields = self.get_required_fields()
        return all(field in self.config for field in required_fields)
    
    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Get required configuration fields"""
        pass
```

### Custom Integration Example

**ServiceNow Integration:**
```python
# integrations/servicenow_integration.py
import requests
from integrations.base_integration import BaseIntegration

class ServiceNowIntegration(BaseIntegration):
    def initialize(self) -> bool:
        self.base_url = f"https://{self.config['instance']}.service-now.com"
        self.auth = (self.config['username'], self.config['password'])
        return self.health_check()
    
    def send_data(self, finding: Dict) -> bool:
        """Create incident from security finding"""
        incident_data = {
            'short_description': f"Security Finding: {finding['title']}",
            'description': finding['description'],
            'priority': self.map_severity(finding['severity']),
            'category': 'Security',
            'assignment_group': self.config.get('assignment_group')
        }
        
        response = requests.post(
            f"{self.base_url}/api/now/table/incident",
            auth=self.auth,
            json=incident_data,
            headers={'Content-Type': 'application/json'}
        )
        
        return response.status_code == 201
    
    def receive_data(self, query: Dict) -> List[Dict]:
        """Query ServiceNow for related incidents"""
        params = {'sysparm_query': self.build_query(query)}
        
        response = requests.get(
            f"{self.base_url}/api/now/table/incident",
            auth=self.auth,
            params=params
        )
        
        if response.status_code == 200:
            return response.json().get('result', [])
        return []
    
    def health_check(self) -> bool:
        """Check ServiceNow connectivity"""
        try:
            response = requests.get(
                f"{self.base_url}/api/now/table/sys_user",
                auth=self.auth,
                params={'sysparm_limit': 1}
            )
            return response.status_code == 200
        except:
            return False
    
    def get_required_fields(self) -> List[str]:
        return ['instance', 'username', 'password']
    
    def map_severity(self, severity: str) -> str:
        mapping = {
            'critical': '1',
            'high': '2', 
            'medium': '3',
            'low': '4',
            'info': '5'
        }
        return mapping.get(severity.lower(), '3')
```

### Integration Registry

**Dynamic Integration Loading:**
```python
# integrations/integration_manager.py
import importlib
from typing import Dict, List
from integrations.base_integration import BaseIntegration

class IntegrationManager:
    def __init__(self):
        self.integrations: Dict[str, BaseIntegration] = {}
        self.config = {}
    
    def load_integrations(self, config: Dict):
        """Load and initialize all configured integrations"""
        self.config = config
        
        for integration_name, integration_config in config.items():
            if integration_config.get('enabled', False):
                try:
                    integration = self.create_integration(integration_name, integration_config)
                    if integration and integration.initialize():
                        self.integrations[integration_name] = integration
                        print(f"Loaded integration: {integration_name}")
                    else:
                        print(f"Failed to initialize integration: {integration_name}")
                except Exception as e:
                    print(f"Error loading integration {integration_name}: {e}")
    
    def create_integration(self, name: str, config: Dict) -> BaseIntegration:
        """Dynamically create integration instance"""
        try:
            module_name = f"integrations.{name}_integration"
            class_name = f"{name.title()}Integration"
            
            module = importlib.import_module(module_name)
            integration_class = getattr(module, class_name)
            
            return integration_class(config)
        except (ImportError, AttributeError) as e:
            print(f"Integration {name} not found: {e}")
            return None
    
    def send_to_all(self, data: Any):
        """Send data to all active integrations"""
        for name, integration in self.integrations.items():
            try:
                integration.send_data(data)
            except Exception as e:
                print(f"Error sending to {name}: {e}")
    
    def health_check_all(self) -> Dict[str, bool]:
        """Check health of all integrations"""
        results = {}
        for name, integration in self.integrations.items():
            results[name] = integration.health_check()
        return results
```

## 📋 Integration Best Practices

### Configuration Management

1. **Environment Variables**: Store sensitive data in environment variables
2. **Configuration Validation**: Validate all integration configs on startup
3. **Fallback Handling**: Implement graceful degradation when integrations fail
4. **Rate Limiting**: Respect API rate limits of external services
5. **Error Handling**: Implement robust error handling and logging

### Security Considerations

1. **Authentication**: Use secure authentication methods (API keys, OAuth)
2. **Encryption**: Encrypt data in transit and at rest
3. **Access Control**: Implement least privilege access
4. **Audit Logging**: Log all integration activities
5. **Certificate Validation**: Verify SSL/TLS certificates

### Performance Optimization

1. **Async Processing**: Use asynchronous operations where possible
2. **Connection Pooling**: Reuse connections to external services
3. **Caching**: Cache responses to reduce API calls
4. **Batch Operations**: Use batch operations when available
5. **Timeout Handling**: Set appropriate timeouts

### Monitoring and Alerting

1. **Health Checks**: Regular health checks for all integrations
2. **Performance Metrics**: Monitor integration performance
3. **Error Tracking**: Track and alert on integration errors
4. **SLA Monitoring**: Monitor SLA compliance
5. **Capacity Planning**: Plan for scaling integration usage

---

**Next:** [FAQ](18-faq.md) | **Previous:** [Command Reference](16-command-reference.md)

---
*This guide is part of the LEWIS documentation. For more information, visit the [main documentation](README.md).*
