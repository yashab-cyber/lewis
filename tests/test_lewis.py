#!/usr/bin/env python3
"""
LEWIS Testing Suite
Comprehensive unit tests, integration tests, and validation scripts
"""

import unittest
import asyncio
import json
import tempfile
import os
import sys
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import Settings, load_settings
from utils.logger import Logger, setup_logger
from core.lewis_core import LewisCore
from ai.ai_engine import AIEngine
from ai.nlp_processor import NLPProcessor
from tools.tool_manager import ToolManager
from security.security_manager import SecurityManager
from storage.database_manager import DatabaseManager
from execution.command_executor import CommandExecutor

class TestSettings(unittest.TestCase):
    """Test configuration and settings"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_config = {
            "ai": {
                "model_name": "test-model",
                "temperature": 0.7,
                "max_tokens": 512
            },
            "security": {
                "jwt_secret": "test-secret",
                "session_timeout": 3600
            },
            "database": {
                "type": "json",
                "path": "test_data"
            }
        }
    
    def test_settings_loading(self):
        """Test settings loading and validation"""
        settings = Settings(self.test_config)
        
        self.assertEqual(settings.get("ai", {}).get("model_name"), "test-model")
        self.assertEqual(settings.get("security", {}).get("jwt_secret"), "test-secret")
        self.assertEqual(settings.get("database", {}).get("type"), "json")
    
    def test_settings_defaults(self):
        """Test default settings values"""
        settings = Settings({})
        
        # Should have default values
        self.assertIsNotNone(settings.get("ai", {}))
        self.assertIsNotNone(settings.get("security", {}))
    
    def test_settings_update(self):
        """Test settings update functionality"""
        settings = Settings(self.test_config)
        
        settings.update({"ai": {"temperature": 0.8}})
        self.assertEqual(settings.get("ai", {}).get("temperature"), 0.8)

class TestLogger(unittest.TestCase):
    """Test logging functionality"""
    
    def setUp(self):
        """Set up test logger"""
        self.settings = Settings({"logging": {"level": "DEBUG"}})
        self.logger = setup_logger(self.settings)
    
    def test_logger_creation(self):
        """Test logger creation"""
        self.assertIsInstance(self.logger, Logger)
        self.assertIsNotNone(self.logger.logger)
    
    def test_logging_levels(self):
        """Test different logging levels"""
        with patch('logging.Logger.info') as mock_info:
            self.logger.info("Test info message")
            mock_info.assert_called_once()
        
        with patch('logging.Logger.error') as mock_error:
            self.logger.error("Test error message")
            mock_error.assert_called_once()

class TestNLPProcessor(unittest.TestCase):
    """Test NLP processing functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({})
        self.logger = Logger(self.settings)
        self.nlp_processor = NLPProcessor(self.settings, self.logger)
    
    def test_intent_recognition(self):
        """Test intent recognition"""
        test_cases = [
            ("scan 192.168.1.1", "network_scan"),
            ("run nmap on example.com", "network_scan"),
            ("check for sql injection", "web_vulnerability"),
            ("generate report", "report_generation"),
            ("help", "help"),
            ("what is my ip", "information_query")
        ]
        
        for command, expected_intent in test_cases:
            intent = self.nlp_processor.extract_intent(command)
            self.assertIn(expected_intent, intent.lower())
    
    def test_entity_extraction(self):
        """Test entity extraction"""
        command = "scan 192.168.1.1 with nmap"
        entities = self.nlp_processor.extract_entities(command)
        
        self.assertIn("target", entities)
        self.assertIn("tool", entities)
        self.assertEqual(entities["target"], "192.168.1.1")
        self.assertEqual(entities["tool"], "nmap")
    
    def test_command_preprocessing(self):
        """Test command preprocessing"""
        test_cases = [
            ("Scan the network 192.168.1.0/24", "scan 192.168.1.0/24"),
            ("Please run nmap on example.com", "nmap example.com"),
            ("Can you check for vulnerabilities?", "vulnerability scan")
        ]
        
        for raw_command, expected in test_cases:
            processed = self.nlp_processor.preprocess_command(raw_command)
            self.assertIsInstance(processed, str)
            self.assertGreater(len(processed), 0)

