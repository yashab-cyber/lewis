"""
Security Manager for LEWIS
Handles authentication, authorization, and security policies
"""

import hashlib
import jwt
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set
import re
import ipaddress

class SecurityManager:
    """
    Security manager for LEWIS
    Handles user authentication, command authorization, and security policies
    """
    
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        
        # Security configuration
        self.jwt_secret = settings.get("security.jwt_secret", "default-secret")
        self.session_timeout = settings.get("security.session_timeout", 3600)
        self.max_failed_attempts = settings.get("security.max_failed_attempts", 5)
        
        # Allowed IP ranges
        self.allowed_ips = settings.get("security.allowed_ips", [])
        
        # Active sessions
        self.active_sessions = {}
        self.failed_attempts = {}
        
        # Command restrictions
        self._initialize_security_policies()
        
        # Authorized targets
        self.authorized_targets = set()
        
    def _initialize_security_policies(self):
        """Initialize security policies and restrictions"""
        # Dangerous commands that require special authorization
        self.dangerous_commands = {
            "exploitation": ["metasploit", "msfconsole", "exploit"],
            "privilege_escalation": ["sudo", "su", "setuid"],
            "system_modification": ["rm", "del", "format", "mkfs"],
            "network_attacks": ["ddos", "dos", "flood"]
        }
        
        # Restricted file paths
        self.restricted_paths = [
            "/etc/passwd", "/etc/shadow", "/etc/hosts",
            "C:\\Windows\\System32", "C:\\Users\\Administrator"
        ]
        
        # Blocked IP ranges (internal networks, localhost)
        self.blocked_targets = [
            "127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
            "169.254.0.0/16", "::1/128", "fc00::/7"
        ]
        
        # Safe target patterns
        self.safe_target_patterns = [
            r".*\.testfire\.net$",
            r".*\.dvwa\..*$",
            r".*\.hackthebox\..*$",
            r".*\.vulnhub\..*$"
        ]
    
    def authenticate_user(
        self, 
        username: str, 
        password: str, 
        ip_address: str = None
    ) -> Dict[str, Any]:
        """
        Authenticate user credentials
        
        Args:
            username: Username
            password: Password
            ip_address: Client IP address
            
        Returns:
            Authentication result with token if successful
        """
        try:
            # Check IP whitelist if configured
            if self.allowed_ips and ip_address:
                if not self._is_ip_allowed(ip_address):
                    self.logger.warning(f"🚫 Authentication blocked from IP: {ip_address}")
                    return {"success": False, "error": "IP address not allowed"}
            
            # Check failed attempts
            if self._is_account_locked(username):
                return {"success": False, "error": "Account temporarily locked"}
            
            # Validate credentials (simplified - in real implementation, check against database)
            if self._validate_credentials(username, password):
                # Generate JWT token
                token = self._generate_jwt_token(username)
                
                # Create session
                session_id = self._create_session(username, ip_address)
                
                # Reset failed attempts
                self.failed_attempts.pop(username, None)
                
                self.logger.info(f"✅ User authenticated: {username}")
                
                return {
                    "success": True,
                    "token": token,
                    "session_id": session_id,
                    "expires_at": datetime.utcnow() + timedelta(seconds=self.session_timeout)
                }
            else:
                # Record failed attempt
                self._record_failed_attempt(username)
                
                self.logger.warning(f"❌ Authentication failed for user: {username}")
                return {"success": False, "error": "Invalid credentials"}
                
        except Exception as e:
            self.logger.error(f"❌ Authentication error: {e}")
            return {"success": False, "error": "Authentication system error"}
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """Validate JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            
            # Check expiration
            if payload.get("exp", 0) < time.time():
                return {"valid": False, "error": "Token expired"}
            
            return {"valid": True, "user": payload.get("user")}
            
        except jwt.ExpiredSignatureError:
            return {"valid": False, "error": "Token expired"}
        except jwt.InvalidTokenError:
            return {"valid": False, "error": "Invalid token"}
    
    def is_command_allowed(self, command: str, user_id: str) -> bool:
        """
        Check if command is allowed for user
        
        Args:
            command: Command to check
            user_id: User identifier
            
        Returns:
            True if command is allowed
        """
        try:
            # Check for dangerous commands
            command_lower = command.lower()
            
            for category, dangerous_cmds in self.dangerous_commands.items():
                for dangerous_cmd in dangerous_cmds:
                    if dangerous_cmd in command_lower:
                        if not self._is_user_authorized_for_category(user_id, category):
                            self.logger.warning(
                                f"🚫 Command blocked for user {user_id}: {command[:50]}..."
                            )
                            return False
            
            # Check for restricted file paths
            for restricted_path in self.restricted_paths:
                if restricted_path.lower() in command_lower:
                    self.logger.warning(
                        f"🚫 Restricted path access blocked for user {user_id}: {restricted_path}"
                    )
                    return False
            
            # Basic command validation
            if self._contains_malicious_patterns(command):
                self.logger.warning(f"🚫 Malicious pattern detected in command: {command[:50]}...")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking command authorization: {e}")
            return False
    
    def is_target_allowed(self, target: str, user_id: str) -> bool:
        """
        Check if target is allowed for scanning/testing
        
        Args:
            target: Target IP/domain
            user_id: User identifier
            
        Returns:
            True if target is allowed
        """
        try:
            # Check if target is in authorized list
            if target in self.authorized_targets:
                return True
            
            # Check safe target patterns
            for pattern in self.safe_target_patterns:
                if re.match(pattern, target, re.IGNORECASE):
                    return True
            
            # Check blocked targets
            if self._is_target_blocked(target):
                self.logger.warning(f"🚫 Blocked target: {target} for user {user_id}")
                return False
            
            # For real implementation, check against authorized target database
            # For now, allow external targets but log them
            self.logger.info(f"🎯 Target scan authorized: {target} for user {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking target authorization: {e}")
            return False
    
    def is_exploitation_allowed(self, user_id: str) -> bool:
        """Check if user is authorized for exploitation activities"""
        # In real implementation, check user permissions from database
        # For now, require explicit authorization
        return user_id in ["admin", "pentest_lead"]
    
    def add_authorized_target(self, target: str, user_id: str) -> bool:
        """Add target to authorized list"""
        try:
            if self._validate_target_format(target):
                self.authorized_targets.add(target)
                self.logger.info(f"✅ Target authorized: {target} by user {user_id}")
                return True
            else:
                self.logger.warning(f"❌ Invalid target format: {target}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error authorizing target: {e}")
            return False
    
    def get_active_users_count(self) -> int:
        """Get count of active users"""
        active_count = 0
        current_time = time.time()
        
        for session in self.active_sessions.values():
            if session.get("expires_at", 0) > current_time:
                active_count += 1
        
        return active_count
    
    def log_security_event(self, event_type: str, user_id: str, details: Dict[str, Any]):
        """Log security event"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details
        }
        
        self.logger.warning(f"🔐 Security event: {event_type} - User: {user_id}")
        # In real implementation, save to security audit log
    
    # Private methods
    def _is_ip_allowed(self, ip_address: str) -> bool:
        """Check if IP address is in allowed list"""
        try:
            client_ip = ipaddress.ip_address(ip_address)
            for allowed_range in self.allowed_ips:
                if client_ip in ipaddress.ip_network(allowed_range):
                    return True
            return False
        except:
            return False
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to failed attempts"""
        if username not in self.failed_attempts:
            return False
        
        attempts = self.failed_attempts[username]
        return attempts.get("count", 0) >= self.max_failed_attempts
    
    def _validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials"""
        # Simplified validation - in real implementation, check against database
        # For demo purposes, accept any non-empty credentials
        return bool(username and password)
    
    def _generate_jwt_token(self, username: str) -> str:
        """Generate JWT token for user"""
        payload = {
            "user": username,
            "iat": time.time(),
            "exp": time.time() + self.session_timeout
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    def _create_session(self, username: str, ip_address: str) -> str:
        """Create user session"""
        session_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
        
        self.active_sessions[session_id] = {
            "username": username,
            "ip_address": ip_address,
            "created_at": time.time(),
            "expires_at": time.time() + self.session_timeout
        }
        
        return session_id
    
    def _record_failed_attempt(self, username: str):
        """Record failed authentication attempt"""
        if username not in self.failed_attempts:
            self.failed_attempts[username] = {"count": 0, "last_attempt": time.time()}
        
        self.failed_attempts[username]["count"] += 1
        self.failed_attempts[username]["last_attempt"] = time.time()
    
    def _is_user_authorized_for_category(self, user_id: str, category: str) -> bool:
        """Check if user is authorized for specific command category"""
        # In real implementation, check user permissions from database
        # For now, use simple role-based authorization
        admin_users = ["admin", "pentest_lead"]
        
        if category == "exploitation":
            return user_id in admin_users
        
        return True  # Allow other categories for now
    
    def _contains_malicious_patterns(self, command: str) -> bool:
        """Check for malicious patterns in command"""
        malicious_patterns = [
            r";\s*rm\s+-rf\s+/",  # Destructive commands
            r">\s*/dev/null\s*2>&1",  # Output redirection to hide traces
            r"\|\s*nc\s+",  # Netcat piping
            r"curl\s+.*\|\s*sh",  # Download and execute
            r"wget\s+.*\|\s*sh"  # Download and execute
        ]
        
        for pattern in malicious_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        
        return False
    
    def _is_target_blocked(self, target: str) -> bool:
        """Check if target is in blocked list"""
        try:
            # Try to parse as IP address
            target_ip = ipaddress.ip_address(target)
            
            for blocked_range in self.blocked_targets:
                if target_ip in ipaddress.ip_network(blocked_range):
                    return True
            
            return False
            
        except ipaddress.AddressValueError:
            # Not an IP address, check domain patterns
            blocked_domains = ["localhost", "127.0.0.1", "0.0.0.0"]
            return target.lower() in blocked_domains
    
    def _validate_target_format(self, target: str) -> bool:
        """Validate target format"""
        # IP address pattern
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        
        # Domain pattern
        domain_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
        
        # URL pattern
        url_pattern = r"^https?://[^\s/$.?#].[^\s]*$"
        
        return (re.match(ip_pattern, target) or 
                re.match(domain_pattern, target) or 
                re.match(url_pattern, target))
