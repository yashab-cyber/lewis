"""
Extension Base Classes for LEWIS
Provides base functionality for creating LEWIS extensions
"""

import abc
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

class ExtensionBase(abc.ABC):
    """
    Base class for all LEWIS extensions
    
    Extensions should inherit from this class and implement the required methods.
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.logger = logging.getLogger(f"lewis.extension.{name}")
        self.commands = {}
        self.tools = {}
        self.config = {}
        self.enabled = False
        
    @abc.abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the extension
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abc.abstractmethod
    def cleanup(self) -> bool:
        """
        Cleanup extension resources
        
        Returns:
            bool: True if cleanup successful, False otherwise
        """
        pass
    
    def load_config(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load extension configuration
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dict containing configuration
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "default.yaml"
            
        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r') as f:
                    self.config = yaml.safe_load(f)
                self.logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                self.logger.error(f"Failed to load config: {e}")
                self.config = {}
        else:
            self.logger.warning(f"Config file not found: {config_path}")
            self.config = {}
            
        return self.config
    
    def register_command(self, name: str, func: Callable, description: str = ""):
        """
        Register a command with the extension
        
        Args:
            name: Command name
            func: Function to execute
            description: Command description
        """
        self.commands[name] = {
            "function": func,
            "description": description,
            "extension": self.name
        }
        self.logger.debug(f"Registered command: {name}")
    
    def register_tool(self, name: str, func: Callable, description: str = ""):
        """
        Register a tool with the extension
        
        Args:
            name: Tool name
            func: Function to execute
            description: Tool description
        """
        self.tools[name] = {
            "function": func,
            "description": description,
            "extension": self.name
        }
        self.logger.debug(f"Registered tool: {name}")
    
    def get_commands(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered commands"""
        return self.commands
    
    def get_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered tools"""
        return self.tools
    
    def execute_command(self, command_name: str, *args, **kwargs) -> Any:
        """
        Execute a registered command
        
        Args:
            command_name: Name of command to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Command execution result
        """
        if command_name not in self.commands:
            raise ValueError(f"Command '{command_name}' not found in extension '{self.name}'")
        
        try:
            return self.commands[command_name]["function"](*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error executing command '{command_name}': {e}")
            raise
    
    def execute_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """
        Execute a registered tool
        
        Args:
            tool_name: Name of tool to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found in extension '{self.name}'")
        
        try:
            return self.tools[tool_name]["function"](*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error executing tool '{tool_name}': {e}")
            raise
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get extension information
        
        Returns:
            Dict containing extension metadata
        """
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "commands": list(self.commands.keys()),
            "tools": list(self.tools.keys()),
            "config": self.config
        }


class NetworkExtension(ExtensionBase):
    """Base class for network-related extensions"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        super().__init__(name, version)
        self.network_tools = {}
    
    def scan_network(self, target: str, scan_type: str = "basic") -> Dict[str, Any]:
        """
        Perform network scan
        
        Args:
            target: Target IP or range
            scan_type: Type of scan to perform
            
        Returns:
            Scan results
        """
        # This is a base implementation that should be overridden
        return {
            "target": target,
            "scan_type": scan_type,
            "status": "not_implemented",
            "message": "Override this method in your extension"
        }


class InterfaceExtension(ExtensionBase):
    """Base class for interface-related extensions"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        super().__init__(name, version)
        self.routes = {}
        self.templates = {}
    
    def register_route(self, path: str, func: Callable, methods: List[str] = None):
        """
        Register a web route
        
        Args:
            path: URL path
            func: Function to handle the route
            methods: HTTP methods (default: ['GET'])
        """
        if methods is None:
            methods = ['GET']
            
        self.routes[path] = {
            "function": func,
            "methods": methods,
            "extension": self.name
        }
        self.logger.debug(f"Registered route: {path}")
    
    def render_template(self, template_name: str, **kwargs) -> str:
        """
        Render a template
        
        Args:
            template_name: Name of template file
            **kwargs: Template variables
            
        Returns:
            Rendered template content
        """
        # Basic template rendering - override for advanced functionality
        template_path = Path(__file__).parent / "templates" / template_name
        
        if template_path.exists():
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Simple variable substitution
            for key, value in kwargs.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
            
            return content
        else:
            self.logger.error(f"Template not found: {template_name}")
            return f"Template '{template_name}' not found"