class TestToolManager(unittest.TestCase):
    """Test tool management functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({})
        self.logger = Logger(self.settings)
        self.tool_manager = ToolManager(self.settings, self.logger)
    
    def test_tool_registration(self):
        """Test tool registration"""
        test_tool = {
            "name": "test_tool",
            "command_template": "test_command {target}",
            "category": "testing",
            "description": "Test tool for unit testing"
        }
        
        self.tool_manager.register_tool("test_tool", test_tool)
        tools = self.tool_manager.get_available_tools()
        
        self.assertIn("test_tool", [tool["name"] for tool in tools])
    
    def test_tool_execution_preparation(self):
        """Test tool execution preparation"""
        command = self.tool_manager.prepare_tool_execution(
            "nmap", 
            {"target": "example.com", "options": ["-sV"]}
        )
        
        self.assertIsInstance(command, str)
        self.assertIn("nmap", command)
        self.assertIn("example.com", command)
    
    def test_tool_validation(self):
        """Test tool validation"""
        # Test valid tool
        self.assertTrue(self.tool_manager.validate_tool("nmap"))
        
        # Test invalid tool
        self.assertFalse(self.tool_manager.validate_tool("nonexistent_tool"))

class TestSecurityManager(unittest.TestCase):
    """Test security management functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({
            "security": {
                "jwt_secret": "test-secret-key",
                "session_timeout": 3600
            }
        })
        self.logger = Logger(self.settings)
        self.security_manager = SecurityManager(self.settings, self.logger)
    
    def test_token_generation(self):
        """Test JWT token generation"""
        user_data = {"user_id": "test_user", "permissions": ["execute_commands"]}
        token = self.security_manager.generate_token(user_data)
        
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)
    
    def test_token_verification(self):
        """Test JWT token verification"""
        user_data = {"user_id": "test_user", "permissions": ["execute_commands"]}
        token = self.security_manager.generate_token(user_data)
        
        verified_data = self.security_manager.verify_token(token)
        self.assertIsNotNone(verified_data)
        self.assertEqual(verified_data["user_id"], "test_user")
    
    def test_command_authorization(self):
        """Test command authorization"""
        # Test authorized command
        self.assertTrue(
            self.security_manager.is_command_authorized("nmap example.com", "test_user")
        )
        
        # Test dangerous command
        self.assertFalse(
            self.security_manager.is_command_authorized("rm -rf /", "test_user")
        )
    
    def test_target_validation(self):
        """Test target validation"""
        # Test valid targets
        valid_targets = [
            "192.168.1.1",
            "example.com",
            "subdomain.example.com"
        ]
        
        for target in valid_targets:
            self.assertTrue(self.security_manager.validate_target(target))
        
        # Test invalid targets
        invalid_targets = [
            "localhost",
            "127.0.0.1",
            "internal.company.com"
        ]
        
        for target in invalid_targets:
            self.assertFalse(self.security_manager.validate_target(target))

class TestCommandExecutor(unittest.TestCase):
    """Test command execution functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({})
        self.logger = Logger(self.settings)
        self.security_manager = SecurityManager(self.settings, self.logger)
        self.executor = CommandExecutor(self.settings, self.logger, self.security_manager)
    
    @patch('subprocess.run')
    def test_safe_command_execution(self, mock_run):
        """Test safe command execution"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Test output",
            stderr=""
        )
        
        result = asyncio.run(
            self.executor.execute_command("echo 'test'", "test_user")
        )
        
        self.assertTrue(result["success"])
        self.assertIn("output", result)
    
    def test_command_sanitization(self):
        """Test command sanitization"""
        dangerous_commands = [
            "rm -rf /",
            ":(){ :|:& };:",  # Fork bomb
            "cat /etc/passwd",
            "sudo su -"
        ]
        
        for cmd in dangerous_commands:
            sanitized = self.executor.sanitize_command(cmd)
            self.assertNotEqual(cmd, sanitized)
    
    def test_timeout_handling(self):
        """Test command timeout handling"""
        with patch('asyncio.wait_for') as mock_wait:
            mock_wait.side_effect = asyncio.TimeoutError()
            
            result = asyncio.run(
                self.executor.execute_command("sleep 1000", "test_user")
            )
            
            self.assertFalse(result["success"])
            self.assertIn("timeout", result["error"].lower())

class TestDatabaseManager(unittest.TestCase):
    """Test database management functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({
            "database": {
                "type": "json",
                "path": "test_data"
            }
        })
        self.logger = Logger(self.settings)
        self.db_manager = DatabaseManager(self.settings, self.logger)
    
    def tearDown(self):
        """Clean up test data"""
        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
    
    def test_data_storage(self):
        """Test data storage functionality"""
        test_data = {
            "command": "test command",
            "timestamp": datetime.now().isoformat(),
            "user_id": "test_user",
            "success": True
        }
        
        # Store data
        asyncio.run(self.db_manager.store_command_history(test_data))
        
        # Retrieve data
        history = asyncio.run(self.db_manager.get_command_history("test_user", limit=1))
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["command"], "test command")
    
    def test_data_retrieval(self):
        """Test data retrieval functionality"""
        # Store multiple test records
        for i in range(5):
            test_data = {
                "command": f"test command {i}",
                "timestamp": datetime.now().isoformat(),
                "user_id": "test_user",
                "success": True
            }
            asyncio.run(self.db_manager.store_command_history(test_data))
        
        # Test retrieval with limit
        history = asyncio.run(self.db_manager.get_command_history("test_user", limit=3))
        self.assertEqual(len(history), 3)
        
        # Test retrieval without limit
        all_history = asyncio.run(self.db_manager.get_command_history("test_user"))
        self.assertEqual(len(all_history), 5)

class TestAIEngine(unittest.TestCase):
    """Test AI engine functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({
            "ai": {
                "model_name": "test-model",
                "temperature": 0.7
            }
        })
        self.logger = Logger(self.settings)
        self.ai_engine = AIEngine(self.settings, self.logger)
    
    @patch('transformers.pipeline')
    def test_response_generation(self, mock_pipeline):
        """Test AI response generation"""
        mock_pipeline.return_value = Mock(
            return_value=[{"generated_text": "Test AI response"}]
        )
        
        response = asyncio.run(
            self.ai_engine.generate_response("test query", "test_user", {})
        )
        
        self.assertIsInstance(response, dict)
        self.assertIn("response", response)
    
    def test_context_management(self):
        """Test conversation context management"""
        # Add context
        self.ai_engine.add_context("test_user", "previous command", "previous response")
        
        # Get context
        context = self.ai_engine.get_conversation_context("test_user")
        
        self.assertIsInstance(context, list)
        self.assertGreater(len(context), 0)

