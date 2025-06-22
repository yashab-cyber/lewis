"""
LEWIS Configuration Settings
Central configuration management for all LEWIS components
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Settings:
    """Main configuration class for LEWIS"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        default_config = {
            "ai": {
                "model_name": "microsoft/DialoGPT-medium",
                "nlp_model": "en_core_web_sm",
                "max_tokens": 512,
                "temperature": 0.7
            },
            "database": {
                "mongodb_uri": "mongodb://localhost:27017/",
                "database_name": "lewis_db"
            },
            "security": {
                "jwt_secret": "your-secret-key-here",
                "session_timeout": 3600,
                "max_failed_attempts": 5
            },
            "tools": {
                "nmap_path": "/usr/bin/nmap",
                "nikto_path": "/usr/bin/nikto",
                "metasploit_path": "/usr/share/metasploit-framework",
                "output_dir": "outputs"
            },
            "voice": {
                "enabled": True,
                "model_path": "models/vosk-model-en-us-0.22",
                "sample_rate": 16000
            },
            "web": {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": False
            },
            "logging": {
                "level": "INFO",
                "file": "logs/lewis.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_path}: {e}")
                
        return default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save current configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, indent=2)
