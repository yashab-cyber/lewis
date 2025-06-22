# LEWIS API Reference

Complete reference guide for LEWIS REST API, Python SDK, and integration capabilities.

## 🌐 REST API Overview

LEWIS provides a comprehensive REST API for programmatic access to all cybersecurity operations.

### Base URL
```
https://lewis.company.com/api/v1
```

### Authentication
All API requests require authentication using JWT tokens or API keys.

#### JWT Authentication
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "analyst",
  "password": "password",
  "mfa_token": "123456"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

#### API Key Authentication
```http
GET /api/v1/system/status
Authorization: ApiKey your-api-key-here
```

### Error Handling
Standard HTTP status codes are used. Error responses include detailed information:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid target format",
    "details": {
      "field": "target",
      "expected": "IP address or hostname"
    },
    "timestamp": "2025-06-21T10:30:00Z"
  }
}
```

## 🔍 Scanning Operations

### Network Scanning

#### Start Network Scan
```http
POST /api/v1/scan/network
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "target": "192.168.1.0/24",
  "options": {
    "scan_type": "comprehensive",
    "include_services": true,
    "include_os_detection": true,
    "timeout": 300,
    "rate_limit": 100
  }
}
```

Response:
```json
{
  "scan_id": "scan_12345",
  "status": "started",
  "target": "192.168.1.0/24",
  "estimated_duration": 180,
  "created_at": "2025-06-21T10:30:00Z"
}
```

#### Get Scan Status
```http
GET /api/v1/scan/{scan_id}/status
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "scan_id": "scan_12345",
  "status": "running",
  "progress": {
    "percentage": 45,
    "current_target": "192.168.1.100",
    "completed_hosts": 112,
    "total_hosts": 254
  },
  "elapsed_time": 67,
  "estimated_remaining": 82
}
```

#### Get Scan Results
```http
GET /api/v1/scan/{scan_id}/results
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "scan_id": "scan_12345",
  "status": "completed",
  "results": {
    "hosts_discovered": 45,
    "services_found": 234,
    "vulnerabilities": 12,
    "hosts": [
      {
        "ip": "192.168.1.100",
        "hostname": "server01.local",
        "status": "up",
        "os": "Linux Ubuntu 20.04",
        "ports": [
          {
            "port": 22,
            "protocol": "tcp",
            "state": "open",
            "service": "ssh",
            "version": "OpenSSH 8.2p1"
          }
        ]
      }
    ]
  }
}
```

### Web Application Scanning

#### Start Web Scan
```http
POST /api/v1/scan/web
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "target": "https://example.com",
  "options": {
    "scan_type": "comprehensive",
    "include_ssl_analysis": true,
    "include_directory_enumeration": true,
    "include_vulnerability_scan": true,
    "max_depth": 3,
    "timeout": 1800
  }
}
```

### Vulnerability Scanning

#### Start Vulnerability Assessment
```http
POST /api/v1/scan/vulnerability
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "targets": ["192.168.1.100", "192.168.1.101"],
  "options": {
    "severity_filter": ["high", "critical"],
    "include_patches": true,
    "update_definitions": true
  }
}
```

## 📊 Data Management

### Scan Management

#### List Scans
```http
GET /api/v1/scans?page=1&limit=20&status=completed
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "scans": [
    {
      "scan_id": "scan_12345",
      "type": "network",
      "target": "192.168.1.0/24",
      "status": "completed",
      "created_at": "2025-06-21T10:30:00Z",
      "completed_at": "2025-06-21T10:33:45Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_results": 97,
    "has_next": true
  }
}
```

#### Delete Scan
```http
DELETE /api/v1/scan/{scan_id}
Authorization: Bearer <jwt_token>
```

### Export Data

#### Export Scan Results
```http
POST /api/v1/scan/{scan_id}/export
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "format": "pdf",
  "include_raw_data": false,
  "template": "executive_summary"
}
```

Response:
```json
{
  "export_id": "export_67890",
  "download_url": "/api/v1/exports/export_67890/download",
  "expires_at": "2025-06-22T10:30:00Z"
}
```

## 📈 Analytics and Reporting

### Dashboard Data

#### Get Dashboard Statistics
```http
GET /api/v1/analytics/dashboard
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "summary": {
    "total_scans": 156,
    "active_scans": 3,
    "hosts_discovered": 1247,
    "vulnerabilities_found": 89,
    "risk_score": 7.2
  },
  "recent_activity": [
    {
      "type": "scan_completed",
      "target": "192.168.1.0/24",
      "timestamp": "2025-06-21T10:30:00Z"
    }
  ],
  "vulnerability_trends": {
    "critical": [2, 3, 1, 4, 2],
    "high": [8, 12, 9, 15, 11],
    "medium": [23, 28, 21, 31, 25]
  }
}
```

### Reports

#### Generate Report
```http
POST /api/v1/reports/generate
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "type": "vulnerability_assessment",
  "scope": {
    "scan_ids": ["scan_12345", "scan_12346"],
    "date_range": {
      "start": "2025-06-01",
      "end": "2025-06-21"
    }
  },
  "format": "pdf",
  "template": "detailed_technical",
  "options": {
    "include_executive_summary": true,
    "include_remediation_steps": true,
    "include_appendices": true
  }
}
```

#### List Reports
```http
GET /api/v1/reports?type=vulnerability_assessment&page=1&limit=10
Authorization: Bearer <jwt_token>
```

## ⚙️ System Management

### System Status

#### Get System Health
```http
GET /api/v1/system/health
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "status": "healthy",
  "components": {
    "database": {
      "status": "up",
      "response_time": 12,
      "connections": 15
    },
    "ai_engine": {
      "status": "up",
      "model_loaded": true,
      "gpu_available": true
    },
    "tools": {
      "status": "up",
      "available_tools": 47,
      "failed_tools": 0
    }
  },
  "metrics": {
    "uptime": 86400,
    "cpu_usage": 23.5,
    "memory_usage": 62.1,
    "disk_usage": 45.8
  }
}
```

### Configuration Management

#### Get Configuration
```http
GET /api/v1/system/config
Authorization: Bearer <jwt_token>
```

#### Update Configuration
```http
PUT /api/v1/system/config
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "scanning": {
    "defaults": {
      "timeout": 600,
      "max_concurrent": 15
    }
  }
}
```

## 👥 User Management

### User Operations

#### List Users
```http
GET /api/v1/users?page=1&limit=20&role=security_analyst
Authorization: Bearer <jwt_token>
```

#### Create User
```http
POST /api/v1/users
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "username": "new_analyst",
  "email": "analyst@company.com",
  "full_name": "Security Analyst",
  "role": "security_analyst",
  "password": "secure_password123",
  "enabled": true
}
```

#### Update User
```http
PUT /api/v1/users/{user_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "role": "senior_analyst",
  "enabled": true
}
```

### Role and Permission Management

#### List Roles
```http
GET /api/v1/roles
Authorization: Bearer <jwt_token>
```

#### Create Custom Role
```http
POST /api/v1/roles
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "custom_analyst",
  "description": "Custom security analyst role",
  "permissions": [
    "scan:network",
    "scan:web:basic",
    "report:view",
    "report:create"
  ]
}
```

## 🔧 Tools and Integration

### Tool Management

#### List Available Tools
```http
GET /api/v1/tools
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "tools": [
    {
      "name": "nmap",
      "category": "network_scanner",
      "version": "7.91",
      "status": "available",
      "path": "/usr/bin/nmap",
      "capabilities": ["port_scanning", "service_detection", "os_detection"]
    }
  ]
}
```

#### Execute Tool Directly
```http
POST /api/v1/tools/{tool_name}/execute
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "target": "192.168.1.100",
  "arguments": ["-sS", "-sV", "-p", "1-1000"],
  "timeout": 300
}
```

### Natural Language Processing

#### Process Natural Language Command
```http
POST /api/v1/ai/process
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "input": "Perform a comprehensive security scan of 192.168.1.100 including service detection",
  "context": {
    "user_id": "analyst1",
    "workspace": "pentest_project"
  }
}
```

Response:
```json
{
  "intent": "security_scan",
  "entities": {
    "target": "192.168.1.100",
    "scan_type": "comprehensive",
    "options": ["service_detection"]
  },
  "generated_commands": [
    {
      "tool": "nmap",
      "arguments": ["-sS", "-sV", "-sC", "192.168.1.100"]
    }
  ],
  "execution_plan": {
    "steps": 1,
    "estimated_duration": 120
  }
}
```

## 🔌 WebSocket API

### Real-time Updates

#### Connect to WebSocket
```javascript
const ws = new WebSocket('wss://lewis.company.com/api/v1/ws');
ws.send(JSON.stringify({
  "type": "auth",
  "token": "jwt_token_here"
}));
```

#### Subscribe to Events
```javascript
// Subscribe to scan progress
ws.send(JSON.stringify({
  "type": "subscribe",
  "events": ["scan_progress", "vulnerability_found", "scan_completed"]
}));

