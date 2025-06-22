"""
Knowledge Base for LEWIS
Manages cybersecurity knowledge, CVE data, and threat intelligence
"""

import asyncio
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

class KnowledgeBase:
    """
    Knowledge base manager for LEWIS
    Handles CVE data, threat intelligence, and cybersecurity knowledge
    """
    
    def __init__(self, settings, logger, database_manager):
        self.settings = settings
        self.logger = logger
        self.db_manager = database_manager
        
        # Knowledge categories
        self.categories = {
            "cve": "Common Vulnerabilities and Exposures",
            "tools": "Cybersecurity Tools Information",
            "techniques": "Attack Techniques and Procedures",
            "threats": "Threat Intelligence",
            "best_practices": "Security Best Practices",
            "compliance": "Compliance and Standards"
        }
        
        # CVE data sources
        self.cve_sources = settings.get("learning.cve_sources", [])
        
        # Initialize knowledge base
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base with default data"""
        try:
            self.logger.info("📚 Initializing knowledge base...")
            
            # Load default cybersecurity knowledge
            self._load_default_knowledge()
            
            self.logger.info("✅ Knowledge base initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize knowledge base: {e}")
    
    def _load_default_knowledge(self):
        """Load default cybersecurity knowledge"""
        # Default tool information
        default_tools = {
            "nmap": {
                "category": "tools",
                "title": "Nmap - Network Mapper",
                "description": "Network exploration tool and security scanner",
                "usage": "nmap [options] [target]",
                "common_options": [
                    "-sS: TCP SYN scan",
                    "-sV: Version detection", 
                    "-sC: Default script scan",
                    "-O: OS detection",
                    "-A: Aggressive scan"
                ],
                "examples": [
                    "nmap -sS 192.168.1.1",
                    "nmap -sV -sC example.com",
                    "nmap -p 80,443 -sS target.com"
                ]
            },
            
            "nikto": {
                "category": "tools",
                "title": "Nikto - Web Vulnerability Scanner",
                "description": "Web server scanner for vulnerabilities",
                "usage": "nikto -h [target]",
                "common_options": [
                    "-h: Target host",
                    "-p: Port number",
                    "-Format: Output format",
                    "-C: Cookie to use"
                ],
                "examples": [
                    "nikto -h http://example.com",
                    "nikto -h example.com -p 443 -ssl"
                ]
            },
            
            "metasploit": {
                "category": "tools", 
                "title": "Metasploit Framework",
                "description": "Penetration testing framework",
                "usage": "msfconsole",
                "basic_commands": [
                    "search: Search for exploits",
                    "use: Select exploit",
                    "set: Set parameters",
                    "exploit: Run exploit"
                ],
                "warning": "Use only on authorized targets"
            }
        }
        
        # Default attack techniques
        default_techniques = {
            "port_scanning": {
                "category": "techniques",
                "title": "Port Scanning Techniques",
                "description": "Methods for discovering open ports and services",
                "types": [
                    "TCP Connect Scan",
                    "TCP SYN Scan", 
                    "UDP Scan",
                    "Stealth Scan"
                ],
                "tools": ["nmap", "masscan", "zmap"],
                "countermeasures": [
                    "Firewall configuration",
                    "Port knocking",
                    "Service hardening"
                ]
            },
            
            "web_vulnerabilities": {
                "category": "techniques",
                "title": "Common Web Vulnerabilities",
                "description": "OWASP Top 10 and common web application vulnerabilities",
                "vulnerabilities": [
                    "SQL Injection",
                    "Cross-Site Scripting (XSS)",
                    "Cross-Site Request Forgery (CSRF)",
                    "Directory Traversal",
                    "Command Injection"
                ],
                "tools": ["sqlmap", "burp suite", "nikto", "dirb"],
                "prevention": [
                    "Input validation",
                    "Parameterized queries",
                    "Output encoding",
                    "Security headers"
                ]
            }
        }
        
        # Save default knowledge to database
        asyncio.create_task(self._save_default_knowledge(default_tools, default_techniques))
    
    async def _save_default_knowledge(self, tools: Dict, techniques: Dict):
        """Save default knowledge to database"""
        try:
            # Save tools
            for tool_name, tool_info in tools.items():
                await self.db_manager.save_knowledge({
                    "type": "tool",
                    "name": tool_name,
                    "category": tool_info["category"],
                    "title": tool_info["title"],
                    "content": tool_info,
                    "keywords": [tool_name, tool_info["category"]]
                })
            
            # Save techniques
            for technique_name, technique_info in techniques.items():
                await self.db_manager.save_knowledge({
                    "type": "technique",
                    "name": technique_name,
                    "category": technique_info["category"],
                    "title": technique_info["title"],
                    "content": technique_info,
                    "keywords": [technique_name, technique_info["category"]]
                })
                
            self.logger.info("✅ Default knowledge saved to database")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving default knowledge: {e}")
    
    async def search_knowledge(
        self, 
        query: str, 
        category: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search knowledge base
        
        Args:
            query: Search query
            category: Filter by category
            limit: Maximum results
            
        Returns:
            List of matching knowledge entries
        """
        try:
            results = await self.db_manager.search_knowledge(query, category, limit)
            
            # Enhance results with relevance scoring
            enhanced_results = self._enhance_search_results(results, query)
            
            return enhanced_results
            
        except Exception as e:
            self.logger.error(f"❌ Error searching knowledge base: {e}")
            return []
    
    def _enhance_search_results(
        self, 
        results: List[Dict[str, Any]], 
        query: str
    ) -> List[Dict[str, Any]]:
        """Enhance search results with relevance scoring"""
        query_words = query.lower().split()
        
        for result in results:
            score = 0
            content = str(result.get("content", "")).lower()
            title = str(result.get("title", "")).lower()
            
            # Score based on title matches
            for word in query_words:
                if word in title:
                    score += 3
                if word in content:
                    score += 1
            
            result["relevance_score"] = score
        
        # Sort by relevance
        return sorted(results, key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    async def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        try:
            results = await self.search_knowledge(tool_name, category="tools", limit=1)
            return results[0] if results else None
            
        except Exception as e:
            self.logger.error(f"❌ Error getting tool info: {e}")
            return None
    
    async def get_vulnerability_info(self, vulnerability: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific vulnerability"""
        try:
            results = await self.search_knowledge(vulnerability, category="cve", limit=1)
            return results[0] if results else None
            
        except Exception as e:
            self.logger.error(f"❌ Error getting vulnerability info: {e}")
            return None
    
    async def add_knowledge_entry(self, entry: Dict[str, Any]) -> bool:
        """Add new knowledge entry"""
        try:
            # Validate entry
            if not self._validate_knowledge_entry(entry):
                return False
            
            # Add metadata
            entry["added_at"] = datetime.utcnow()
            entry["source"] = "user_input"
            
            # Save to database
            success = await self.db_manager.save_knowledge(entry)
            
            if success:
                self.logger.info(f"✅ Knowledge entry added: {entry.get('title')}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Error adding knowledge entry: {e}")
            return False
    
    def _validate_knowledge_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate knowledge entry format"""
        required_fields = ["type", "category", "title", "content"]
        
        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"⚠️  Missing required field: {field}")
                return False
        
        # Validate category
        if entry["category"] not in self.categories:
            self.logger.warning(f"⚠️  Invalid category: {entry['category']}")
            return False
        
        return True
    
    async def update_cve_data(self) -> bool:
        """Update CVE data from external sources"""
        try:
            self.logger.info("🔄 Updating CVE data...")
            
            # This is a simplified implementation
            # In real implementation, parse NVD/MITRE CVE feeds
            
            success_count = 0
            
            for source_url in self.cve_sources:
                try:
                    cve_data = await self._fetch_cve_data(source_url)
                    if cve_data:
                        await self._process_cve_data(cve_data)
                        success_count += 1
                        
                except Exception as e:
                    self.logger.error(f"❌ Error updating from {source_url}: {e}")
            
            self.logger.info(f"✅ CVE data updated from {success_count} sources")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"❌ Error updating CVE data: {e}")
            return False
    
    async def _fetch_cve_data(self, source_url: str) -> Optional[Dict[str, Any]]:
        """Fetch CVE data from external source"""
        try:
            # Simplified implementation - in real version, handle different CVE feed formats
            response = requests.get(source_url, timeout=30)
            if response.status_code == 200:
                return {"data": "placeholder"}  # Placeholder for actual CVE data
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error fetching CVE data from {source_url}: {e}")
            return None
    
    async def _process_cve_data(self, cve_data: Dict[str, Any]):
        """Process and save CVE data"""
        # Placeholder for CVE data processing
        # In real implementation, parse CVE entries and save to knowledge base
        pass
    
    def get_cve_info(self, entities: List[Dict[str, Any]]) -> Optional[str]:
        """Get CVE information for entities"""
        # Simplified implementation
        cve_entities = [e for e in entities if e.get("type") == "cve"]
        
        if cve_entities:
            cve_ids = [e.get("value") for e in cve_entities]
            return f"Found CVE references: {', '.join(cve_ids)}"
        
        return None
    
    def get_entry_count(self) -> int:
        """Get total number of knowledge entries"""
        try:
            # This would query the database for count
            # For now, return a placeholder
            return 100  # Placeholder
            
        except Exception as e:
            self.logger.error(f"❌ Error getting entry count: {e}")
            return 0
    
    async def get_recommendations(
        self, 
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get recommendations based on context"""
        try:
            recommendations = []
            
            # Tool recommendations based on intent
            intent = context.get("intent")
            
            if intent == "network_scanning":
                recommendations.extend([
                    {
                        "type": "tool",
                        "title": "Advanced Nmap Scanning",
                        "description": "Use Nmap with script scanning for comprehensive results",
                        "command": "nmap -sV -sC -A <target>"
                    },
                    {
                        "type": "technique",
                        "title": "Service Enumeration",
                        "description": "Follow up port scans with service enumeration",
                        "next_steps": ["banner grabbing", "service version detection"]
                    }
                ])
            
            elif intent == "vulnerability_assessment":
                recommendations.extend([
                    {
                        "type": "tool",
                        "title": "Web Application Testing",
                        "description": "Use Nikto for web vulnerability scanning",
                        "command": "nikto -h <target>"
                    },
                    {
                        "type": "best_practice",
                        "title": "Vulnerability Prioritization",
                        "description": "Prioritize vulnerabilities by CVSS score and exploitability"
                    }
                ])
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"❌ Error getting recommendations: {e}")
            return []
