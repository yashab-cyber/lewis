#!/usr/bin/env python3
"""
LEWIS Analytics Engine
Real-time analytics, visualization, and dashboard data generation
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import statistics
import hashlib

# Data visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import pandas as pd
import numpy as np
from io import BytesIO
import base64

from config.settings import Settings
from utils.logger import Logger
from storage.database_manager import DatabaseManager

@dataclass
class MetricData:
    timestamp: datetime
    metric_name: str
    value: float
    tags: Dict[str, str] = None

@dataclass
class ThreatEvent:
    timestamp: datetime
    event_type: str
    severity: str
    source_ip: str
    target_ip: str
    description: str
    mitre_technique: str = None

@dataclass
class SystemMetric:
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_activity: float
    active_connections: int
    timestamp: datetime

class AnalyticsEngine:
    """Real-time analytics and visualization engine for LEWIS"""
    
    def __init__(self, settings: Settings, logger: Logger):
        self.settings = settings
        self.logger = logger
        self.db_manager = DatabaseManager(settings, logger)
        
        # In-memory data stores for real-time analytics
        self.metrics_buffer = deque(maxlen=1000)
        self.threat_events = deque(maxlen=500)
        self.system_metrics = deque(maxlen=100)
        self.command_history = deque(maxlen=1000)
        
        # Analytics configuration
        self.update_interval = settings.get("analytics", {}).get("update_interval", 60)  # seconds
        self.retention_days = settings.get("analytics", {}).get("retention_days", 30)
        
        # Set visualization style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    async def start_analytics_engine(self):
        """Start the analytics engine background tasks"""
        self.logger.info("Starting analytics engine")
        
        # Start background tasks
        tasks = [
            asyncio.create_task(self._collect_system_metrics()),
            asyncio.create_task(self._process_threat_events()),
            asyncio.create_task(self._cleanup_old_data()),
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _collect_system_metrics(self):
        """Collect system metrics periodically"""
        while True:
            try:
                # Collect system metrics (mock data for now)
                metrics = SystemMetric(
                    cpu_usage=np.random.uniform(10, 90),
                    memory_usage=np.random.uniform(30, 80),
                    disk_usage=np.random.uniform(20, 70),
                    network_activity=np.random.uniform(0, 100),
                    active_connections=np.random.randint(50, 200),
                    timestamp=datetime.now()
                )
                
                self.system_metrics.append(metrics)
                
                # Store in database
                await self.db_manager.store_system_metrics(asdict(metrics))
                
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                self.logger.error(f"Error collecting system metrics: {str(e)}")
                await asyncio.sleep(self.update_interval)
    
    async def _process_threat_events(self):
        """Process and analyze threat events"""
        while True:
            try:
                # Mock threat event generation
                if np.random.random() < 0.1:  # 10% chance of threat event
                    event = ThreatEvent(
                        timestamp=datetime.now(),
                        event_type=np.random.choice(["malware", "phishing", "brute_force", "sql_injection"]),
                        severity=np.random.choice(["low", "medium", "high", "critical"]),
                        source_ip=f"192.168.1.{np.random.randint(1, 255)}",
                        target_ip=f"10.0.0.{np.random.randint(1, 100)}",
                        description="Suspicious activity detected",
                        mitre_technique=f"T{np.random.randint(1000, 9999)}"
                    )
                    
                    self.threat_events.append(event)
                    await self.db_manager.store_threat_event(asdict(event))
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error processing threat events: {str(e)}")
                await asyncio.sleep(30)
    
    async def _cleanup_old_data(self):
        """Clean up old analytics data"""
        while True:
            try:
                cutoff_date = datetime.now() - timedelta(days=self.retention_days)
                await self.db_manager.cleanup_old_analytics(cutoff_date)
                
                # Sleep for 24 hours before next cleanup
                await asyncio.sleep(86400)
                
            except Exception as e:
                self.logger.error(f"Error during data cleanup: {str(e)}")
                await asyncio.sleep(86400)
    
    async def get_dashboard_data(self, user_id: str = None) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        
        try:
            # Get various analytics data
            system_stats = await self._get_system_statistics()
            threat_stats = await self._get_threat_statistics()
            command_stats = await self._get_command_statistics(user_id)
            performance_data = await self._get_performance_data()
            
            # Generate charts
            charts = await self._generate_dashboard_charts()
            
            dashboard_data = {
                "system_statistics": system_stats,
                "threat_statistics": threat_stats,
                "command_statistics": command_stats,
                "performance_data": performance_data,
                "charts": charts,
                "last_updated": datetime.now().isoformat(),
                "health_status": await self._get_system_health()
            }
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Error generating dashboard data: {str(e)}")
            return {"error": "Failed to generate dashboard data"}
    
    async def _get_system_statistics(self) -> Dict[str, Any]:
        """Get system performance statistics"""
        
        if not self.system_metrics:
            return {
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0,
                "network_activity": 0,
                "active_connections": 0
            }
        
        recent_metrics = list(self.system_metrics)[-10:]  # Last 10 readings
        
        return {
            "cpu_usage": round(statistics.mean([m.cpu_usage for m in recent_metrics]), 1),
            "memory_usage": round(statistics.mean([m.memory_usage for m in recent_metrics]), 1),
            "disk_usage": round(statistics.mean([m.disk_usage for m in recent_metrics]), 1),
            "network_activity": round(statistics.mean([m.network_activity for m in recent_metrics]), 1),
            "active_connections": int(statistics.mean([m.active_connections for m in recent_metrics])),
            "uptime": self._get_system_uptime()
        }
    
    async def _get_threat_statistics(self) -> Dict[str, Any]:
        """Get threat detection statistics"""
        
        if not self.threat_events:
            return {
                "total_threats": 0,
                "severity_breakdown": {"low": 0, "medium": 0, "high": 0, "critical": 0},
                "threat_types": {},
                "recent_threats": []
            }
        
        # Count threats by severity
        severity_counts = defaultdict(int)
        type_counts = defaultdict(int)
        
        for event in self.threat_events:
            severity_counts[event.severity] += 1
            type_counts[event.event_type] += 1
        
        # Get recent threats (last 10)
        recent_threats = [
            {
                "timestamp": event.timestamp.isoformat(),
                "type": event.event_type,
                "severity": event.severity,
                "source_ip": event.source_ip,
                "description": event.description
            }
            for event in list(self.threat_events)[-10:]
        ]
        
        return {
            "total_threats": len(self.threat_events),
            "severity_breakdown": dict(severity_counts),
            "threat_types": dict(type_counts),
            "recent_threats": recent_threats,
            "threats_last_24h": len([e for e in self.threat_events 
                                   if e.timestamp > datetime.now() - timedelta(days=1)])
        }
    
    async def _get_command_statistics(self, user_id: str = None) -> Dict[str, Any]:
        """Get command execution statistics"""
        
        # Get command statistics from database
        try:
            stats = await self.db_manager.get_command_statistics(user_id)
            return stats
        except:
            # Fallback to mock data
            return {
                "total_commands": 156,
                "successful_commands": 142,
                "failed_commands": 14,
                "success_rate": 91.0,
                "most_used_tools": [
                    {"name": "nmap", "count": 45},
                    {"name": "nikto", "count": 32},
                    {"name": "sqlmap", "count": 28},
                    {"name": "gobuster", "count": 21},
                    {"name": "metasploit", "count": 15}
                ],
                "commands_last_24h": 23
            }
    
    async def _get_performance_data(self) -> Dict[str, Any]:
        """Get system performance data"""
        
        return {
            "response_time_avg": 1.2,  # seconds
            "response_time_p95": 3.4,
            "requests_per_minute": 45,
            "error_rate": 2.1,  # percentage
            "cache_hit_rate": 87.5,
            "database_connections": 12,
            "memory_usage_trend": "stable",
            "cpu_load_avg": [1.2, 1.5, 1.8]  # 1, 5, 15 minute averages
        }
    
    async def _generate_dashboard_charts(self) -> Dict[str, Any]:
        """Generate charts for dashboard"""
        
        charts = {}
        
        try:
            # System metrics chart
            if self.system_metrics:
                metrics_df = pd.DataFrame([asdict(m) for m in self.system_metrics])
                
                # CPU usage chart
                fig_cpu = px.line(
                    metrics_df, 
                    x='timestamp', 
                    y='cpu_usage',
                    title='CPU Usage Over Time',
                    line_shape='spline'
                )
                charts['cpu_usage'] = json.dumps(fig_cpu, cls=PlotlyJSONEncoder)
                
                # Memory usage chart
                fig_mem = px.line(
                    metrics_df, 
                    x='timestamp', 
                    y='memory_usage',
                    title='Memory Usage Over Time',
                    line_shape='spline'
                )
                charts['memory_usage'] = json.dumps(fig_mem, cls=PlotlyJSONEncoder)
            
            # Threat events chart
            if self.threat_events:
                threat_df = pd.DataFrame([asdict(t) for t in self.threat_events])
                
                # Threat severity distribution
                severity_counts = threat_df['severity'].value_counts()
                fig_threats = px.pie(
                    values=severity_counts.values,
                    names=severity_counts.index,
                    title='Threat Severity Distribution'
                )
                charts['threat_distribution'] = json.dumps(fig_threats, cls=PlotlyJSONEncoder)
                
                # Threat timeline
                threat_timeline = threat_df.groupby(
                    threat_df['timestamp'].dt.floor('H')
                ).size().reset_index(name='count')
                
                fig_timeline = px.bar(
                    threat_timeline,
                    x='timestamp',
                    y='count',
                    title='Threats Over Time (Hourly)'
                )
                charts['threat_timeline'] = json.dumps(fig_timeline, cls=PlotlyJSONEncoder)
            
            # Network activity heatmap (mock data)
            network_data = np.random.rand(24, 7)  # 24 hours x 7 days
            fig_heatmap = px.imshow(
                network_data,
                title='Network Activity Heatmap (Last 7 Days)',
                labels=dict(x="Day", y="Hour", color="Activity Level"),
                x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                y=[f"{i:02d}:00" for i in range(24)]
            )
            charts['network_heatmap'] = json.dumps(fig_heatmap, cls=PlotlyJSONEncoder)
            
        except Exception as e:
            self.logger.error(f"Error generating charts: {str(e)}")
        
        return charts
    
    def _get_system_uptime(self) -> str:
        """Get system uptime (mock)"""
        # This would typically get real system uptime
        uptime_seconds = 345600  # 4 days
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        
        return f"{days}d {hours}h {minutes}m"
    
    async def _get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        
        # Calculate health based on various metrics
        health_score = 100
        issues = []
        
        if self.system_metrics:
            latest_metrics = self.system_metrics[-1]
            
            # Check CPU usage
            if latest_metrics.cpu_usage > 90:
                health_score -= 20
                issues.append("High CPU usage")
            
            # Check memory usage
            if latest_metrics.memory_usage > 85:
                health_score -= 15
                issues.append("High memory usage")
            
            # Check disk usage
            if latest_metrics.disk_usage > 90:
                health_score -= 25
                issues.append("Low disk space")
        
        # Check threat level
        critical_threats = len([t for t in self.threat_events 
                              if t.severity == "critical" and 
                              t.timestamp > datetime.now() - timedelta(hours=1)])
        
        if critical_threats > 0:
            health_score -= critical_threats * 10
            issues.append(f"{critical_threats} critical threats in last hour")
        
        # Determine status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 75:
            status = "good"
        elif health_score >= 50:
            status = "warning"
        else:
            status = "critical"
        
        return {
            "status": status,
            "score": max(0, health_score),
            "issues": issues,
            "last_check": datetime.now().isoformat()
        }
    
    async def record_command_execution(self, 
                                     command: str, 
                                     user_id: str, 
                                     success: bool, 
                                     execution_time: float,
                                     tool_used: str = None):
        """Record command execution for analytics"""
        
        command_data = {
            "timestamp": datetime.now(),
            "command": command,
            "user_id": user_id,
            "success": success,
            "execution_time": execution_time,
            "tool_used": tool_used
        }
        
        self.command_history.append(command_data)
        await self.db_manager.store_command_execution(command_data)
    
    async def record_threat_event(self, 
                                event_type: str,
                                severity: str,
                                source_ip: str,
                                target_ip: str,
                                description: str,
                                mitre_technique: str = None):
        """Record a threat event"""
        
        event = ThreatEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            severity=severity,
            source_ip=source_ip,
            target_ip=target_ip,
            description=description,
            mitre_technique=mitre_technique
        )
        
        self.threat_events.append(event)
        await self.db_manager.store_threat_event(asdict(event))
        
        self.logger.warning(f"Threat event recorded: {event_type} - {severity}")
    
    async def get_threat_analysis(self, time_range: str = "24h") -> Dict[str, Any]:
        """Get detailed threat analysis"""
        
        # Parse time range
        if time_range == "1h":
            cutoff = datetime.now() - timedelta(hours=1)
        elif time_range == "24h":
            cutoff = datetime.now() - timedelta(days=1)
        elif time_range == "7d":
            cutoff = datetime.now() - timedelta(days=7)
        elif time_range == "30d":
            cutoff = datetime.now() - timedelta(days=30)
        else:
            cutoff = datetime.now() - timedelta(days=1)
        
        # Filter events by time range
        filtered_events = [e for e in self.threat_events if e.timestamp >= cutoff]
        
        if not filtered_events:
            return {"message": "No threats detected in specified time range"}
        
        # Analyze threat patterns
        analysis = {
            "total_threats": len(filtered_events),
            "time_range": time_range,
            "severity_distribution": {},
            "threat_types": {},
            "top_source_ips": {},
            "attack_timeline": [],
            "mitre_techniques": {},
            "recommendations": []
        }
        
        # Count by severity
        for event in filtered_events:
            analysis["severity_distribution"][event.severity] = \
                analysis["severity_distribution"].get(event.severity, 0) + 1
            
            analysis["threat_types"][event.event_type] = \
                analysis["threat_types"].get(event.event_type, 0) + 1
            
            analysis["top_source_ips"][event.source_ip] = \
                analysis["top_source_ips"].get(event.source_ip, 0) + 1
            
            if event.mitre_technique:
                analysis["mitre_techniques"][event.mitre_technique] = \
                    analysis["mitre_techniques"].get(event.mitre_technique, 0) + 1
        
        # Generate recommendations
        critical_count = analysis["severity_distribution"].get("critical", 0)
        high_count = analysis["severity_distribution"].get("high", 0)
        
        if critical_count > 0:
            analysis["recommendations"].append(
                f"Immediate action required: {critical_count} critical threats detected"
            )
        
        if high_count > 5:
            analysis["recommendations"].append(
                "Consider implementing additional security measures due to high threat volume"
            )
        
        # Sort dictionaries by count
        analysis["top_source_ips"] = dict(
            sorted(analysis["top_source_ips"].items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        return analysis
    
    async def generate_analytics_report(self, report_type: str = "summary") -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        
        report = {
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            "time_period": "Last 24 hours",
        }
        
        if report_type == "summary":
            report.update({
                "system_health": await self._get_system_health(),
                "threat_summary": await self._get_threat_statistics(),
                "performance_summary": await self._get_performance_data()
            })
        
        elif report_type == "detailed":
            report.update({
                "system_statistics": await self._get_system_statistics(),
                "threat_analysis": await self.get_threat_analysis("24h"),
                "command_statistics": await self._get_command_statistics(),
                "performance_metrics": await self._get_performance_data(),
                "charts": await self._generate_dashboard_charts()
            })
        
        return report

# Factory function
def create_analytics_engine(settings: Settings, logger: Logger) -> AnalyticsEngine:
    """Create and configure analytics engine"""
    return AnalyticsEngine(settings, logger)
