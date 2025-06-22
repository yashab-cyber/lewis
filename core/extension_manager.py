"""
LEWIS Extension Manager
Manages loading, initialization, and lifecycle of LEWIS extensions
"""

import json
import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Type
import yaml

from core.extension_base import ExtensionBase
from utils.logger import Logger

class ExtensionManager:
    """
    Manages LEWIS extensions discovery, loading, and lifecycle
    """
    
    def __init__(self, settings: Dict[str, Any], logger: Logger):
        self.settings = settings
        self.logger = logger
        self.extensions: Dict[str, ExtensionBase] = {}
        self.extension_paths = self._get_extension_paths()
        self.loaded_extensions = set()
        
    def _get_extension_paths(self) -> List[Path]:
        """Get configured extension paths"""
        paths = []
        
        # Default extension paths
        default_paths = [
            Path(__file__).parent.parent / "examples",
            Path(__file__).parent.parent / "extensions",
            Path.home() / ".lewis" / "extensions"
        ]
        
        # Add configured paths
        config_paths = self.settings.get("extensions", {}).get("paths", [])
        for path_str in config_paths:
            paths.append(Path(path_str))
        
        # Add default paths
        paths.extend(default_paths)
        
        # Return existing paths only
        return [path for path in paths if path.exists()]
    
    def discover_extensions(self) -> List[Dict[str, Any]]:
        """Discover available extensions"""
        discovered = []
        
        for path in self.extension_paths:
            self.logger.debug(f"Scanning for extensions in: {path}")
            
            # Look for extension directories
            for item in path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    manifest_path = item / "manifest.json"
                    
                    if manifest_path.exists():
                        try:
                            extension_info = self._load_extension_manifest(manifest_path)
                            extension_info['path'] = str(item)
                            discovered.append(extension_info)
                            self.logger.debug(f"Discovered extension: {extension_info['name']}")
                        except Exception as e:
                            self.logger.warning(f"Failed to load manifest from {manifest_path}: {e}")
        
        return discovered
    
    def _load_extension_manifest(self, manifest_path: Path) -> Dict[str, Any]:
        """Load extension manifest file"""
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Validate required fields
        required_fields = ['name', 'version', 'entry_point']
        for field in required_fields:
            if field not in manifest:
                raise ValueError(f"Missing required field: {field}")
        
        return manifest
    
    def load_extension(self, extension_info: Dict[str, Any]) -> bool:
        """Load a single extension"""
        try:
            extension_name = extension_info['name']
            extension_path = Path(extension_info['path'])
            entry_point = extension_info['entry_point']
            
            if extension_name in self.loaded_extensions:
                self.logger.warning(f"Extension {extension_name} already loaded")
                return True
            
            # Add extension path to Python path
            if str(extension_path.parent) not in sys.path:
                sys.path.insert(0, str(extension_path.parent))
            
            # Import extension module
            module_name, class_name = entry_point.rsplit('.', 1)
            module_path = f"{extension_path.name}.{module_name}"
            
            self.logger.debug(f"Importing extension module: {module_path}")
            module = importlib.import_module(module_path)
            
            # Get extension class
            extension_class = getattr(module, class_name)
            
            # Validate extension class
            if not issubclass(extension_class, ExtensionBase):
                raise ValueError(f"Extension class {class_name} must inherit from ExtensionBase")
            
            # Instantiate extension
            extension_instance = extension_class()
            
            # Initialize extension
            if extension_instance.initialize():
                self.extensions[extension_name] = extension_instance
                self.loaded_extensions.add(extension_name)
                self.logger.info(f"✅ Loaded extension: {extension_name} v{extension_info['version']}")
                return True
            else:
                self.logger.error(f"❌ Failed to initialize extension: {extension_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Failed to load extension {extension_info['name']}: {e}")
            return False
    
    def load_all_extensions(self) -> Dict[str, bool]:
        """Load all discovered extensions"""
        self.logger.info("🔌 Loading LEWIS extensions...")
        
        discovered_extensions = self.discover_extensions()
        load_results = {}
        
        for extension_info in discovered_extensions:
            extension_name = extension_info['name']
            
            # Check if extension is enabled
            if self._is_extension_enabled(extension_name):
                load_results[extension_name] = self.load_extension(extension_info)
            else:
                self.logger.debug(f"Extension {extension_name} is disabled, skipping")
                load_results[extension_name] = False
        
        loaded_count = sum(1 for success in load_results.values() if success)
        total_count = len(load_results)
        
        self.logger.info(f"📊 Extensions loaded: {loaded_count}/{total_count}")
        
        return load_results
    
    def _is_extension_enabled(self, extension_name: str) -> bool:
        """Check if extension is enabled in configuration"""
        extension_config = self.settings.get("extensions", {})
        
        # Check global enable/disable
        if not extension_config.get("enabled", True):
            return False
        
        # Check extension-specific configuration
        extension_settings = extension_config.get("extension_settings", {})
        specific_config = extension_settings.get(extension_name, {})
        
        return specific_config.get("enabled", True)
    
    def unload_extension(self, extension_name: str) -> bool:
        """Unload a specific extension"""
        if extension_name not in self.extensions:
            self.logger.warning(f"Extension {extension_name} not loaded")
            return False
        
        try:
            extension = self.extensions[extension_name]
            
            # Cleanup extension
            if extension.cleanup():
                del self.extensions[extension_name]
                self.loaded_extensions.discard(extension_name)
                self.logger.info(f"🔌 Unloaded extension: {extension_name}")
                return True
            else:
                self.logger.error(f"Failed to cleanup extension: {extension_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error unloading extension {extension_name}: {e}")
            return False
    
    def unload_all_extensions(self):
        """Unload all loaded extensions"""
        self.logger.info("🔌 Unloading all extensions...")
        
        extension_names = list(self.extensions.keys())
        for extension_name in extension_names:
            self.unload_extension(extension_name)
    
    def get_extension(self, extension_name: str) -> Optional[ExtensionBase]:
        """Get loaded extension instance"""
        return self.extensions.get(extension_name)
    
    def list_extensions(self) -> Dict[str, Dict[str, Any]]:
        """List all loaded extensions with their info"""
        extension_info = {}
        
        for name, extension in self.extensions.items():
            extension_info[name] = extension.get_info()
        
        return extension_info
    
    def execute_command(self, command_name: str, *args, **kwargs) -> Any:
        """Execute a command from any loaded extension"""
        for extension in self.extensions.values():
            if command_name in extension.get_commands():
                return extension.execute_command(command_name, *args, **kwargs)
        
        raise ValueError(f"Command '{command_name}' not found in any loaded extension")
    
    def execute_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Execute a tool from any loaded extension"""
        for extension in self.extensions.values():
            if tool_name in extension.get_tools():
                return extension.execute_tool(tool_name, *args, **kwargs)
        
        raise ValueError(f"Tool '{tool_name}' not found in any loaded extension")
    
    def get_all_commands(self) -> Dict[str, Dict[str, Any]]:
        """Get all commands from all loaded extensions"""
        all_commands = {}
        
        for extension in self.extensions.values():
            commands = extension.get_commands()
            all_commands.update(commands)
        
        return all_commands
    
    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all tools from all loaded extensions"""
        all_tools = {}
        
        for extension in self.extensions.values():
            tools = extension.get_tools()
            all_tools.update(tools)
        
        return all_tools
    
    def reload_extension(self, extension_name: str) -> bool:
        """Reload a specific extension"""
        if extension_name not in self.extensions:
            self.logger.warning(f"Extension {extension_name} not loaded")
            return False
        
        # Find extension info
        discovered = self.discover_extensions()
        extension_info = None
        
        for info in discovered:
            if info['name'] == extension_name:
                extension_info = info
                break
        
        if not extension_info:
            self.logger.error(f"Cannot find extension info for {extension_name}")
            return False
        
        # Unload and reload
        if self.unload_extension(extension_name):
            return self.load_extension(extension_info)
        
        return False
    
    def get_extension_status(self) -> Dict[str, Any]:
        """Get extension system status"""
        discovered = self.discover_extensions()
        
        return {
            'total_discovered': len(discovered),
            'total_loaded': len(self.extensions),
            'loaded_extensions': list(self.extensions.keys()),
            'extension_paths': [str(path) for path in self.extension_paths],
            'extensions_enabled': self.settings.get("extensions", {}).get("enabled", True)
        }