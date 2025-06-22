"""
LEWIS Core System
Central orchestrator for all LEWIS components and services
"""

import asyncio
import signal
import threading
from typing import Dict, Any, Optional
from pathlib import Path

from ai.ai_engine import AIEngine
from ai.nlp_processor import NLPProcessor
from execution.command_executor import CommandExecutor
from learning.knowledge_base import KnowledgeBase
from learning.self_learning import SelfLearningEngine
from storage.database_manager import DatabaseManager
from security.security_manager import SecurityManager
from tools.tool_manager import ToolManager
from core.extension_manager import ExtensionManager
from utils.logger import Logger

class LewisCore:
    """
    Main LEWIS system orchestrator
    Manages all components and provides unified interface
    """
    
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        self.running = False
        
        # Initialize core components
        self._initialize_components()
        
        # Setup signal handlers
        self._setup_signal_handlers()
        
    def _initialize_components(self):
        """Initialize all LEWIS components"""
        try:
            self.logger.info("🔧 Initializing LEWIS components...")
            
            # Database Manager
            self.db_manager = DatabaseManager(self.settings, self.logger)
            
            # Security Manager
            self.security_manager = SecurityManager(self.settings, self.logger)
            
            # Knowledge Base
            self.knowledge_base = KnowledgeBase(self.settings, self.logger, self.db_manager)
            
            # AI Engine
            self.ai_engine = AIEngine(self.settings, self.logger, self.knowledge_base)
            
            # NLP Processor
            self.nlp_processor = NLPProcessor(self.settings, self.logger)
            
            # Tool Manager
            self.tool_manager = ToolManager(self.settings, self.logger)
            
            # Command Executor
            self.command_executor = CommandExecutor(
                self.settings, self.logger, self.tool_manager, self.security_manager
            )
              # Self-Learning Engine
            self.learning_engine = SelfLearningEngine(
                self.settings, self.logger, self.knowledge_base, self.ai_engine
            )
            
            # Extension Manager
            self.extension_manager = ExtensionManager(self.settings, self.logger)
            
            self.logger.info("✅ All LEWIS components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize LEWIS components: {e}")
            raise
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"📡 Received signal {signum}, initiating shutdown...")
            self.shutdown()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def process_command(self, user_input: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Process a user command through the LEWIS pipeline
        
        Args:
            user_input: Natural language command from user
            user_id: User identifier for logging and personalization
            
        Returns:
            Dictionary containing command result and metadata
        """
        try:
            # Log user input
            self.logger.info(f"👤 User {user_id}: {user_input}")
            
            # Security check
            if not self.security_manager.is_command_allowed(user_input, user_id):
                return {
                    "success": False,
                    "error": "Command not allowed by security policy",
                    "type": "security_error"
                }
            
            # Process with NLP
            intent_result = await self.nlp_processor.process_intent(user_input)
            
            # Generate AI response
            ai_response = await self.ai_engine.generate_response(
                user_input, intent_result, user_id
            )
              # Execute command if needed
            execution_result = None
            if intent_result.get("requires_execution"):
                # Check if this is an extension command first
                command_name = intent_result.get("command")
                if command_name and self._is_extension_command(command_name):
                    execution_result = await self._execute_extension_command(
                        command_name, intent_result, user_id
                    )
                else:
                    execution_result = await self.command_executor.execute_command(
                        intent_result, user_id
                    )
            
            # Learn from interaction
            await self.learning_engine.learn_from_interaction(
                user_input, intent_result, ai_response, execution_result
            )
            
            # Prepare response
            response = {
                "success": True,
                "ai_response": ai_response,
                "intent": intent_result,
                "execution": execution_result,
                "timestamp": self._get_timestamp()
            }
            
            self.logger.info(f"✅ Command processed successfully for user {user_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error processing command: {e}")
            return {
                "success": False,
                "error": str(e),
                "type": "processing_error"
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "running": self.running,
            "components": {
                "ai_engine": self.ai_engine.is_ready(),
                "nlp_processor": self.nlp_processor.is_ready(),
                "database": self.db_manager.is_connected(),
                "tools": self.tool_manager.get_available_tools_count(),
                "learning_engine": self.learning_engine.is_active(),
                "extensions": len(self.extension_manager.extensions)
            },
            "stats": {
                "total_commands": self.db_manager.get_command_count(),
                "knowledge_entries": self.knowledge_base.get_entry_count(),
                "active_users": self.security_manager.get_active_users_count()
            }
        }
    
    def start(self):
        """Start LEWIS system"""
        try:
            self.logger.info("🚀 Starting LEWIS system...")
            self.running = True
            
            # Load extensions
            self.extension_manager.load_all_extensions()
            
            # Start background services
            self._start_background_services()
            
            self.logger.info("✅ LEWIS system started successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start LEWIS system: {e}")
            raise
    
    def shutdown(self):
        """Gracefully shutdown LEWIS system"""
        if not self.running:
            return
            
        self.logger.info("🛑 Shutting down LEWIS system...")
        self.running = False
        
        try:
            # Unload extensions
            if hasattr(self, 'extension_manager'):
                self.extension_manager.unload_all_extensions()
            
            # Stop background services
            if hasattr(self, 'learning_engine'):
                self.learning_engine.stop()
            
            # Close database connections
            if hasattr(self, 'db_manager'):
                self.db_manager.close()
            
            self.logger.info("✅ LEWIS system shutdown complete")
            
        except Exception as e:
            self.logger.error(f"❌ Error during shutdown: {e}")
    
    def _is_extension_command(self, command_name: str) -> bool:
        """Check if a command belongs to an extension"""
        all_extension_commands = self.extension_manager.get_all_commands()
        return command_name in all_extension_commands
    
    async def _execute_extension_command(self, command_name: str, intent_result: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Execute a command from an extension"""
        try:
            # Extract arguments from intent
            args = intent_result.get("parameters", {})
            
            # Execute extension command
            result = self.extension_manager.execute_command(command_name, **args)
            
            return {
                "success": True,
                "result": result,
                "type": "extension_command",
                "extension": True
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error executing extension command {command_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "type": "extension_command_error"
            }
    
    def _start_background_services(self):
        """Start background services in separate threads"""
        if self.settings.get("learning.enabled", True):
            learning_thread = threading.Thread(
                target=self.learning_engine.start_background_learning,
                daemon=True
            )
            learning_thread.start()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_available_commands(self) -> Dict[str, str]:
        """Get list of available commands and their descriptions"""
        # Get core commands
        core_commands = self.nlp_processor.get_supported_intents()
        
        # Get extension commands
        extension_commands = self.extension_manager.get_all_commands()
        extension_command_descriptions = {
            cmd: info.get("description", "Extension command")
            for cmd, info in extension_commands.items()
        }
        
        # Combine all commands
        all_commands = {**core_commands, **extension_command_descriptions}
        return all_commands
    
    def get_tool_status(self) -> Dict[str, Any]:
        """Get status of all integrated tools"""
        # Get core tool status
        core_tools = self.tool_manager.get_tool_status()
        
        # Get extension tools
        extension_tools = self.extension_manager.get_all_tools()
        extension_tool_status = {
            tool: {"status": "available", "extension": True}
            for tool in extension_tools.keys()
        }
        
        return {
            "core_tools": core_tools,
            "extension_tools": extension_tool_status,
            "total_tools": len(core_tools) + len(extension_tools)
        }
    
    def get_extension_status(self) -> Dict[str, Any]:
        """Get extension system status"""
        return self.extension_manager.get_extension_status()