// Handle events
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'scan_progress':
      console.log(`Scan progress: ${data.progress}%`);
      break;
    case 'vulnerability_found':
      console.log(`Vulnerability found: ${data.cve_id}`);
      break;
    case 'scan_completed':
      console.log(`Scan completed: ${data.scan_id}`);
      break;
  }
};
```

## 🐍 Python SDK

### Installation
```bash
pip install lewis-sdk
```

### Basic Usage

#### Initialize Client
```python
from lewis_sdk import LEWISClient

# Initialize with API key
client = LEWISClient(
    base_url="https://lewis.company.com",
    api_key="your-api-key"
)

# Initialize with username/password
client = LEWISClient(
    base_url="https://lewis.company.com",
    username="analyst",
    password="password"
)
```

#### Network Scanning
```python
# Start network scan
scan = client.scan_network(
    target="192.168.1.0/24",
    scan_type="comprehensive",
    include_services=True,
    include_os_detection=True
)

# Wait for completion
scan.wait_for_completion(timeout=600)

# Get results
results = scan.get_results()
print(f"Found {len(results.hosts)} hosts")

# Process results
for host in results.hosts:
    print(f"Host: {host.ip} ({host.hostname})")
    for port in host.ports:
        if port.state == "open":
            print(f"  Port {port.port}: {port.service}")
