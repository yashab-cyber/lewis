"""
Tool Manager for LEWIS
Manages integration with cybersecurity tools and their execution
"""

import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import json

class ToolManager:
    """
    Manages cybersecurity tools integration
    Handles tool discovery, validation, and execution coordination
    """
    
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        
        # Tool configurations
        self.tools = {}
        self._initialize_tools()
        
        # Tool validation results
        self.tool_status = {}
        self._validate_tools()
    
    def _initialize_tools(self):
        """Initialize tool configurations"""
        self.tools = {
            # Network Scanning
            "nmap": {
                "path": self.settings.get("tools.nmap_path", "nmap"),
                "category": "network_scanning",
                "description": "Network exploration and security auditing",
                "common_args": ["-sS", "-sV", "-sC", "-O", "-A"],
                "output_formats": ["-oN", "-oX", "-oG"]
            },
            
            "masscan": {
                "path": "masscan",
                "category": "network_scanning", 
                "description": "High-speed port scanner",
                "common_args": ["-p1-65535", "--rate=1000"],
                "requires_root": True
            },
            
            # Web Application Testing
            "nikto": {
                "path": self.settings.get("tools.nikto_path", "nikto"),
                "category": "web_scanning",
                "description": "Web server scanner",
                "common_args": ["-h", "-C", "all", "-Format", "htm"],
                "output_formats": ["-output"]
            },
            
            "dirb": {
                "path": "dirb",
                "category": "web_scanning",
                "description": "Web content scanner",
                "common_args": ["-r", "-S", "-w"],
                "wordlists": [
                    "/usr/share/wordlists/dirb/common.txt",
                    "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
                ]
            },
            
            "gobuster": {
                "path": "gobuster",
                "category": "web_scanning",
                "description": "Directory/file & DNS busting tool",
                "common_args": ["dir", "-u", "-w", "-t", "50"],
                "modes": ["dir", "dns", "vhost"]
            },
            
            "sqlmap": {
                "path": self.settings.get("tools.sqlmap_path", "sqlmap"),
                "category": "web_exploitation",
                "description": "SQL injection testing tool",
                "common_args": ["-u", "--batch", "--random-agent"],
                "requires_confirmation": True
            },
            
            # Information Gathering
            "subfinder": {
                "path": "subfinder",
                "category": "information_gathering",
                "description": "Subdomain discovery tool",
                "common_args": ["-d", "-o", "-silent"]
            },
            
            "theharvester": {
                "path": "theharvester",
                "category": "information_gathering", 
                "description": "Email harvesting tool",
                "common_args": ["-d", "-b", "-l", "500"]
            },
            
            "whois": {
                "path": "whois",
                "category": "information_gathering",
                "description": "Domain information lookup",
                "common_args": []
            },
            
            # Exploitation Framework
            "metasploit": {
                "path": self.settings.get("tools.metasploit_path", "/usr/share/metasploit-framework"),
                "category": "exploitation",
                "description": "Penetration testing framework",
                "executable": "msfconsole",
                "requires_confirmation": True,
                "danger_level": "high"
            },
            
            # DNS Tools
            "dig": {
                "path": "dig",
                "category": "information_gathering",
                "description": "DNS lookup utility",
                "common_args": ["ANY", "+short", "+trace"]
            },
            
            "nslookup": {
                "path": "nslookup",
                "category": "information_gathering", 
                "description": "DNS lookup utility",
                "common_args": []
            }
        }
    
    def _validate_tools(self):
        """Validate tool availability and accessibility"""
        self.logger.info("🔧 Validating cybersecurity tools...")
        
        for tool_name, config in self.tools.items():
            try:
                tool_path = config["path"]
                
                # Check if tool exists
                if shutil.which(tool_path) or Path(tool_path).exists():
                    # Test tool execution
                    result = subprocess.run(
                        [tool_path, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    self.tool_status[tool_name] = {
                        "available": True,
                        "path": tool_path,
                        "version": self._extract_version(result.stdout + result.stderr),
                        "validated": True
                    }
                    
                else:
                    self.tool_status[tool_name] = {
                        "available": False,
                        "path": tool_path,
                        "error": "Tool not found in system PATH",
                        "validated": False
                    }
                    
            except subprocess.TimeoutExpired:
                self.tool_status[tool_name] = {
                    "available": True,
                    "path": tool_path,
                    "error": "Version check timeout",
                    "validated": False
                }
                
            except Exception as e:
                self.tool_status[tool_name] = {
                    "available": False,
                    "path": tool_path,
                    "error": str(e),
                    "validated": False
                }
        
        # Log validation results
        available_count = sum(1 for status in self.tool_status.values() if status["available"])
        total_count = len(self.tool_status)
        
        self.logger.info(f"✅ Tool validation complete: {available_count}/{total_count} tools available")
        
        # Log missing tools
        missing_tools = [name for name, status in self.tool_status.items() if not status["available"]]
        if missing_tools:
            self.logger.warning(f"⚠️  Missing tools: {', '.join(missing_tools)}")
    
    def _extract_version(self, version_output: str) -> str:
        """Extract version information from tool output"""
        import re
        
        # Common version patterns
        patterns = [
            r"version\s+(\d+\.\d+(?:\.\d+)?)",
            r"v(\d+\.\d+(?:\.\d+)?)",
            r"(\d+\.\d+(?:\.\d+)?)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, version_output, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "unknown"
    
    async def execute_tool(
        self, 
        tool_name: str, 
        args: List[str], 
        target: str = None,
        output_file: str = None
    ) -> Dict[str, Any]:
        """
        Execute a cybersecurity tool with given arguments
        
        Args:
            tool_name: Name of the tool to execute
            args: List of command arguments
            target: Target for the tool (optional)
            output_file: Output file path (optional)
            
        Returns:
            Dictionary containing execution results
        """
        try:
            # Validate tool availability
            if tool_name not in self.tool_status or not self.tool_status[tool_name]["available"]:
                return {
                    "success": False,
                    "error": f"Tool {tool_name} is not available",
                    "tool": tool_name
                }
            
            tool_config = self.tools[tool_name]
            tool_path = tool_config["path"]
            
            # Build command
            command = [tool_path] + args
            
            # Add target if provided
            if target:
                command.append(target)
            
            # Add output file if provided
            if output_file and "output_formats" in tool_config:
                output_format = tool_config["output_formats"][0]
                command.extend([output_format, output_file])
            
            self.logger.info(f"🔧 Executing: {' '.join(command)}")
            
            # Execute command
            start_time = asyncio.get_event_loop().time()
            
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.settings.get("tools.output_dir", "outputs")
            )
            
            stdout, stderr = await process.communicate()
            
            end_time = asyncio.get_event_loop().time()
            execution_time = end_time - start_time
            
            # Process results
            result = {
                "success": process.returncode == 0,
                "tool": tool_name,
                "command": " ".join(command),
                "return_code": process.returncode,
                "stdout": stdout.decode("utf-8", errors="ignore"),
                "stderr": stderr.decode("utf-8", errors="ignore"),
                "execution_time": execution_time,
                "output_file": output_file
            }
            
            if result["success"]:
                self.logger.info(f"✅ Tool {tool_name} executed successfully in {execution_time:.2f}s")
            else:
                self.logger.error(f"❌ Tool {tool_name} execution failed (code: {process.returncode})")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error executing tool {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    def get_tool_suggestions(self, intent: str, entities: List[Dict]) -> List[Dict[str, Any]]:
        """Get tool suggestions based on intent and entities"""
        suggestions = []
        
        # Map intents to tool categories
        intent_tool_map = {
            "network_scanning": ["nmap", "masscan"],
            "web_scanning": ["nikto", "dirb", "gobuster"],
            "web_exploitation": ["sqlmap"],
            "information_gathering": ["subfinder", "theharvester", "whois", "dig"],
            "exploitation": ["metasploit"]
        }
        
        # Get relevant tools for intent
        relevant_tools = intent_tool_map.get(intent, [])
        
        for tool_name in relevant_tools:
            if tool_name in self.tool_status and self.tool_status[tool_name]["available"]:
                tool_config = self.tools[tool_name]
                
                suggestion = {
                    "tool": tool_name,
                    "description": tool_config["description"],
                    "category": tool_config["category"],
                    "common_args": tool_config.get("common_args", []),
                    "requires_confirmation": tool_config.get("requires_confirmation", False)
                }
                
                suggestions.append(suggestion)
        
        return suggestions
    
    def get_tool_status(self) -> Dict[str, Any]:
        """Get status of all tools"""
        return {
            "total_tools": len(self.tools),
            "available_tools": len([s for s in self.tool_status.values() if s["available"]]),
            "tools": self.tool_status,
            "categories": list(set(tool["category"] for tool in self.tools.values()))
        }
    
    def get_available_tools_count(self) -> int:
        """Get count of available tools"""
        return len([s for s in self.tool_status.values() if s["available"]])
    
    def is_tool_available(self, tool_name: str) -> bool:
        """Check if specific tool is available"""
        return (tool_name in self.tool_status and 
                self.tool_status[tool_name]["available"])
    
    def get_tool_help(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get help information for a specific tool"""
        if tool_name not in self.tools:
            return None
        
        tool_config = self.tools[tool_name]
        tool_status = self.tool_status.get(tool_name, {})
        
        return {
            "name": tool_name,
            "description": tool_config["description"],
            "category": tool_config["category"],
            "path": tool_config["path"],
            "available": tool_status.get("available", False),
            "version": tool_status.get("version", "unknown"),
            "common_args": tool_config.get("common_args", []),
            "output_formats": tool_config.get("output_formats", []),
            "requires_root": tool_config.get("requires_root", False),
            "requires_confirmation": tool_config.get("requires_confirmation", False),
            "danger_level": tool_config.get("danger_level", "low")
        }
