#!/usr/bin/env python3
"""
LEWIS Threat Detection & Response Module
Real-time threat detection, analysis, and automated response capabilities
"""

import asyncio
import json
import re
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from enum import Enum
import ipaddress
import subprocess
import psutil
import socket

from config.settings import Settings
from utils.logger import Logger
from storage.database_manager import DatabaseManager

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatType(Enum):
    MALWARE = "malware"
    PHISHING = "phishing"
    BRUTE_FORCE = "brute_force"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    DDoS = "ddos"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DATA_EXFILTRATION = "data_exfiltration"
    LATERAL_MOVEMENT = "lateral_movement"
    PERSISTENCE = "persistence"

@dataclass
class ThreatIndicator:
    ioc_type: str  # IP, domain, hash, etc.
    value: str
    threat_level: ThreatLevel
    description: str
    source: str
    first_seen: datetime
    last_seen: datetime
    confidence: float

@dataclass
class ThreatEvent:
    event_id: str
    timestamp: datetime
    threat_type: ThreatType
    threat_level: ThreatLevel
    source_ip: str
    target_ip: str
    port: int
    protocol: str
    description: str
    indicators: List[ThreatIndicator]
    mitre_technique: str = None
    mitre_tactic: str = None
    raw_data: Dict[str, Any] = None

@dataclass
class ResponseAction:
    action_id: str
    action_type: str  # block_ip, isolate_host, alert, etc.
    target: str
    timestamp: datetime
    status: str
    details: str

