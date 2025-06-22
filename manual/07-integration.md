# LEWIS Integration Guide

This guide covers how to integrate LEWIS with other tools, systems, and platforms for enhanced security operations.

## 🔗 Overview

LEWIS is designed to work seamlessly with existing security infrastructure, development tools, and enterprise systems. This guide provides comprehensive integration instructions.

## 📋 Table of Contents

1. [SIEM Integration](#siem-integration)
2. [Security Tools Integration](#security-tools-integration)
3. [CI/CD Pipeline Integration](#cicd-pipeline-integration)
4. [Enterprise Systems](#enterprise-systems)
5. [Cloud Platform Integration](#cloud-platform-integration)
6. [Monitoring and Alerting](#monitoring-and-alerting)
7. [API Integration](#api-integration)
8. [Custom Integrations](#custom-integrations)

## 🛡️ SIEM Integration

### Splunk Integration

```python
# integrations/splunk_integration.py
import splunklib.client as client
from core.lewis_core import LEWISCore

class SplunkIntegration:
    def __init__(self, host, port, username, password):
        self.service = client.connect(
            host=host,
            port=port,
            username=username,
            password=password
        )
    
    def send_findings(self, findings):
        """Send LEWIS findings to Splunk"""
        index = self.service.indexes["lewis_findings"]
        
        for finding in findings:
            event_data = {
                'timestamp': finding['timestamp'],
                'severity': finding['severity'],
                'target': finding['target'],
                'description': finding['description'],
                'source': 'LEWIS'
            }
            index.submit(json.dumps(event_data))
    
    def query_threats(self, query):
        """Query Splunk for threat data"""
        job = self.service.jobs.create(query)
        
        # Wait for job completion
        while not job.is_done():
            time.sleep(1)
        
        # Get results
        results = []
        for result in job.results():
            results.append(dict(result))
        
        return results
```

### ELK Stack Integration

```python
# integrations/elk_integration.py
from elasticsearch import Elasticsearch
import json

class ELKIntegration:
    def __init__(self, hosts, index_name="lewis-findings"):
        self.es = Elasticsearch(hosts)
        self.index = index_name
    
    def index_findings(self, findings):
        """Index LEWIS findings in Elasticsearch"""
        for finding in findings:
            doc = {
                'timestamp': finding['timestamp'],
                'severity': finding['severity'],
                'target': finding['target'],
                'vulnerability': finding.get('vulnerability', ''),
                'description': finding['description'],
                'risk_score': finding.get('risk_score', 0),
                'source': 'LEWIS'
            }
            
            self.es.index(index=self.index, body=doc)
    
    def search_findings(self, query):
        """Search findings in Elasticsearch"""
        search_body = {
            "query": {
                "query_string": {
                    "query": query
                }
            }
        }
        
        response = self.es.search(index=self.index, body=search_body)
        return response['hits']['hits']
```

### QRadar Integration

```python
# integrations/qradar_integration.py
import requests
import json

class QRadarIntegration:
    def __init__(self, console_ip, sec_token):
        self.base_url = f"https://{console_ip}/api"
        self.headers = {
            'SEC': sec_token,
            'Content-Type': 'application/json'
        }
    
    def create_offense(self, finding):
        """Create QRadar offense from LEWIS finding"""
        offense_data = {
            'description': f"LEWIS Finding: {finding['description']}",
            'magnitude': self.map_severity_to_magnitude(finding['severity']),
            'status': 'OPEN'
        }
        
        response = requests.post(
            f"{self.base_url}/siem/offenses",
            headers=self.headers,
            data=json.dumps(offense_data),
            verify=False
        )
        
        return response.json()
    
    def map_severity_to_magnitude(self, severity):
        """Map LEWIS severity to QRadar magnitude"""
        mapping = {
            'critical': 8,
            'high': 6,
            'medium': 4,
            'low': 2,
            'info': 1
        }
        return mapping.get(severity.lower(), 1)
```

## 🔧 Security Tools Integration

### Nmap Integration

```python
# integrations/nmap_integration.py
import nmap
from tools.tool_manager import ToolManager

class NmapIntegration(ToolManager):
    def __init__(self):
        super().__init__()
        self.nm = nmap.PortScanner()
    
    def enhanced_scan(self, target, scan_type="comprehensive"):
        """Enhanced Nmap scan with LEWIS processing"""
        scan_args = self.get_scan_arguments(scan_type)
        
        # Perform Nmap scan
        self.nm.scan(target, arguments=scan_args)
        
        # Process results with LEWIS
        results = self.process_nmap_results(self.nm)
        
        return results
    
    def get_scan_arguments(self, scan_type):
        """Get Nmap arguments based on scan type"""
        scan_types = {
            'quick': '-T4 -F',
            'comprehensive': '-T4 -A -v',
            'stealth': '-sS -T2',
            'udp': '-sU',
            'vulnerability': '--script vuln'
        }
        return scan_types.get(scan_type, '-T4 -A')
```

### Metasploit Integration

```python
# integrations/metasploit_integration.py
from pymetasploit3.msfrpc import MsfRpcClient

class MetasploitIntegration:
    def __init__(self, password='msf', server='127.0.0.1', port=55553):
        self.client = MsfRpcClient(password, server=server, port=port)
    
    def exploit_vulnerability(self, target, vulnerability):
        """Attempt to exploit identified vulnerability"""
        # Select appropriate exploit
        exploit = self.select_exploit(vulnerability)
        
        if exploit:
            # Configure exploit
            exploit_obj = self.client.modules.use('exploit', exploit)
            exploit_obj['RHOSTS'] = target
            
            # Select payload
            payload = self.select_payload(vulnerability)
            exploit_obj.payload = payload
            
            # Execute exploit
            result = exploit_obj.execute()
            
            return {
                'success': result.get('job_id') is not None,
                'exploit': exploit,
                'payload': payload,
                'result': result
            }
        
        return {'success': False, 'error': 'No suitable exploit found'}
    
    def select_exploit(self, vulnerability):
        """Select appropriate exploit for vulnerability"""
        # Mapping of vulnerabilities to exploits
        exploit_mapping = {
            'ms17-010': 'windows/smb/ms17_010_eternalblue',
            'cve-2014-6271': 'multi/http/apache_mod_cgi_bash_env_exec',
            # Add more mappings
        }
        
        return exploit_mapping.get(vulnerability.lower())
```

### Burp Suite Integration

```python
# integrations/burp_integration.py
import requests
import json

class BurpIntegration:
    def __init__(self, api_url='http://localhost:1337'):
        self.api_url = api_url
    
    def start_scan(self, target_url):
        """Start Burp Suite scan"""
        scan_config = {
            'urls': [target_url],
            'application_logins': [],
            'resource_pool': None
        }
        
        response = requests.post(
            f"{self.api_url}/v0.1/scan",
            json=scan_config
        )
        
        return response.json()['task_id']
    
    def get_scan_status(self, task_id):
        """Get scan status"""
        response = requests.get(f"{self.api_url}/v0.1/scan/{task_id}")
        return response.json()
    
    def get_scan_issues(self, task_id):
        """Get scan issues"""
        response = requests.get(f"{self.api_url}/v0.1/scan/{task_id}/issues")
        return response.json()['issues']
```

## 🚀 CI/CD Pipeline Integration

### Jenkins Integration

```groovy
// jenkins/lewis-pipeline.groovy
pipeline {
    agent any
    
    stages {
        stage('LEWIS Security Scan') {
            steps {
                script {
                    // Run LEWIS scan
                    sh '''
                        python lewis.py --target ${TARGET_URL} \
                                      --output jenkins-report.json \
                                      --format json
                    '''
                    
                    // Parse results
                    def scanResults = readJSON file: 'jenkins-report.json'
                    
                    // Check for critical findings
                    if (scanResults.critical_count > 0) {
                        error "Critical security issues found!"
                    }
                    
                    // Archive results
                    archiveArtifacts artifacts: 'jenkins-report.json'
                }
            }
        }
    }
    
    post {
        always {
            // Publish security report
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'lewis-report.html',
                reportName: 'LEWIS Security Report'
            ])
        }
    }
}
```

### GitHub Actions Integration

```yaml
# .github/workflows/lewis-security-scan.yml
name: LEWIS Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install LEWIS
      run: |
        pip install -r requirements.txt
        python setup.py install
    
    - name: Run LEWIS Scan
      run: |
        python lewis.py --target ${{ github.event.repository.html_url }} \
                       --output security-report.json \
                       --format json
    
    - name: Upload Security Report
      uses: actions/upload-artifact@v2
      with:
        name: lewis-security-report
        path: security-report.json
    
    - name: Check Security Issues
      run: |
        python scripts/check_security_issues.py security-report.json
```

### GitLab CI Integration

```yaml
# .gitlab-ci.yml
stages:
  - security-scan

lewis-security-scan:
  stage: security-scan
  image: python:3.9
  
  before_script:
    - pip install -r requirements.txt
    - python setup.py install
  
  script:
    - python lewis.py --target $CI_PROJECT_URL --output security-report.json
  
  artifacts:
    reports:
      junit: security-report.xml
    paths:
      - security-report.json
      - security-report.html
    expire_in: 1 week
  
  only:
    - master
    - develop
```

## 🏢 Enterprise Systems

### Active Directory Integration

```python
# integrations/ad_integration.py
from ldap3 import Server, Connection, ALL

class ActiveDirectoryIntegration:
    def __init__(self, server, user, password, domain):
        self.server = Server(server, get_info=ALL)
        self.conn = Connection(
            self.server,
            user=f"{domain}\\{user}",
            password=password,
            auto_bind=True
        )
    
    def get_user_info(self, username):
        """Get user information from AD"""
        search_filter = f"(sAMAccountName={username})"
        
        self.conn.search(
            search_base='dc=domain,dc=com',
            search_filter=search_filter,
            attributes=['displayName', 'mail', 'memberOf']
        )
        
        return self.conn.entries
    
    def check_privileged_accounts(self):
        """Check for privileged accounts"""
        privileged_groups = [
            'Domain Admins',
            'Enterprise Admins',
            'Schema Admins'
        ]
        
        findings = []
        for group in privileged_groups:
            members = self.get_group_members(group)
            findings.append({
                'group': group,
                'members': members,
                'risk_level': 'high' if len(members) > 5 else 'medium'
            })
        
        return findings
```

### ServiceNow Integration

```python
# integrations/servicenow_integration.py
import requests
import json

class ServiceNowIntegration:
    def __init__(self, instance, username, password):
        self.base_url = f"https://{instance}.service-now.com/api/now"
        self.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def create_incident(self, finding):
        """Create ServiceNow incident from LEWIS finding"""
        incident_data = {
            'short_description': f"Security Finding: {finding['title']}",
            'description': finding['description'],
            'priority': self.map_severity_to_priority(finding['severity']),
            'category': 'Security',
            'subcategory': 'Vulnerability',
            'assignment_group': 'Security Team'
        }
        
        response = requests.post(
            f"{self.base_url}/table/incident",
            auth=self.auth,
            headers=self.headers,
            data=json.dumps(incident_data)
        )
        
        return response.json()
    
    def map_severity_to_priority(self, severity):
        """Map LEWIS severity to ServiceNow priority"""
        mapping = {
            'critical': '1',
            'high': '2',
            'medium': '3',
            'low': '4',
            'info': '5'
        }
        return mapping.get(severity.lower(), '3')
```

## ☁️ Cloud Platform Integration

### AWS Integration

```python
# integrations/aws_integration.py
import boto3
from botocore.exceptions import ClientError

class AWSIntegration:
    def __init__(self, access_key=None, secret_key=None, region='us-east-1'):
        if access_key and secret_key:
            self.session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
        else:
            self.session = boto3.Session(region_name=region)
    
    def scan_s3_buckets(self):
        """Scan S3 buckets for security issues"""
        s3 = self.session.client('s3')
        findings = []
        
        try:
            buckets = s3.list_buckets()['Buckets']
            
            for bucket in buckets:
                bucket_name = bucket['Name']
                
                # Check bucket policy
                try:
                    policy = s3.get_bucket_policy(Bucket=bucket_name)
                    # Analyze policy for security issues
                    policy_findings = self.analyze_bucket_policy(policy)
                    findings.extend(policy_findings)
                except ClientError:
                    # No bucket policy found
                    findings.append({
                        'resource': bucket_name,
                        'issue': 'No bucket policy configured',
                        'severity': 'medium'
                    })
                
                # Check public access
                public_access = self.check_bucket_public_access(s3, bucket_name)
                if public_access:
                    findings.append({
                        'resource': bucket_name,
                        'issue': 'Bucket allows public access',
                        'severity': 'high'
                    })
        
        except ClientError as e:
            print(f"Error scanning S3 buckets: {e}")
        
        return findings
    
    def scan_ec2_instances(self):
        """Scan EC2 instances for security issues"""
        ec2 = self.session.client('ec2')
        findings = []
        
        try:
            instances = ec2.describe_instances()
            
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    
                    # Check security groups
                    security_groups = instance.get('SecurityGroups', [])
                    for sg in security_groups:
                        sg_findings = self.analyze_security_group(ec2, sg['GroupId'])
                        findings.extend(sg_findings)
        
        except ClientError as e:
            print(f"Error scanning EC2 instances: {e}")
        
        return findings
```

### Azure Integration

```python
# integrations/azure_integration.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

class AzureIntegration:
    def __init__(self, subscription_id):
        self.credential = DefaultAzureCredential()
        self.subscription_id = subscription_id
        
        self.resource_client = ResourceManagementClient(
            self.credential, subscription_id
        )
        self.compute_client = ComputeManagementClient(
            self.credential, subscription_id
        )
        self.network_client = NetworkManagementClient(
            self.credential, subscription_id
        )
    
    def scan_virtual_machines(self):
        """Scan Azure VMs for security issues"""
        findings = []
        
        for resource_group in self.resource_client.resource_groups.list():
            rg_name = resource_group.name
            
            vms = self.compute_client.virtual_machines.list(rg_name)
            
            for vm in vms:
                vm_findings = self.analyze_vm_security(vm, rg_name)
                findings.extend(vm_findings)
        
        return findings
    
    def scan_network_security_groups(self):
        """Scan Network Security Groups"""
        findings = []
        
        for resource_group in self.resource_client.resource_groups.list():
            rg_name = resource_group.name
            
            nsgs = self.network_client.network_security_groups.list(rg_name)
            
            for nsg in nsgs:
                nsg_findings = self.analyze_nsg_rules(nsg)
                findings.extend(nsg_findings)
        
        return findings
```

## 📊 Monitoring and Alerting

### Prometheus Integration

```python
# integrations/prometheus_integration.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

class PrometheusIntegration:
    def __init__(self):
        # Define metrics
        self.scan_counter = Counter('lewis_scans_total', 'Total scans performed')
        self.finding_counter = Counter(
            'lewis_findings_total', 
            'Total findings by severity', 
            ['severity']
        )
        self.scan_duration = Histogram(
            'lewis_scan_duration_seconds',
            'Time spent on scans'
        )
        self.active_scans = Gauge(
            'lewis_active_scans',
            'Number of active scans'
        )
    
    def record_scan_start(self):
        """Record scan start"""
        self.scan_counter.inc()
        self.active_scans.inc()
        return time.time()
    
    def record_scan_end(self, start_time, findings):
        """Record scan completion"""
        duration = time.time() - start_time
        self.scan_duration.observe(duration)
        self.active_scans.dec()
        
        # Record findings by severity
        for finding in findings:
            severity = finding.get('severity', 'unknown')
            self.finding_counter.labels(severity=severity).inc()
    
    def start_metrics_server(self, port=8000):
        """Start Prometheus metrics server"""
        start_http_server(port)
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "LEWIS Security Dashboard",
    "panels": [
      {
        "title": "Scan Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(lewis_scans_total[5m])",
            "legendFormat": "Scans per second"
          }
        ]
      },
      {
        "title": "Findings by Severity",
        "type": "piechart",
        "targets": [
          {
            "expr": "lewis_findings_total",
            "legendFormat": "{{severity}}"
          }
        ]
      },
      {
        "title": "Active Scans",
        "type": "singlestat",
        "targets": [
          {
            "expr": "lewis_active_scans",
            "legendFormat": "Active Scans"
          }
        ]
      }
    ]
  }
}
```

## 🔌 API Integration

### REST API Client

```python
# integrations/api_client.py
import requests
import json

class LEWISAPIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def submit_scan_request(self, target, scan_type='full'):
        """Submit scan request via API"""
        data = {
            'target': target,
            'scan_type': scan_type,
            'callback_url': f"{self.base_url}/callbacks/scan_complete"
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/scans",
            headers=self.headers,
            data=json.dumps(data)
        )
        
        return response.json()
    
    def get_scan_results(self, scan_id):
        """Get scan results via API"""
        response = requests.get(
            f"{self.base_url}/api/v1/scans/{scan_id}/results",
            headers=self.headers
        )
        
        return response.json()
```

### Webhook Integration

```python
# integrations/webhook_handler.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/webhook/findings', methods=['POST'])
def handle_findings_webhook():
    """Handle incoming findings webhook"""
    try:
        data = request.get_json()
        
        # Process findings
        findings = data.get('findings', [])
        
        for finding in findings:
            # Forward to appropriate systems
            if finding['severity'] in ['critical', 'high']:
                send_to_incident_management(finding)
            
            # Update threat intelligence
            update_threat_intelligence(finding)
            
            # Log to SIEM
            send_to_siem(finding)
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_to_incident_management(finding):
    """Send high-severity findings to incident management"""
    # Implementation here
    pass

def update_threat_intelligence(finding):
    """Update threat intelligence with finding"""
    # Implementation here
    pass

def send_to_siem(finding):
    """Send finding to SIEM"""
    # Implementation here
    pass
```

## 🛠️ Custom Integrations

### Integration Template

```python
# integrations/custom_integration_template.py
from abc import ABC, abstractmethod

class IntegrationBase(ABC):
    """Base class for custom integrations"""
    
    def __init__(self, config):
        self.config = config
        self.initialize()
    
    @abstractmethod
    def initialize(self):
        """Initialize the integration"""
        pass
    
    @abstractmethod
    def send_findings(self, findings):
        """Send findings to external system"""
        pass
    
    @abstractmethod
    def get_data(self, query):
        """Get data from external system"""
        pass
    
    def validate_config(self):
        """Validate integration configuration"""
        required_fields = self.get_required_config_fields()
        
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required config field: {field}")
    
    @abstractmethod
    def get_required_config_fields(self):
        """Return list of required configuration fields"""
        pass

class CustomIntegration(IntegrationBase):
    """Example custom integration"""
    
    def initialize(self):
        """Initialize custom integration"""
        self.validate_config()
        # Custom initialization logic
    
    def send_findings(self, findings):
        """Send findings to custom system"""
        # Implementation here
        pass
    
    def get_data(self, query):
        """Get data from custom system"""
        # Implementation here
        return []
    
    def get_required_config_fields(self):
        """Required configuration fields"""
        return ['api_url', 'api_key', 'timeout']
```

### Integration Configuration

```yaml
# config/integrations.yaml
integrations:
  splunk:
    enabled: true
    host: "splunk.company.com"
    port: 8089
    username: "lewis_user"
    password_env: "SPLUNK_PASSWORD"
    index: "lewis_findings"
  
  servicenow:
    enabled: true
    instance: "company"
    username: "lewis_integration"
    password_env: "SERVICENOW_PASSWORD"
    assignment_group: "Security Team"
  
  slack:
    enabled: true
    webhook_url_env: "SLACK_WEBHOOK_URL"
    channel: "#security-alerts"
    severity_threshold: "medium"
  
  jira:
    enabled: true
    server: "https://company.atlassian.net"
    username: "lewis@company.com"
    api_token_env: "JIRA_API_TOKEN"
    project_key: "SEC"
```

## 📋 Integration Checklist

### Pre-Integration Steps

- [ ] Review system requirements
- [ ] Obtain necessary credentials/API keys
- [ ] Configure network access
- [ ] Test connectivity
- [ ] Backup existing configurations

### Post-Integration Steps

- [ ] Validate data flow
- [ ] Test error handling
- [ ] Monitor performance impact
- [ ] Document configuration
- [ ] Train users
- [ ] Set up monitoring/alerts

## 🆘 Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify credentials
   - Check API key validity
   - Review permissions

2. **Network Connectivity**
   - Check firewall rules
   - Verify DNS resolution
   - Test network connectivity

3. **Data Format Issues**
   - Validate data schema
   - Check encoding/formatting
   - Review API documentation

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable integration debugging
lewis.set_integration_debug(True)
```

---

**Next:** [Security Guide](08-security.md) | **Previous:** [Customization Guide](06-customization.md)

---
*This guide is part of the LEWIS documentation. For more information, visit the [main documentation](README.md).*