```

#### Web Application Scanning
```python
# Start web scan
scan = client.scan_web(
    target="https://example.com",
    include_ssl_analysis=True,
    include_vulnerability_scan=True
)

# Monitor progress
for progress in scan.progress():
    print(f"Progress: {progress.percentage}%")

# Get vulnerabilities
vulnerabilities = scan.get_vulnerabilities()
for vuln in vulnerabilities:
    print(f"Vulnerability: {vuln.title} (Severity: {vuln.severity})")
```

#### Natural Language Processing
```python
# Process natural language command
result = client.process_command(
    "Scan the network 192.168.1.0/24 for vulnerabilities"
)

# Execute the interpreted command
execution = result.execute()

# Get results
results = execution.get_results()
```

### Advanced SDK Features

#### Async Support
```python
import asyncio
from lewis_sdk import AsyncLEWISClient

async def main():
    client = AsyncLEWISClient(api_key="your-api-key")
    
    # Start multiple scans concurrently
    scans = await asyncio.gather(
        client.scan_network("192.168.1.0/24"),
        client.scan_network("10.0.0.0/24"),
        client.scan_web("https://example.com")
    )
    
    # Wait for all to complete
    results = await asyncio.gather(
        *[scan.wait_for_completion() for scan in scans]
    )

asyncio.run(main())
```

#### Batch Operations
```python
# Batch scan multiple targets
targets = ["192.168.1.100", "192.168.1.101", "192.168.1.102"]
batch_scan = client.create_batch_scan(targets)

