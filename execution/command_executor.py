"""
Command Executor for LEWIS
Handles safe execution of cybersecurity commands and tools
"""

import asyncio
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

class CommandExecutor:
    """
    Secure command executor for LEWIS
    Executes cybersecurity tools with proper validation and logging
    """
    
    def __init__(self, settings, logger, tool_manager, security_manager):
        self.settings = settings
        self.logger = logger
        self.tool_manager = tool_manager
        self.security_manager = security_manager
        
        # Output configuration
        self.output_dir = Path(settings.get("tools.output_dir", "outputs"))
        self.temp_dir = Path(settings.get("tools.temp_dir", "temp"))
        
        # Create directories
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        # Execution limits
        self.max_execution_time = 300  # 5 minutes
        self.max_output_size = 10 * 1024 * 1024  # 10MB
    
    async def execute_command(
        self, 
        intent_result: Dict[str, Any], 
        user_id: str
    ) -> Dict[str, Any]:
        """
        Execute command based on processed intent
        
        Args:
            intent_result: Processed intent from NLP
            user_id: User identifier
            
        Returns:
            Dictionary containing execution results
        """
        try:
            intent = intent_result.get("intent")
            entities = intent_result.get("entities", [])
            
            # Map intent to execution strategy
            execution_strategy = self._get_execution_strategy(intent)
            
            if not execution_strategy:
                return {
                    "success": False,
                    "error": f"No execution strategy for intent: {intent}"
                }
            
            # Execute based on strategy
            result = await execution_strategy(intent_result, user_id)
            
            # Log execution
            await self._log_execution(intent_result, result, user_id)
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Command execution error: {e}")
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}"
            }
    
    def _get_execution_strategy(self, intent: str) -> Optional[callable]:
        """Get execution strategy for intent"""
        strategies = {
            "network_scanning": self._execute_network_scan,
            "vulnerability_assessment": self._execute_vulnerability_scan,
            "information_gathering": self._execute_information_gathering,
            "web_scanning": self._execute_web_scan,
            "exploitation": self._execute_exploitation
        }
        
        return strategies.get(intent)
    
    async def _execute_network_scan(
        self, 
        intent_result: Dict[str, Any], 
        user_id: str
    ) -> Dict[str, Any]:
        """Execute network scanning commands"""
        entities = intent_result.get("entities", [])
        
        # Extract target
        target = self._extract_target(entities, required=True)
        if not target:
            return {
                "success": False,
                "error": "No target specified for network scan"
            }
        
        # Validate target
        if not self.security_manager.is_target_allowed(target, user_id):
            return {
                "success": False,
                "error": "Target not authorized for scanning"
            }
        
        # Choose scanning tool and parameters
        if self.tool_manager.is_tool_available("nmap"):
            return await self._execute_nmap_scan(target, entities, user_id)
        else:
            return {
                "success": False,
                "error": "No network scanning tools available"
            }
    
    async def _execute_nmap_scan(
        self, 
        target: str, 
        entities: List[Dict], 
        user_id: str
    ) -> Dict[str, Any]:
        """Execute Nmap scan"""
        try:
            # Build Nmap arguments
            args = ["-sS"]  # Default SYN scan
            
            # Extract port specification
            ports = self._extract_ports(entities)
            if ports:
                args.extend(["-p", ports])
            
            # Add service detection
            args.append("-sV")
            
            # Generate output file
            output_file = self._generate_output_filename("nmap", target, user_id)
            
            # Execute scan
            result = await self.tool_manager.execute_tool(
                "nmap", 
                args, 
                target, 
                output_file
            )
            
            # Parse results
            if result["success"]:
                parsed_results = self._parse_nmap_output(result["stdout"])
                result["parsed_results"] = parsed_results
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Nmap execution failed: {str(e)}"
            }
    
    async def _execute_vulnerability_scan(
        self, 
        intent_result: Dict[str, Any], 
        user_id: str
    ) -> Dict[str, Any]:
        """Execute vulnerability scanning"""
        entities = intent_result.get("entities", [])
        target = self._extract_target(entities, required=True)
        
        if not target:
            return {
                "success": False,
                "error": "No target specified for vulnerability scan"
            }
        
        # Check if target is web application
        if target.startswith("http://") or target.startswith("https://"):
            return await self._execute_web_vulnerability_scan(target, user_id)
        else:
            return await self._execute_network_vulnerability_scan(target, user_id)
    
    async def _execute_web_vulnerability_scan(self, target: str, user_id: str) -> Dict[str, Any]:
        """Execute web vulnerability scan"""
        if self.tool_manager.is_tool_available("nikto"):
            output_file = self._generate_output_filename("nikto", target, user_id)
            
            result = await self.tool_manager.execute_tool(
                "nikto",
                ["-h", target, "-Format", "htm"],
                output_file=output_file
            )
            
            if result["success"]:
                result["parsed_results"] = self._parse_nikto_output(result["stdout"])
            
            return result
        else:
            return {
                "success": False,
                "error": "No web vulnerability scanning tools available"
            }
    
    async def _execute_information_gathering(
        self, 
        intent_result: Dict[str, Any], 
        user_id: str
    ) -> Dict[str, Any]:
        """Execute information gathering"""
        entities = intent_result.get("entities", [])
        target = self._extract_target(entities, required=True)
        
        if not target:
            return {
                "success": False,
                "error": "No target specified for information gathering"
            }
        
        # Execute multiple information gathering tools
        results = {}
        
        # WHOIS lookup
        if self.tool_manager.is_tool_available("whois"):
            whois_result = await self.tool_manager.execute_tool("whois", [], target)
            results["whois"] = whois_result
        
        # Subdomain enumeration
        if self.tool_manager.is_tool_available("subfinder"):
            output_file = self._generate_output_filename("subfinder", target, user_id)
            subfinder_result = await self.tool_manager.execute_tool(
                "subfinder", ["-d", target, "-o", output_file]
            )
            results["subdomains"] = subfinder_result
        
        # DNS enumeration
        if self.tool_manager.is_tool_available("dig"):
            dig_result = await self.tool_manager.execute_tool("dig", [target, "ANY"])
            results["dns"] = dig_result
        
        return {
            "success": True,
            "results": results,
            "summary": self._summarize_info_gathering(results)
        }
    
    async def _execute_web_scan(
        self, 
        intent_result: Dict[str, Any], 
        user_id: str
    ) -> Dict[str, Any]:
        """Execute web application scanning"""
        entities = intent_result.get("entities", [])
        target = self._extract_target(entities, required=True)
        
        if not target:
            return {
                "success": False,
                "error": "No target specified for web scan"
            }
        
        # Ensure target is a web application
        if not (target.startswith("http://") or target.startswith("https://")):
            target = f"http://{target}"
        
        results = {}
        
        # Directory busting
        if self.tool_manager.is_tool_available("gobuster"):
            wordlist = "/usr/share/wordlists/dirb/common.txt"
            gobuster_result = await self.tool_manager.execute_tool(
                "gobuster", 
                ["dir", "-u", target, "-w", wordlist, "-t", "50"]
            )
            results["directories"] = gobuster_result
        
        # Web vulnerability scan
        if self.tool_manager.is_tool_available("nikto"):
            nikto_result = await self.tool_manager.execute_tool("nikto", ["-h", target])
            results["vulnerabilities"] = nikto_result
        
        return {
            "success": True,
            "results": results,
            "summary": self._summarize_web_scan(results)
        }
    
    async def _execute_exploitation(
        self, 
        intent_result: Dict[str, Any], 
        user_id: str
    ) -> Dict[str, Any]:
        """Execute exploitation (with safety checks)"""
        # This is a high-risk operation that requires special authorization
        if not self.security_manager.is_exploitation_allowed(user_id):
            return {
                "success": False,
                "error": "Exploitation not authorized for this user"
            }
        
        return {
            "success": False,
            "error": "Exploitation functionality requires manual confirmation and is not automated"
        }
    
    # Utility Methods
    def _extract_target(self, entities: List[Dict], required: bool = False) -> Optional[str]:
        """Extract target from entities"""
        target_types = ["ip_address", "domain", "url"]
        
        for entity in entities:
            if entity.get("type") in target_types:
                return entity.get("value")
        
        if required:
            return None
        
        return None
    
    def _extract_ports(self, entities: List[Dict]) -> Optional[str]:
        """Extract port specification from entities"""
        for entity in entities:
            if entity.get("type") == "port":
                return entity.get("value")
        
        return None
    
    def _generate_output_filename(self, tool: str, target: str, user_id: str) -> str:
        """Generate unique output filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = target.replace(".", "_").replace("/", "_").replace(":", "_")
        filename = f"{tool}_{safe_target}_{timestamp}_{user_id}.txt"
        return str(self.output_dir / filename)
    
    def _parse_nmap_output(self, output: str) -> Dict[str, Any]:
        """Parse Nmap output for structured data"""
        # Simplified parsing - in real implementation, use proper XML parsing
        lines = output.split('\n')
        open_ports = []
        
        for line in lines:
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 2:
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else "unknown"
                    open_ports.append({"port": port, "service": service})
        
        return {
            "open_ports": open_ports,
            "total_ports_found": len(open_ports)
        }
    
    def _parse_nikto_output(self, output: str) -> Dict[str, Any]:
        """Parse Nikto output for structured data"""
        lines = output.split('\n')
        vulnerabilities = []
        
        for line in lines:
            if '+ ' in line and 'OSVDB' in line:
                vulnerabilities.append(line.strip())
        
        return {
            "vulnerabilities": vulnerabilities,
            "vulnerability_count": len(vulnerabilities)
        }
    
    def _summarize_info_gathering(self, results: Dict[str, Any]) -> str:
        """Summarize information gathering results"""
        summary = []
        
        if "whois" in results and results["whois"]["success"]:
            summary.append("✅ WHOIS information retrieved")
        
        if "subdomains" in results and results["subdomains"]["success"]:
            summary.append("✅ Subdomain enumeration completed")
        
        if "dns" in results and results["dns"]["success"]:
            summary.append("✅ DNS records analyzed")
        
        return "; ".join(summary) if summary else "Information gathering completed with limited results"
    
    def _summarize_web_scan(self, results: Dict[str, Any]) -> str:
        """Summarize web scan results"""
        summary = []
        
        if "directories" in results and results["directories"]["success"]:
            summary.append("✅ Directory enumeration completed")
        
        if "vulnerabilities" in results and results["vulnerabilities"]["success"]:
            summary.append("✅ Vulnerability scan completed")
        
        return "; ".join(summary) if summary else "Web scan completed"
    
    async def _log_execution(
        self, 
        intent_result: Dict[str, Any], 
        execution_result: Dict[str, Any], 
        user_id: str
    ):
        """Log command execution"""
        log_data = {
            "user_id": user_id,
            "intent": intent_result.get("intent"),
            "command_type": "tool_execution",
            "success": execution_result.get("success", False),
            "execution_time": execution_result.get("execution_time", 0),
            "error": execution_result.get("error") if not execution_result.get("success") else None
        }
        
        # Log to database (this would use the database manager)
        self.logger.info(f"📝 Command executed: {intent_result.get('intent')} by {user_id}")
