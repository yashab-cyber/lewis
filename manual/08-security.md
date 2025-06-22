# LEWIS Security Guide

This guide covers security best practices, configuration, and implementation guidelines for LEWIS deployments.

## 🔒 Overview

Security is paramount in LEWIS design and deployment. This guide provides comprehensive security guidelines for administrators, developers, and users.

## 📋 Table of Contents

1. [Security Architecture](#security-architecture)
2. [Authentication & Authorization](#authentication--authorization)
3. [Data Protection](#data-protection)
4. [Network Security](#network-security)
5. [Deployment Security](#deployment-security)
6. [Operational Security](#operational-security)
7. [Compliance & Auditing](#compliance--auditing)
8. [Security Monitoring](#security-monitoring)

## 🏗️ Security Architecture

### Security-by-Design Principles

LEWIS follows these core security principles:

1. **Zero Trust Architecture**: Never trust, always verify
2. **Defense in Depth**: Multiple layers of security controls
3. **Principle of Least Privilege**: Minimal necessary access
4. **Secure by Default**: Secure configurations out-of-the-box
5. **Fail Secure**: Safe failure modes

### Security Components

```
┌─────────────────────────────────────────────────┐
│                 LEWIS Security                  │
├─────────────────────────────────────────────────┤
│ Authentication │ Authorization │ Encryption     │
├─────────────────────────────────────────────────┤
│ Input Validation │ Output Encoding │ Logging   │
├─────────────────────────────────────────────────┤
│ Session Management │ CSRF Protection │ XSS     │
├─────────────────────────────────────────────────┤
│ Rate Limiting │ IP Filtering │ Audit Trail     │
└─────────────────────────────────────────────────┘
```

## 🔐 Authentication & Authorization

### Multi-Factor Authentication (MFA)

```python
# security/mfa.py
import pyotp
import qrcode
from io import BytesIO
import base64

class MFAManager:
    def __init__(self):
        self.secret_key = pyotp.random_base32()
    
    def generate_qr_code(self, user_email, issuer="LEWIS"):
        """Generate QR code for MFA setup"""
        totp_uri = pyotp.totp.TOTP(self.secret_key).provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for web display
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return img_str
    
    def verify_token(self, token, secret_key):
        """Verify MFA token"""
        totp = pyotp.TOTP(secret_key)
        return totp.verify(token, valid_window=1)
```

### Role-Based Access Control (RBAC)

```python
# security/rbac.py
from enum import Enum
from typing import List, Dict, Set

class Permission(Enum):
    READ_SCANS = "read_scans"
    WRITE_SCANS = "write_scans"
    DELETE_SCANS = "delete_scans"
    ADMIN_USERS = "admin_users"
    ADMIN_SYSTEM = "admin_system"
    VIEW_REPORTS = "view_reports"
    GENERATE_REPORTS = "generate_reports"

class Role:
    def __init__(self, name: str, permissions: List[Permission]):
        self.name = name
        self.permissions = set(permissions)
    
    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions

class RBACManager:
    def __init__(self):
        self.roles = self._initialize_default_roles()
        self.user_roles: Dict[str, Set[str]] = {}
    
    def _initialize_default_roles(self) -> Dict[str, Role]:
        """Initialize default roles"""
        return {
            'admin': Role('admin', list(Permission)),
            'analyst': Role('analyst', [
                Permission.READ_SCANS,
                Permission.WRITE_SCANS,
                Permission.VIEW_REPORTS,
                Permission.GENERATE_REPORTS
            ]),
            'viewer': Role('viewer', [
                Permission.READ_SCANS,
                Permission.VIEW_REPORTS
            ]),
            'operator': Role('operator', [
                Permission.READ_SCANS,
                Permission.WRITE_SCANS,
                Permission.VIEW_REPORTS
            ])
        }
    
    def assign_role(self, user_id: str, role_name: str):
        """Assign role to user"""
        if role_name not in self.roles:
            raise ValueError(f"Role {role_name} does not exist")
        
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        
        self.user_roles[user_id].add(role_name)
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has permission"""
        if user_id not in self.user_roles:
            return False
        
        for role_name in self.user_roles[user_id]:
            role = self.roles[role_name]
            if role.has_permission(permission):
                return True
        
        return False
```

### JWT Token Management

```python
# security/jwt_manager.py
import jwt
import datetime
from typing import Dict, Optional

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry = 3600  # 1 hour
    
    def generate_token(self, user_id: str, roles: List[str]) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_id,
            'roles': roles,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.token_expiry),
            'iat': datetime.datetime.utcnow(),
            'iss': 'LEWIS'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh JWT token"""
        payload = self.verify_token(token)
        if not payload:
            return None
        
        # Generate new token with same user info
        return self.generate_token(
            payload['user_id'], 
            payload['roles']
        )
```

### Single Sign-On (SSO) Integration

```python
# security/sso.py
from flask import Flask, request, redirect, session
import requests
import base64
import json

class SAMLSSOMnager:
    def __init__(self, idp_url, sp_entity_id, cert_path):
        self.idp_url = idp_url
        self.sp_entity_id = sp_entity_id
        self.cert_path = cert_path
    
    def initiate_sso(self):
        """Initiate SSO authentication"""
        saml_request = self.create_saml_request()
        encoded_request = base64.b64encode(saml_request.encode()).decode()
        
        sso_url = f"{self.idp_url}?SAMLRequest={encoded_request}"
        return sso_url
    
    def process_sso_response(self, saml_response):
        """Process SSO response"""
        decoded_response = base64.b64decode(saml_response)
        
        # Validate SAML response
        if self.validate_saml_response(decoded_response):
            user_info = self.extract_user_info(decoded_response)
            return user_info
        
        return None

class OAuthManager:
    def __init__(self, client_id, client_secret, auth_url, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.token_url = token_url
    
    def get_authorization_url(self, redirect_uri, scope="openid"):
        """Get OAuth authorization URL"""
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': scope,
            'state': 'random_state_string'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{self.auth_url}?{query_string}"
    
    def exchange_code_for_token(self, code, redirect_uri):
        """Exchange authorization code for access token"""
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        
        response = requests.post(self.token_url, data=data)
        return response.json()
```

## 🛡️ Data Protection

### Encryption at Rest

```python
# security/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class EncryptionManager:
    def __init__(self, password: str = None):
        if password:
            self.key = self.derive_key(password)
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def derive_key(self, password: str, salt: bytes = None) -> bytes:
        """Derive encryption key from password"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt data"""
        encrypted_data = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data"""
        decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.cipher.decrypt(decoded_data)
        return decrypted_data.decode()
    
    def encrypt_file(self, file_path: str, output_path: str = None):
        """Encrypt file"""
        if output_path is None:
            output_path = f"{file_path}.encrypted"
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = self.cipher.encrypt(file_data)
        
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)
```

### Secure Data Storage

```python
# security/secure_storage.py
import sqlite3
import hashlib
from contextlib import contextmanager

class SecureDatabase:
    def __init__(self, db_path: str, encryption_key: str):
        self.db_path = db_path
        self.encryption_manager = EncryptionManager(encryption_key)
        self.init_database()
    
    def init_database(self):
        """Initialize secure database"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS secure_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_hash TEXT UNIQUE,
                    encrypted_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def store_data(self, data: str) -> str:
        """Store data securely"""
        # Hash data for integrity checking
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        
        # Encrypt data
        encrypted_data = self.encryption_manager.encrypt_data(data)
        
        with self.get_connection() as conn:
            conn.execute(
                'INSERT INTO secure_data (data_hash, encrypted_data) VALUES (?, ?)',
                (data_hash, encrypted_data)
            )
            conn.commit()
        
        return data_hash
    
    def retrieve_data(self, data_hash: str) -> str:
        """Retrieve data securely"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT encrypted_data FROM secure_data WHERE data_hash = ?',
                (data_hash,)
            )
            result = cursor.fetchone()
        
        if result:
            encrypted_data = result[0]
            return self.encryption_manager.decrypt_data(encrypted_data)
        
        return None
```

### Data Masking and Anonymization

```python
# security/data_masking.py
import re
import hashlib
import random
import string

class DataMasker:
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'phone': r'\b\d{3}-\d{3}-\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
    
    def mask_data(self, text: str, mask_type: str = 'partial') -> str:
        """Mask sensitive data in text"""
        masked_text = text
        
        for data_type, pattern in self.patterns.items():
            if mask_type == 'partial':
                masked_text = self.partial_mask(masked_text, pattern, data_type)
            elif mask_type == 'full':
                masked_text = self.full_mask(masked_text, pattern, data_type)
            elif mask_type == 'hash':
                masked_text = self.hash_mask(masked_text, pattern)
        
        return masked_text
    
    def partial_mask(self, text: str, pattern: str, data_type: str) -> str:
        """Apply partial masking"""
        def mask_match(match):
            value = match.group(0)
            if data_type == 'email':
                local, domain = value.split('@')
                masked_local = local[:2] + '*' * (len(local) - 2)
                return f"{masked_local}@{domain}"
            elif data_type == 'ip_address':
                parts = value.split('.')
                return f"{parts[0]}.{parts[1]}.*.* "
            else:
                return value[:4] + '*' * (len(value) - 4)
        
        return re.sub(pattern, mask_match, text)
    
    def full_mask(self, text: str, pattern: str, placeholder: str) -> str:
        """Apply full masking"""
        placeholder_map = {
            'email': '[EMAIL]',
            'ip_address': '[IP_ADDRESS]',
            'phone': '[PHONE]',
            'ssn': '[SSN]',
            'credit_card': '[CREDIT_CARD]'
        }
        return re.sub(pattern, placeholder_map.get(placeholder, '[MASKED]'), text)
    
    def hash_mask(self, text: str, pattern: str) -> str:
        """Apply hash-based masking"""
        def hash_match(match):
            value = match.group(0)
            hash_value = hashlib.sha256(value.encode()).hexdigest()[:8]
            return f"[HASH:{hash_value}]"
        
        return re.sub(pattern, hash_match, text)
```

## 🌐 Network Security

### TLS/SSL Configuration

```python
# security/tls_config.py
import ssl
import socket
from typing import Dict, List

class TLSConfig:
    def __init__(self):
        self.min_tls_version = ssl.TLSVersion.TLSv1_2
        self.ciphers = [
            'ECDHE+AESGCM',
            'ECDHE+CHACHA20',
            'DHE+AESGCM',
            'DHE+CHACHA20',
            '!aNULL',
            '!MD5',
            '!DSS'
        ]
    
    def create_secure_context(self, cert_file: str, key_file: str) -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        
        # Set minimum TLS version
        context.minimum_version = self.min_tls_version
        
        # Load certificate and key
        context.load_cert_chain(cert_file, key_file)
        
        # Set secure ciphers
        context.set_ciphers(':'.join(self.ciphers))
        
        # Additional security settings
        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED
        
        return context
    
    def validate_certificate(self, hostname: str, port: int) -> Dict:
        """Validate SSL certificate"""
        context = ssl.create_default_context()
        
        try:
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'valid': True,
                        'subject': cert.get('subject'),
                        'issuer': cert.get('issuer'),
                        'not_after': cert.get('notAfter'),
                        'serial_number': cert.get('serialNumber')
                    }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
```

### IP Filtering and Rate Limiting

```python
# security/network_security.py
import time
from collections import defaultdict, deque
from ipaddress import ip_network, ip_address
from typing import List, Dict

class IPFilter:
    def __init__(self):
        self.whitelist: List[str] = []
        self.blacklist: List[str] = []
        self.rate_limits: Dict[str, deque] = defaultdict(deque)
        self.rate_limit_window = 60  # 1 minute
        self.rate_limit_threshold = 100  # requests per minute
    
    def add_to_whitelist(self, ip_range: str):
        """Add IP range to whitelist"""
        self.whitelist.append(ip_range)
    
    def add_to_blacklist(self, ip_range: str):
        """Add IP range to blacklist"""
        self.blacklist.append(ip_range)
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if IP is allowed"""
        client_addr = ip_address(client_ip)
        
        # Check blacklist first
        for blocked_range in self.blacklist:
            if client_addr in ip_network(blocked_range, strict=False):
                return False
        
        # Check whitelist
        for allowed_range in self.whitelist:
            if client_addr in ip_network(allowed_range, strict=False):
                return True
        
        # If whitelist is empty, allow by default (unless blacklisted)
        return len(self.whitelist) == 0
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """Check rate limiting for IP"""
        current_time = time.time()
        
        # Clean old entries
        self.rate_limits[client_ip] = deque([
            timestamp for timestamp in self.rate_limits[client_ip]
            if current_time - timestamp < self.rate_limit_window
        ])
        
        # Check if under rate limit
        if len(self.rate_limits[client_ip]) >= self.rate_limit_threshold:
            return False
        
        # Add current request
        self.rate_limits[client_ip].append(current_time)
        return True

class WAFRules:
    def __init__(self):
        self.sql_injection_patterns = [
            r"(\%27)|(\')|(\-\-)|(%23)|(#)",
            r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(%23)|(#))",
            r"union.*select.*from",
            r"insert.*into.*values",
            r"select.*from.*where"
        ]
        
        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>"
        ]
    
    def scan_for_attacks(self, request_data: str) -> List[str]:
        """Scan request for attack patterns"""
        threats = []
        
        # Check for SQL injection
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, request_data, re.IGNORECASE):
                threats.append("SQL Injection")
                break
        
        # Check for XSS
        for pattern in self.xss_patterns:
            if re.search(pattern, request_data, re.IGNORECASE):
                threats.append("Cross-Site Scripting (XSS)")
                break
        
        return threats
```

## 🚀 Deployment Security

### Container Security

```dockerfile
# Dockerfile.secure
FROM python:3.9-slim as base

# Create non-root user
RUN useradd --create-home --shell /bin/bash lewis

# Security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R lewis:lewis /app

# Switch to non-root user
USER lewis

# Set security-focused environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run application
EXPOSE 8080
CMD ["python", "lewis.py", "--production"]
```

### Kubernetes Security

```yaml
# k8s/security-config.yaml
apiVersion: v1
kind: SecurityContext
metadata:
  name: lewis-security-context
spec:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: lewis-network-policy
spec:
  podSelector:
    matchLabels:
      app: lewis
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: allowed-namespace
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS only
```

### Environment Hardening

```bash
#!/bin/bash
# scripts/harden_environment.sh

# System hardening script for LEWIS deployment

echo "Starting LEWIS environment hardening..."

# Update system
apt-get update && apt-get upgrade -y

# Install security tools
apt-get install -y fail2ban ufw auditd

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 8080/tcp  # LEWIS web interface
ufw enable

# Configure fail2ban
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log

[lewis-web]
enabled = true
port = 8080
filter = lewis-web
logpath = /var/log/lewis/access.log
maxretry = 5
EOF

# Create custom fail2ban filter for LEWIS
cat > /etc/fail2ban/filter.d/lewis-web.conf << EOF
[Definition]
failregex = ^<HOST> .* ".*" 4\d\d \d+
ignoreregex =
EOF

# Set file permissions
chmod 600 /etc/lewis/config.yaml
chmod 700 /var/log/lewis/
chown -R lewis:lewis /opt/lewis/

# Configure audit logging
cat >> /etc/audit/audit.rules << EOF
# LEWIS audit rules
-w /opt/lewis/ -p wa -k lewis_files
-w /etc/lewis/ -p wa -k lewis_config
-w /var/log/lewis/ -p wa -k lewis_logs
EOF

# Restart services
systemctl restart fail2ban
systemctl restart ufw
systemctl restart auditd

echo "Environment hardening completed."
```

## 🔍 Operational Security

### Security Monitoring

```python
# security/monitoring.py
import logging
import json
from datetime import datetime
from typing import Dict, List

class SecurityMonitor:
    def __init__(self):
        self.setup_logging()
        self.security_events = []
        self.threat_indicators = []
    
    def setup_logging(self):
        """Setup security logging"""
        self.security_logger = logging.getLogger('lewis.security')
        handler = logging.FileHandler('/var/log/lewis/security.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.security_logger.addHandler(handler)
        self.security_logger.setLevel(logging.INFO)
    
    def log_security_event(self, event_type: str, details: Dict):
        """Log security event"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details,
            'severity': self.calculate_severity(event_type, details)
        }
        
        self.security_events.append(event)
        self.security_logger.info(json.dumps(event))
        
        # Check for immediate threats
        if event['severity'] == 'critical':
            self.handle_critical_event(event)
    
    def calculate_severity(self, event_type: str, details: Dict) -> str:
        """Calculate event severity"""
        severity_map = {
            'authentication_failure': 'medium',
            'authorization_failure': 'high',
            'data_access_violation': 'high',
            'system_intrusion': 'critical',
            'malware_detected': 'critical',
            'data_exfiltration': 'critical'
        }
        
        base_severity = severity_map.get(event_type, 'low')
        
        # Escalate based on context
        if details.get('repeated_attempts', 0) > 5:
            return 'critical'
        elif details.get('admin_account', False):
            return 'high'
        
        return base_severity
    
    def handle_critical_event(self, event: Dict):
        """Handle critical security events"""
        # Send immediate alerts
        self.send_alert(event)
        
        # Trigger automated response
        self.trigger_incident_response(event)
    
    def detect_anomalies(self, user_activity: List[Dict]) -> List[Dict]:
        """Detect anomalous user activity"""
        anomalies = []
        
        for activity in user_activity:
            # Check for unusual access patterns
            if self.is_unusual_access_time(activity):
                anomalies.append({
                    'type': 'unusual_access_time',
                    'activity': activity,
                    'risk_score': 0.6
                })
            
            # Check for privilege escalation
            if self.is_privilege_escalation(activity):
                anomalies.append({
                    'type': 'privilege_escalation',
                    'activity': activity,
                    'risk_score': 0.8
                })
        
        return anomalies
```

### Incident Response

```python
# security/incident_response.py
from enum import Enum
from typing import Dict, List
import smtplib
from email.mime.text import MIMEText

class IncidentSeverity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class IncidentResponse:
    def __init__(self):
        self.response_team = [
            'security@company.com',
            'admin@company.com'
        ]
        self.escalation_matrix = {
            IncidentSeverity.CRITICAL: ['ciso@company.com', 'ceo@company.com'],
            IncidentSeverity.HIGH: ['security-lead@company.com'],
            IncidentSeverity.MEDIUM: ['security-team@company.com'],
            IncidentSeverity.LOW: ['security-team@company.com']
        }
    
    def handle_incident(self, incident: Dict):
        """Handle security incident"""
        severity = IncidentSeverity(incident['severity_level'])
        
        # Log incident
        self.log_incident(incident)
        
        # Notify appropriate teams
        self.notify_teams(incident, severity)
        
        # Execute automated response
        self.execute_automated_response(incident, severity)
        
        # Create incident ticket
        self.create_incident_ticket(incident)
    
    def execute_automated_response(self, incident: Dict, severity: IncidentSeverity):
        """Execute automated incident response"""
        response_actions = {
            IncidentSeverity.CRITICAL: [
                self.block_suspicious_ips,
                self.disable_compromised_accounts,
                self.isolate_affected_systems,
                self.backup_forensic_data
            ],
            IncidentSeverity.HIGH: [
                self.block_suspicious_ips,
                self.increase_monitoring,
                self.notify_administrators
            ],
            IncidentSeverity.MEDIUM: [
                self.log_detailed_activity,
                self.increase_monitoring
            ],
            IncidentSeverity.LOW: [
                self.log_incident
            ]
        }
        
        actions = response_actions.get(severity, [])
        for action in actions:
            try:
                action(incident)
            except Exception as e:
                self.log_error(f"Response action failed: {e}")
    
    def block_suspicious_ips(self, incident: Dict):
        """Block suspicious IP addresses"""
        suspicious_ips = incident.get('source_ips', [])
        
        for ip in suspicious_ips:
            # Add to firewall block list
            self.add_to_firewall_blocklist(ip)
            
            # Update WAF rules
            self.update_waf_rules(ip)
    
    def disable_compromised_accounts(self, incident: Dict):
        """Disable compromised user accounts"""
        compromised_accounts = incident.get('affected_accounts', [])
        
        for account in compromised_accounts:
            # Disable account
            self.disable_user_account(account)
            
            # Revoke active sessions
            self.revoke_user_sessions(account)
            
            # Reset password
            self.force_password_reset(account)
```

## 📊 Compliance & Auditing

### Compliance Framework

```python
# security/compliance.py
from abc import ABC, abstractmethod
from typing import Dict, List

class ComplianceFramework(ABC):
    """Base class for compliance frameworks"""
    
    @abstractmethod
    def get_requirements(self) -> List[Dict]:
        """Get compliance requirements"""
        pass
    
    @abstractmethod
    def assess_compliance(self, system_config: Dict) -> Dict:
        """Assess system compliance"""
        pass

class SOC2Compliance(ComplianceFramework):
    def get_requirements(self) -> List[Dict]:
        """SOC 2 Type II requirements"""
        return [
            {
                'control': 'CC6.1',
                'description': 'Logical and physical access controls',
                'category': 'Security'
            },
            {
                'control': 'CC6.2',
                'description': 'System backup and recovery',
                'category': 'Availability'
            },
            {
                'control': 'CC6.3',
                'description': 'Data encryption in transit and at rest',
                'category': 'Confidentiality'
            }
        ]
    
    def assess_compliance(self, system_config: Dict) -> Dict:
        """Assess SOC 2 compliance"""
        results = {
            'framework': 'SOC 2',
            'assessment_date': datetime.utcnow().isoformat(),
            'controls': [],
            'overall_score': 0
        }
        
        requirements = self.get_requirements()
        passed_controls = 0
        
        for req in requirements:
            control_result = self.assess_control(req, system_config)
            results['controls'].append(control_result)
            
            if control_result['status'] == 'compliant':
                passed_controls += 1
        
        results['overall_score'] = (passed_controls / len(requirements)) * 100
        return results

class GDPRCompliance(ComplianceFramework):
    def get_requirements(self) -> List[Dict]:
        """GDPR requirements"""
        return [
            {
                'article': 'Article 25',
                'description': 'Data protection by design and by default',
                'category': 'Privacy'
            },
            {
                'article': 'Article 32',
                'description': 'Security of processing',
                'category': 'Security'
            },
            {
                'article': 'Article 35',
                'description': 'Data protection impact assessment',
                'category': 'Privacy'
            }
        ]
    
    def assess_compliance(self, system_config: Dict) -> Dict:
        """Assess GDPR compliance"""
        # Implementation similar to SOC2Compliance
        pass
```

### Audit Logging

```python
# security/audit_logging.py
import json
import hashlib
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    def __init__(self):
        self.audit_log_path = '/var/log/lewis/audit.log'
        self.setup_logging()
    
    def setup_logging(self):
        """Setup audit logging with integrity protection"""
        self.audit_logger = logging.getLogger('lewis.audit')
        handler = logging.FileHandler(self.audit_log_path)
        formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        )
        handler.setFormatter(formatter)
        self.audit_logger.addHandler(handler)
        self.audit_logger.setLevel(logging.INFO)
    
    def log_event(self, event_type: str, user_id: str, details: Dict[str, Any]):
        """Log audit event with integrity hash"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details,
            'session_id': self.get_session_id(),
            'source_ip': self.get_source_ip()
        }
        
        # Add integrity hash
        event_json = json.dumps(event, sort_keys=True)
        event['integrity_hash'] = hashlib.sha256(
            event_json.encode()
        ).hexdigest()
        
        # Log the event
        self.audit_logger.info(json.dumps(event))
    
    def verify_log_integrity(self) -> bool:
        """Verify audit log integrity"""
        with open(self.audit_log_path, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line.split(' - AUDIT - ')[1])
                    
                    # Extract and verify hash
                    stored_hash = event.pop('integrity_hash')
                    calculated_hash = hashlib.sha256(
                        json.dumps(event, sort_keys=True).encode()
                    ).hexdigest()
                    
                    if stored_hash != calculated_hash:
                        return False
                        
                except Exception:
                    continue
        
        return True
```

## 📈 Security Monitoring

### Real-time Monitoring

```python
# security/realtime_monitoring.py
import asyncio
import websocket
from datetime import datetime, timedelta
from typing import Dict, List

class RealTimeSecurityMonitor:
    def __init__(self):
        self.active_connections = set()
        self.threat_feeds = []
        self.alert_thresholds = {
            'failed_logins': 5,
            'unusual_traffic': 100,
            'privilege_escalation': 1
        }
    
    async def monitor_security_events(self):
        """Monitor security events in real-time"""
        while True:
            try:
                # Check for security events
                events = await self.collect_security_events()
                
                # Analyze events
                for event in events:
                    await self.analyze_event(event)
                
                # Check threat intelligence
                await self.check_threat_intelligence()
                
                # Sleep before next check
                await asyncio.sleep(5)
                
            except Exception as e:
                logging.error(f"Monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def analyze_event(self, event: Dict):
        """Analyze security event for threats"""
        event_type = event.get('type')
        
        if event_type == 'failed_login':
            await self.handle_failed_login(event)
        elif event_type == 'privilege_escalation':
            await self.handle_privilege_escalation(event)
        elif event_type == 'data_access':
            await self.handle_data_access(event)
    
    async def handle_failed_login(self, event: Dict):
        """Handle failed login attempts"""
        user_id = event.get('user_id')
        source_ip = event.get('source_ip')
        
        # Count recent failed attempts
        recent_failures = await self.count_recent_events(
            'failed_login', 
            {'user_id': user_id}, 
            timedelta(minutes=15)
        )
        
        if recent_failures >= self.alert_thresholds['failed_logins']:
            await self.trigger_alert({
                'type': 'brute_force_attack',
                'user_id': user_id,
                'source_ip': source_ip,
                'attempts': recent_failures
            })
```

### Threat Intelligence Integration

```python
# security/threat_intelligence.py
import requests
import json
from typing import Dict, List

class ThreatIntelligence:
    def __init__(self):
        self.threat_feeds = [
            {
                'name': 'VirusTotal',
                'url': 'https://www.virustotal.com/vtapi/v2/',
                'api_key': 'your_api_key',
                'type': 'hash_lookup'
            },
            {
                'name': 'AbuseIPDB',
                'url': 'https://api.abuseipdb.com/api/v2/',
                'api_key': 'your_api_key',
                'type': 'ip_reputation'
            }
        ]
    
    def check_ip_reputation(self, ip_address: str) -> Dict:
        """Check IP reputation across threat feeds"""
        results = {}
        
        for feed in self.threat_feeds:
            if feed['type'] == 'ip_reputation':
                try:
                    result = self.query_threat_feed(feed, ip_address)
                    results[feed['name']] = result
                except Exception as e:
                    results[feed['name']] = {'error': str(e)}
        
        return results
    
    def check_file_hash(self, file_hash: str) -> Dict:
        """Check file hash reputation"""
        results = {}
        
        for feed in self.threat_feeds:
            if feed['type'] == 'hash_lookup':
                try:
                    result = self.query_threat_feed(feed, file_hash)
                    results[feed['name']] = result
                except Exception as e:
                    results[feed['name']] = {'error': str(e)}
        
        return results
    
    def query_threat_feed(self, feed: Dict, indicator: str) -> Dict:
        """Query individual threat feed"""
        if feed['name'] == 'VirusTotal':
            return self.query_virustotal(feed, indicator)
        elif feed['name'] == 'AbuseIPDB':
            return self.query_abuseipdb(feed, indicator)
        
        return {}
    
    def query_virustotal(self, feed: Dict, file_hash: str) -> Dict:
        """Query VirusTotal API"""
        url = f"{feed['url']}file/report"
        params = {
            'apikey': feed['api_key'],
            'resource': file_hash
        }
        
        response = requests.get(url, params=params)
        return response.json()
    
    def query_abuseipdb(self, feed: Dict, ip_address: str) -> Dict:
        """Query AbuseIPDB API"""
        url = f"{feed['url']}check"
        headers = {
            'Key': feed['api_key'],
            'Accept': 'application/json'
        }
        params = {
            'ipAddress': ip_address,
            'maxAgeInDays': 90
        }
        
        response = requests.get(url, headers=headers, params=params)
        return response.json()
```

## 🔧 Security Configuration

### Secure Configuration Templates

```yaml
# config/security.yaml
security:
  authentication:
    method: "multi_factor"
    session_timeout: 3600
    max_login_attempts: 3
    lockout_duration: 1800
    
  authorization:
    rbac_enabled: true
    default_role: "viewer"
    admin_approval_required: true
    
  encryption:
    algorithm: "AES-256-GCM"
    key_rotation_interval: 2592000  # 30 days
    encrypt_at_rest: true
    encrypt_in_transit: true
    
  network:
    allowed_ips:
      - "10.0.0.0/8"
      - "192.168.0.0/16"
    blocked_ips: []
    rate_limit: 100
    rate_limit_window: 60
    
  monitoring:
    audit_logging: true
    security_events: true
    threat_detection: true
    real_time_monitoring: true
    
  compliance:
    frameworks:
      - "SOC2"
      - "GDPR"
      - "ISO27001"
    data_retention: 2555  # 7 years
    privacy_controls: true
```

---

**Next:** [Performance Guide](09-performance.md) | **Previous:** [Integration Guide](07-integration.md)

---
*This guide is part of the LEWIS documentation. For more information, visit the [main documentation](README.md).*