class ThreatDetectionEngine:
    """Advanced threat detection and response system"""
    
    def __init__(self, settings: Settings, logger: Logger):
        self.settings = settings
        self.logger = logger
        self.db_manager = DatabaseManager(settings, logger)
        
        # Detection configuration
        self.detection_rules = {}
        self.threat_indicators = {}
        self.active_threats = deque(maxlen=1000)
        self.response_actions = deque(maxlen=500)
        
        # Network monitoring
        self.monitored_interfaces = settings.get("detection", {}).get("interfaces", ["eth0", "wlan0"])
        self.detection_enabled = settings.get("detection", {}).get("enabled", True)
        
        # Threat intelligence feeds
        self.threat_feeds = settings.get("detection", {}).get("threat_feeds", [])
        
        # Response configuration
        self.auto_response_enabled = settings.get("detection", {}).get("auto_response", False)
        self.response_threshold = ThreatLevel.HIGH
        
        # Load detection rules
        self._load_detection_rules()
        
        # Initialize threat intelligence
        asyncio.create_task(self._initialize_threat_intelligence())
    
    def _load_detection_rules(self):
        """Load threat detection rules"""
        
        # Basic detection rules (YARA-style rules could be added here)
        self.detection_rules = {
            "brute_force_ssh": {
                "pattern": r"Failed password.*ssh",
                "threshold": 10,  # attempts
                "time_window": 300,  # seconds
                "threat_type": ThreatType.BRUTE_FORCE,
                "threat_level": ThreatLevel.HIGH
            },
            "sql_injection": {
                "pattern": r"(union.*select|drop.*table|exec.*xp_|sp_executesql)",
                "threshold": 1,
                "time_window": 60,
                "threat_type": ThreatType.SQL_INJECTION,
                "threat_level": ThreatLevel.HIGH
            },
            "xss_attempt": {
                "pattern": r"(<script|javascript:|onload=|onerror=)",
                "threshold": 1,
                "time_window": 60,
                "threat_type": ThreatType.XSS,
                "threat_level": ThreatLevel.MEDIUM
            },
            "privilege_escalation": {
                "pattern": r"(sudo.*-s|su.*root|chmod.*777)",
                "threshold": 3,
                "time_window": 180,
                "threat_type": ThreatType.PRIVILEGE_ESCALATION,
                "threat_level": ThreatLevel.HIGH
            },
            "suspicious_network": {
                "pattern": r"(nc.*-l|netcat.*listen|python.*socket)",
                "threshold": 1,
                "time_window": 60,
                "threat_type": ThreatType.LATERAL_MOVEMENT,
                "threat_level": ThreatLevel.MEDIUM
            }
        }
        
        self.logger.info(f"Loaded {len(self.detection_rules)} detection rules")
    
    async def _initialize_threat_intelligence(self):
        """Initialize threat intelligence feeds"""
        
        try:
            # Load threat indicators from database
            indicators = await self.db_manager.get_threat_indicators()
            
            for indicator in indicators:
                self.threat_indicators[indicator["value"]] = ThreatIndicator(**indicator)
            
            self.logger.info(f"Loaded {len(self.threat_indicators)} threat indicators")
            
            # Schedule threat intelligence updates
            asyncio.create_task(self._update_threat_intelligence())
            
        except Exception as e:
            self.logger.error(f"Failed to initialize threat intelligence: {str(e)}")
    
    async def _update_threat_intelligence(self):
        """Periodically update threat intelligence"""
        
        while True:
            try:
                await asyncio.sleep(3600)  # Update every hour
                
                # Update threat indicators (mock implementation)
                await self._fetch_threat_feeds()
                
                self.logger.info("Threat intelligence updated")
                
            except Exception as e:
                self.logger.error(f"Threat intelligence update failed: {str(e)}")
    
    async def _fetch_threat_feeds(self):
        """Fetch latest threat intelligence from external feeds"""
        
        # Mock threat intelligence data
        mock_indicators = [
            {
                "ioc_type": "ip",
                "value": "192.168.1.100",
                "threat_level": ThreatLevel.HIGH,
                "description": "Known malware C2 server",
                "source": "internal_feeds",
                "confidence": 0.9
            },
            {
                "ioc_type": "domain",
                "value": "malicious-domain.com",
                "threat_level": ThreatLevel.CRITICAL,
                "description": "Phishing domain",
                "source": "threat_feed",
                "confidence": 0.95
            }
        ]
        
        for indicator_data in mock_indicators:
            indicator = ThreatIndicator(
                **indicator_data,
                first_seen=datetime.now(),
                last_seen=datetime.now()
            )
            self.threat_indicators[indicator.value] = indicator
            
            # Store in database
            await self.db_manager.store_threat_indicator(asdict(indicator))
    
    async def start_threat_detection(self):
        """Start threat detection engine"""
        
        if not self.detection_enabled:
            self.logger.info("Threat detection is disabled")
            return
        
        self.logger.info("Starting threat detection engine")
        
        # Start detection tasks
        tasks = [
            asyncio.create_task(self._monitor_network_traffic()),
            asyncio.create_task(self._monitor_system_logs()),
            asyncio.create_task(self._monitor_process_activity()),
            asyncio.create_task(self._analyze_threats()),
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _monitor_network_traffic(self):
        """Monitor network traffic for threats"""
        
        while True:
            try:
                # Get network connections
                connections = psutil.net_connections(kind='inet')
                
                for conn in connections:
                    if conn.raddr:
                        remote_ip = conn.raddr.ip
                        
                        # Check against threat indicators
                        if remote_ip in self.threat_indicators:
                            await self._handle_threat_detection(
                                threat_type=ThreatType.MALWARE,
                                source_ip=remote_ip,
                                target_ip=conn.laddr.ip if conn.laddr else "unknown",
                                port=conn.raddr.port,
                                description=f"Connection to known malicious IP: {remote_ip}"
                            )
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Network monitoring error: {str(e)}")
                await asyncio.sleep(30)
    
    async def _monitor_system_logs(self):
        """Monitor system logs for threat patterns"""
        
        # This would typically tail system logs like /var/log/auth.log, /var/log/syslog
        # For now, we'll simulate log monitoring
        
        while True:
            try:
                # Mock log entries
                mock_logs = [
                    "Failed password for user from 192.168.1.50 port 22 ssh2",
                    "SELECT * FROM users WHERE id=1 OR 1=1--",
                    "<script>alert('xss')</script>",
                    "sudo su - root",
                    "nc -l 4444"
                ]
                
                for log_entry in mock_logs:
                    if await self._analyze_log_entry(log_entry):
                        break  # Exit after first detection to avoid spam
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Log monitoring error: {str(e)}")
                await asyncio.sleep(60)
    
    async def _analyze_log_entry(self, log_entry: str) -> bool:
        """Analyze log entry against detection rules"""
        
        for rule_name, rule in self.detection_rules.items():
            if re.search(rule["pattern"], log_entry, re.IGNORECASE):
                # Extract IP if possible
                ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_entry)
                source_ip = ip_match.group() if ip_match else "unknown"
                
                await self._handle_threat_detection(
                    threat_type=rule["threat_type"],
                    source_ip=source_ip,
                    target_ip="localhost",
                    port=0,
                    description=f"Detected {rule_name}: {log_entry}"
                )
                
                return True
        
        return False
    
    async def _monitor_process_activity(self):
        """Monitor process activity for suspicious behavior"""
        
        suspicious_processes = [
            "nc", "netcat", "ncat", "socat",
            "python -c", "perl -e", "ruby -e",
            "bash -c", "sh -c", "powershell",
            "msfconsole", "metasploit"
        ]
        
        while True:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        
                        for sus_proc in suspicious_processes:
                            if sus_proc in cmdline.lower():
                                await self._handle_threat_detection(
                                    threat_type=ThreatType.LATERAL_MOVEMENT,
                                    source_ip="localhost",
                                    target_ip="localhost",
                                    port=0,
                                    description=f"Suspicious process: {cmdline}"
                                )
                                break
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                await asyncio.sleep(120)  # Check every 2 minutes
                
            except Exception as e:
                self.logger.error(f"Process monitoring error: {str(e)}")
                await asyncio.sleep(120)
    
    async def _handle_threat_detection(self,
                                     threat_type: ThreatType,
                                     source_ip: str,
                                     target_ip: str,
                                     port: int,
                                     description: str,
                                     threat_level: ThreatLevel = None):
        """Handle detected threat"""
        
        # Determine threat level if not provided
        if threat_level is None:
            threat_level = self._assess_threat_level(threat_type, source_ip)
        
        # Create threat event
        event = ThreatEvent(
            event_id=hashlib.md5(f"{datetime.now().isoformat()}{source_ip}{threat_type.value}".encode()).hexdigest()[:16],
            timestamp=datetime.now(),
            threat_type=threat_type,
            threat_level=threat_level,
            source_ip=source_ip,
            target_ip=target_ip,
            port=port,
            protocol="tcp",  # Default
            description=description,
            indicators=self._get_related_indicators(source_ip),
            mitre_technique=self._get_mitre_technique(threat_type),
            mitre_tactic=self._get_mitre_tactic(threat_type)
        )
        
        # Store threat event
        self.active_threats.append(event)
        await self.db_manager.store_threat_event(asdict(event))
        
        self.logger.warning(f"Threat detected: {threat_type.value} from {source_ip} - {threat_level.value}")
        
        # Trigger response if auto-response is enabled
        if self.auto_response_enabled and threat_level.value in ["high", "critical"]:
            await self._trigger_automated_response(event)
    
    def _assess_threat_level(self, threat_type: ThreatType, source_ip: str) -> ThreatLevel:
        """Assess threat level based on type and context"""
        
        # Check if IP is in threat indicators
        if source_ip in self.threat_indicators:
            indicator = self.threat_indicators[source_ip]
            if indicator.threat_level == ThreatLevel.CRITICAL:
                return ThreatLevel.CRITICAL
        
        # Default threat levels by type
        threat_levels = {
            ThreatType.MALWARE: ThreatLevel.CRITICAL,
            ThreatType.PHISHING: ThreatLevel.HIGH,
            ThreatType.BRUTE_FORCE: ThreatLevel.HIGH,
            ThreatType.SQL_INJECTION: ThreatLevel.HIGH,
            ThreatType.XSS: ThreatLevel.MEDIUM,
            ThreatType.DDoS: ThreatLevel.CRITICAL,
            ThreatType.PRIVILEGE_ESCALATION: ThreatLevel.HIGH,
            ThreatType.DATA_EXFILTRATION: ThreatLevel.CRITICAL,
            ThreatType.LATERAL_MOVEMENT: ThreatLevel.MEDIUM,
            ThreatType.PERSISTENCE: ThreatLevel.HIGH
        }
        
        return threat_levels.get(threat_type, ThreatLevel.MEDIUM)
    
    def _get_related_indicators(self, source_ip: str) -> List[ThreatIndicator]:
        """Get threat indicators related to the source IP"""
        
        indicators = []
        
        if source_ip in self.threat_indicators:
            indicators.append(self.threat_indicators[source_ip])
        
        return indicators
    
    def _get_mitre_technique(self, threat_type: ThreatType) -> str:
        """Get MITRE ATT&CK technique for threat type"""
        
        mitre_mapping = {
            ThreatType.MALWARE: "T1059",  # Command and Scripting Interpreter
            ThreatType.PHISHING: "T1566",  # Phishing
            ThreatType.BRUTE_FORCE: "T1110",  # Brute Force
            ThreatType.SQL_INJECTION: "T1190",  # Exploit Public-Facing Application
            ThreatType.XSS: "T1190",  # Exploit Public-Facing Application
            ThreatType.DDoS: "T1498",  # Network Denial of Service
            ThreatType.PRIVILEGE_ESCALATION: "T1068",  # Exploitation for Privilege Escalation
            ThreatType.DATA_EXFILTRATION: "T1041",  # Exfiltration Over C2 Channel
            ThreatType.LATERAL_MOVEMENT: "T1021",  # Remote Services
            ThreatType.PERSISTENCE: "T1053"  # Scheduled Task/Job
        }
        
        return mitre_mapping.get(threat_type, "T1059")
    
    def _get_mitre_tactic(self, threat_type: ThreatType) -> str:
        """Get MITRE ATT&CK tactic for threat type"""
        
        tactic_mapping = {
            ThreatType.MALWARE: "Initial Access",
            ThreatType.PHISHING: "Initial Access",
            ThreatType.BRUTE_FORCE: "Credential Access",
            ThreatType.SQL_INJECTION: "Initial Access",
            ThreatType.XSS: "Initial Access",
            ThreatType.DDoS: "Impact",
            ThreatType.PRIVILEGE_ESCALATION: "Privilege Escalation",
            ThreatType.DATA_EXFILTRATION: "Exfiltration",
            ThreatType.LATERAL_MOVEMENT: "Lateral Movement",
            ThreatType.PERSISTENCE: "Persistence"
        }
        
        return tactic_mapping.get(threat_type, "Initial Access")
    
    async def _trigger_automated_response(self, threat_event: ThreatEvent):
        """Trigger automated response to threat"""
        
        response_actions = []
        
        # Determine response based on threat type and level
        if threat_event.threat_level == ThreatLevel.CRITICAL:
            if threat_event.source_ip != "localhost" and threat_event.source_ip != "unknown":
                # Block malicious IP
                action = await self._block_ip_address(threat_event.source_ip)
                response_actions.append(action)
            
            # Isolate affected host if possible
            if threat_event.target_ip != "localhost":
                action = await self._isolate_host(threat_event.target_ip)
                response_actions.append(action)
        
        elif threat_event.threat_level == ThreatLevel.HIGH:
            # Rate limit or monitor
            action = await self._rate_limit_ip(threat_event.source_ip)
            response_actions.append(action)
        
        # Send alert
        alert_action = await self._send_alert(threat_event)
        response_actions.append(alert_action)
        
        # Store response actions
        for action in response_actions:
            self.response_actions.append(action)
            await self.db_manager.store_response_action(asdict(action))
        
        self.logger.info(f"Automated response triggered for {threat_event.event_id}: {len(response_actions)} actions")
    
    async def _block_ip_address(self, ip_address: str) -> ResponseAction:
        """Block IP address using iptables"""
        
        action = ResponseAction(
            action_id=hashlib.md5(f"block_{ip_address}_{datetime.now()}".encode()).hexdigest()[:16],
            action_type="block_ip",
            target=ip_address,
            timestamp=datetime.now(),
            status="pending",
            details=f"Blocking IP address {ip_address}"
        )
        
        try:
            # Execute iptables command (requires root privileges)
            cmd = f"iptables -A INPUT -s {ip_address} -j DROP"
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                action.status = "success"
                action.details += " - Successfully blocked"
                self.logger.info(f"Blocked IP address: {ip_address}")
            else:
                action.status = "failed"
                action.details += f" - Error: {result.stderr}"
                self.logger.error(f"Failed to block IP {ip_address}: {result.stderr}")
        
        except Exception as e:
            action.status = "failed"
            action.details += f" - Exception: {str(e)}"
            self.logger.error(f"Exception blocking IP {ip_address}: {str(e)}")
        
        return action
    
    async def _isolate_host(self, ip_address: str) -> ResponseAction:
        """Isolate host from network"""
        
        action = ResponseAction(
            action_id=hashlib.md5(f"isolate_{ip_address}_{datetime.now()}".encode()).hexdigest()[:16],
            action_type="isolate_host",
            target=ip_address,
            timestamp=datetime.now(),
            status="pending",
            details=f"Isolating host {ip_address}"
        )
        
        try:
            # This would typically involve network segmentation or VLAN changes
            # For now, we'll simulate the action
            action.status = "simulated"
            action.details += " - Host isolation simulated (requires network infrastructure integration)"
            
            self.logger.info(f"Host isolation simulated for: {ip_address}")
        
        except Exception as e:
            action.status = "failed"
            action.details += f" - Exception: {str(e)}"
            self.logger.error(f"Exception isolating host {ip_address}: {str(e)}")
        
        return action
    
    async def _rate_limit_ip(self, ip_address: str) -> ResponseAction:
        """Apply rate limiting to IP address"""
        
        action = ResponseAction(
            action_id=hashlib.md5(f"ratelimit_{ip_address}_{datetime.now()}".encode()).hexdigest()[:16],
            action_type="rate_limit",
            target=ip_address,
            timestamp=datetime.now(),
            status="pending",
            details=f"Applying rate limit to {ip_address}"
        )
        
        try:
            # Apply rate limiting using iptables
            cmd = f"iptables -A INPUT -s {ip_address} -m limit --limit 10/min -j ACCEPT"
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                action.status = "success"
                action.details += " - Rate limiting applied"
                self.logger.info(f"Rate limiting applied to: {ip_address}")
            else:
                action.status = "failed"
                action.details += f" - Error: {result.stderr}"
        
        except Exception as e:
            action.status = "failed"
            action.details += f" - Exception: {str(e)}"
        
        return action
    
    async def _send_alert(self, threat_event: ThreatEvent) -> ResponseAction:
        """Send threat alert"""
        
        action = ResponseAction(
            action_id=hashlib.md5(f"alert_{threat_event.event_id}_{datetime.now()}".encode()).hexdigest()[:16],
            action_type="alert",
            target="security_team",
            timestamp=datetime.now(),
            status="success",
            details=f"Alert sent for {threat_event.threat_type.value} threat"
        )
        
        # This would typically send email, SMS, or webhook notification
        self.logger.warning(f"SECURITY ALERT: {threat_event.description}")
        
        return action
    
    async def _analyze_threats(self):
        """Continuously analyze threats for patterns and escalation"""
        
        while True:
            try:
                # Analyze recent threats for patterns
                if len(self.active_threats) >= 10:
                    await self._detect_threat_patterns()
                
                # Check for threat escalation
                await self._check_threat_escalation()
                
                await asyncio.sleep(300)  # Analyze every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Threat analysis error: {str(e)}")
                await asyncio.sleep(300)
    
    async def _detect_threat_patterns(self):
        """Detect patterns in threat data"""
        
        recent_threats = list(self.active_threats)[-50:]  # Last 50 threats
        
        # Group by source IP
        ip_counts = defaultdict(int)
        for threat in recent_threats:
            ip_counts[threat.source_ip] += 1
        
        # Detect coordinated attacks
        for ip, count in ip_counts.items():
            if count >= 5:  # Same IP with 5+ different attacks
                await self._handle_threat_detection(
                    threat_type=ThreatType.DDoS,
                    source_ip=ip,
                    target_ip="multiple",
                    port=0,
                    description=f"Coordinated attack detected from {ip} - {count} incidents",
                    threat_level=ThreatLevel.CRITICAL
                )
    
    async def _check_threat_escalation(self):
        """Check if threats need escalation"""
        
        # Count high/critical threats in last hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_critical = [
            t for t in self.active_threats
            if t.timestamp >= one_hour_ago and t.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
        ]
        
        if len(recent_critical) >= 10:
            self.logger.critical(f"THREAT ESCALATION: {len(recent_critical)} high/critical threats in last hour")
            # Trigger escalation procedures
    
    async def get_threat_status(self) -> Dict[str, Any]:
        """Get current threat detection status"""
        
        recent_threats = [t for t in self.active_threats if t.timestamp >= datetime.now() - timedelta(hours=24)]
        
        status = {
            "detection_enabled": self.detection_enabled,
            "auto_response_enabled": self.auto_response_enabled,
            "total_threats_24h": len(recent_threats),
            "threat_breakdown": {},
            "top_source_ips": {},
            "recent_responses": len([r for r in self.response_actions if r.timestamp >= datetime.now() - timedelta(hours=24)]),
            "system_status": "operational"
        }
        
        # Count threats by level
        for threat in recent_threats:
            level = threat.threat_level.value
            status["threat_breakdown"][level] = status["threat_breakdown"].get(level, 0) + 1
        
        # Top source IPs
        ip_counts = defaultdict(int)
        for threat in recent_threats:
            ip_counts[threat.source_ip] += 1
        
        status["top_source_ips"] = dict(
            sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        return status

# Factory function
def create_threat_detection_engine(settings: Settings, logger: Logger) -> ThreatDetectionEngine:
    """Create and configure threat detection engine"""
    return ThreatDetectionEngine(settings, logger)