# Monitor batch progress
for update in batch_scan.progress():
    print(f"Completed: {update.completed}/{update.total}")

# Get all results
all_results = batch_scan.get_all_results()
```

#### Custom Callbacks
```python
def on_vulnerability_found(vulnerability):
    if vulnerability.severity in ["high", "critical"]:
        print(f"ALERT: {vulnerability.title}")
        send_alert_email(vulnerability)

def on_scan_completed(scan):
    print(f"Scan {scan.id} completed")
    generate_report(scan)

# Register callbacks
client.on("vulnerability_found", on_vulnerability_found)
client.on("scan_completed", on_scan_completed)
```

## 📱 Integration Examples

### CI/CD Integration

#### GitHub Actions
```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Security Scan
      run: |
        curl -X POST \
          -H "Authorization: ApiKey ${{ secrets.LEWIS_API_KEY }}" \
          -H "Content-Type: application/json" \
          -d '{"target": "staging.example.com", "scan_type": "web"}' \
          https://lewis.company.com/api/v1/scan/web
```

#### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    stages {
        stage('Security Scan') {
            steps {
                script {
                    def response = httpRequest(
                        url: 'https://lewis.company.com/api/v1/scan/web',
                        httpMode: 'POST',
                        customHeaders: [[name: 'Authorization', value: "ApiKey ${env.LEWIS_API_KEY}"]],
                        requestBody: '{"target": "staging.example.com"}'
                    )
                    
                    def scanId = readJSON(text: response.content).scan_id
                    
                    // Wait for completion and fail build if high-risk vulnerabilities found
                    waitForScanCompletion(scanId)
                }
            }
        }
    }
}
```

### SIEM Integration

#### Splunk
```python
import splunklib.client as client

# Connect to Splunk
service = client.connect(host="splunk.company.com", username="admin", password="password")

# Get LEWIS scan results
lewis_client = LEWISClient(api_key="api_key")
scan_results = lewis_client.get_recent_scans()

# Send to Splunk
for result in scan_results:
    service.indexes["security"].submit(json.dumps(result))
```

#### ELK Stack
```python
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'elasticsearch.company.com', 'port': 9200}])

# Index LEWIS data
for vulnerability in scan_results.vulnerabilities:
    es.index(
        index="lewis-vulnerabilities",
        body={
            "timestamp": vulnerability.discovered_at,
            "host": vulnerability.host,
            "severity": vulnerability.severity,
            "cve_id": vulnerability.cve_id,
            "description": vulnerability.description
        }
    )
```

## 📚 Rate Limiting and Best Practices

### Rate Limits
- **Authentication**: 10 requests per minute
- **Scan Operations**: 5 concurrent scans per user
- **API Calls**: 1000 requests per hour per API key
- **WebSocket Connections**: 10 concurrent connections per user

### Best Practices
1. **Use appropriate timeouts**: Set reasonable timeouts for long-running operations
2. **Handle errors gracefully**: Implement retry logic with exponential backoff
3. **Paginate large results**: Use pagination for large datasets
4. **Cache responses**: Cache frequently accessed data to reduce API calls
5. **Use WebSockets for real-time updates**: Subscribe to relevant events instead of polling

### Error Handling Example
```python
import time
from lewis_sdk import LEWISClient, LEWISError

def robust_scan_with_retry(target, max_retries=3):
    client = LEWISClient(api_key="your-api-key")
    
    for attempt in range(max_retries):
        try:
            scan = client.scan_network(target)
            return scan.wait_for_completion()
        
        except LEWISError as e:
            if e.status_code == 429:  # Rate limited
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            elif e.status_code >= 500:  # Server error
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
            raise e
    
    raise Exception(f"Failed to complete scan after {max_retries} attempts")
```

---

**📝 API Reference Version:** 1.0.0  
**📅 Last Updated:** June 21, 2025  
**👨‍💻 Author:** [ZehraSec Team](https://www.zehrasec.com)