class TestLewisCore(unittest.TestCase):
    """Test LEWIS core functionality integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({
            "ai": {"model_name": "test-model"},
            "security": {"jwt_secret": "test-secret"},
            "database": {"type": "json", "path": "test_data"}
        })
        self.logger = Logger(self.settings)
        self.lewis_core = LewisCore(self.settings, self.logger)
    
    def tearDown(self):
        """Clean up test data"""
        import shutil
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
    
    @patch('execution.command_executor.CommandExecutor.execute_command')
    async def test_command_processing(self, mock_execute):
        """Test end-to-end command processing"""
        mock_execute.return_value = {
            "success": True,
            "output": "Test command output",
            "execution_time": 1.5
        }
        
        result = await self.lewis_core.process_command("test command", "test_user")
        
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
    
    def test_system_status(self):
        """Test system status reporting"""
        status = asyncio.run(self.lewis_core.get_system_status())
        
        self.assertIsInstance(status, dict)
        self.assertIn("status", status)
        self.assertIn("uptime", status)

class TestValidation(unittest.TestCase):
    """Test system validation and health checks"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({})
        self.logger = Logger(self.settings)
    
    def test_dependency_validation(self):
        """Test that all required dependencies are available"""
        required_modules = [
            "asyncio",
            "json",
            "datetime",
            "pathlib",
            "logging",
            "hashlib",
            "uuid"
        ]
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                self.fail(f"Required module {module} is not available")
    
    def test_configuration_validation(self):
        """Test configuration file validation"""
        # Test valid configuration
        valid_config = {
            "ai": {"model_name": "test-model"},
            "security": {"jwt_secret": "test-secret"},
            "database": {"type": "json"}
        }
        
        settings = Settings(valid_config)
        self.assertIsNotNone(settings.get("ai"))
        self.assertIsNotNone(settings.get("security"))
        
        # Test invalid configuration
        invalid_config = {
            "ai": {},  # Missing required fields
            "security": {}  # Missing required fields
        }
        
        # Should still work with defaults
        settings = Settings(invalid_config)
        self.assertIsNotNone(settings.get("ai"))
    
    def test_tool_availability(self):
        """Test cybersecurity tool availability"""
        tool_manager = ToolManager(self.settings, self.logger)
        tools = tool_manager.get_available_tools()
        
        # Should have at least basic tools
        tool_names = [tool["name"] for tool in tools]
        basic_tools = ["nmap", "nikto", "sqlmap", "gobuster"]
        
        for tool in basic_tools:
            self.assertIn(tool, tool_names, f"Tool {tool} not available")

class TestPerformance(unittest.TestCase):
    """Test system performance and resource usage"""
    
    def setUp(self):
        """Set up test environment"""
        self.settings = Settings({})
        self.logger = Logger(self.settings)
    
    def test_response_time(self):
        """Test system response time"""
        import time
        
        start_time = time.time()
        
        # Simulate typical operations
        nlp_processor = NLPProcessor(self.settings, self.logger)
        intent = nlp_processor.extract_intent("scan example.com")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Should respond within reasonable time (< 1 second for simple operations)
        self.assertLess(response_time, 1.0)
    
    def test_memory_usage(self):
        """Test memory usage"""
        import psutil
        import gc
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Create multiple objects
        objects = []
        for i in range(1000):
            lewis_core = LewisCore(self.settings, self.logger)
            objects.append(lewis_core)
        
        peak_memory = process.memory_info().rss
        
        # Clean up
        del objects
        gc.collect()
        
        final_memory = process.memory_info().rss
        
        # Memory should be reasonably bounded
        memory_increase = peak_memory - initial_memory
        self.assertLess(memory_increase, 100 * 1024 * 1024)  # Less than 100MB increase

def run_all_tests():
    """Run all test suites"""
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Run specific test class if provided
    if len(sys.argv) > 1:
        test_class = sys.argv[1]
        if hasattr(sys.modules[__name__], test_class):
            suite = unittest.TestLoader().loadTestsFromTestCase(
                getattr(sys.modules[__name__], test_class)
            )
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        else:
            print(f"Test class {test_class} not found")
    else:
        # Run all tests
        success = run_all_tests()
        sys.exit(0 if success else 1)
