#!/usr/bin/env python3
"""
LEWIS Validation Script
Validates the complete LEWIS installation and all components
"""

import os
import sys
import asyncio
import subprocess
import importlib
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class LEWISValidator:
    """Comprehensive validation for LEWIS system"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def print_header(self):
        """Print validation header"""
        print("=" * 70)
        print("LEWIS - Linux Environment Working Intelligence System")
        print("System Validation & Health Check")
        print("=" * 70)
        print(f"Validation started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def print_section(self, title):
        """Print section header"""
        print(f"\n{'─' * 50}")
        print(f"🔍 {title}")
        print(f"{'─' * 50}")
    
    def check_python_version(self):
        """Check Python version compatibility"""
        self.print_section("Python Environment")
        
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            self.passed.append(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        else:
            self.errors.append(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
    
    def check_required_modules(self):
        """Check if all required Python modules are available"""
        self.print_section("Required Python Modules")
        
        required_modules = [
            ("asyncio", "Core async support"),
            ("json", "JSON processing"),
            ("pathlib", "Path handling"),
            ("datetime", "Date/time operations"),
            ("logging", "Logging system"),
            ("hashlib", "Cryptographic hashing"),
            ("uuid", "UUID generation"),
            ("subprocess", "Process execution"),
            ("threading", "Multi-threading support"),
            ("queue", "Queue operations"),
        ]
        
        for module, description in required_modules:
            try:
                importlib.import_module(module)
                self.passed.append(f"✅ {module} - {description}")
            except ImportError:
                self.errors.append(f"❌ {module} - {description} (Missing)")
    
    def check_optional_modules(self):
        """Check optional modules for enhanced functionality"""
        self.print_section("Optional Enhancement Modules")
        
        optional_modules = [
            ("transformers", "AI/ML capabilities"),
            ("torch", "Deep learning support"),
            ("speech_recognition", "Voice input"),
            ("pyttsx3", "Text-to-speech"),
            ("tkinter", "GUI interface"),
            ("fastapi", "Web API"),
            ("matplotlib", "Data visualization"),
            ("plotly", "Interactive charts"),
            ("psutil", "System monitoring"),
            ("reportlab", "PDF generation"),
        ]
        
        for module, description in optional_modules:
            try:
                importlib.import_module(module)
                self.passed.append(f"✅ {module} - {description}")
            except ImportError:
                self.warnings.append(f"⚠️  {module} - {description} (Optional - Install for enhanced features)")
    
    def check_project_structure(self):
        """Validate project directory structure"""
        self.print_section("Project Structure")
        
        required_dirs = [
            "core", "interfaces", "ai", "tools", "execution", 
            "security", "storage", "learning", "config", "utils",
            "voice", "analytics", "detection", "reports", "tests"
        ]
        
        required_files = [
            "lewis.py", "setup.py", "requirements.txt", "README.md",
            "config/config.yaml", "config/settings.py"
        ]
        
        # Check directories
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.passed.append(f"✅ Directory: {dir_name}/")
            else:
                self.errors.append(f"❌ Missing directory: {dir_name}/")
        
        # Check files
        for file_name in required_files:
            file_path = project_root / file_name
            if file_path.exists() and file_path.is_file():
                self.passed.append(f"✅ File: {file_name}")
            else:
                self.errors.append(f"❌ Missing file: {file_name}")
    
    def check_core_modules(self):
        """Test core LEWIS modules"""
        self.print_section("Core LEWIS Modules")
        
        core_modules = [
            ("config.settings", "Configuration system"),
            ("utils.logger", "Logging system"),
            ("core.lewis_core", "Core engine"),
            ("ai.ai_engine", "AI engine"),
            ("ai.nlp_processor", "NLP processor"),
            ("tools.tool_manager", "Tool manager"),
            ("security.security_manager", "Security manager"),
            ("storage.database_manager", "Database manager"),
            ("execution.command_executor", "Command executor"),
        ]
        
        for module, description in core_modules:
            try:
                importlib.import_module(module)
                self.passed.append(f"✅ {module} - {description}")
            except ImportError as e:
                self.errors.append(f"❌ {module} - {description} (Import Error: {str(e)})")
            except Exception as e:
                self.warnings.append(f"⚠️  {module} - {description} (Warning: {str(e)})")
    
    def check_interface_modules(self):
        """Test interface modules"""
        self.print_section("Interface Modules")
        
        interface_modules = [
            ("interfaces.cli_interface", "CLI interface"),
            ("interfaces.gui_interface", "GUI interface"),
            ("interfaces.web_interface", "Web interface"),
        ]
        
        for module, description in interface_modules:
            try:
                importlib.import_module(module)
                self.passed.append(f"✅ {module} - {description}")
            except ImportError as e:
                self.errors.append(f"❌ {module} - {description} (Import Error: {str(e)})")
            except Exception as e:
                self.warnings.append(f"⚠️  {module} - {description} (Warning: {str(e)})")
    
    def check_advanced_modules(self):
        """Test advanced feature modules"""
        self.print_section("Advanced Feature Modules")
        
        advanced_modules = [
            ("voice.voice_assistant", "Voice assistant"),
            ("analytics.analytics_engine", "Analytics engine"),
            ("detection.threat_detection", "Threat detection"),
            ("reports.report_generator", "Report generator"),
        ]
        
        for module, description in advanced_modules:
            try:
                importlib.import_module(module)
                self.passed.append(f"✅ {module} - {description}")
            except ImportError as e:
                self.warnings.append(f"⚠️  {module} - {description} (Import Error: {str(e)})")
            except Exception as e:
                self.warnings.append(f"⚠️  {module} - {description} (Warning: {str(e)})")
    
    def check_configuration(self):
        """Validate configuration files"""
        self.print_section("Configuration Files")
        
        try:
            from config.settings import load_settings
            settings = load_settings()
            self.passed.append("✅ Configuration loaded successfully")
            
            # Check required config sections
            required_sections = ["ai", "security", "database", "tools"]
            for section in required_sections:
                if settings.get(section):
                    self.passed.append(f"✅ Config section: {section}")
                else:
                    self.warnings.append(f"⚠️  Missing config section: {section}")
            
        except Exception as e:
            self.errors.append(f"❌ Configuration error: {str(e)}")
    
    def check_system_tools(self):
        """Check system tools availability"""
        self.print_section("System Tools")
        
        tools_to_check = [
            ("nmap", "Network scanning"),
            ("nikto", "Web vulnerability scanner"),
            ("sqlmap", "SQL injection testing"),
            ("gobuster", "Directory/file brute-forcer"),
            ("python3", "Python interpreter"),
            ("pip", "Package installer"),
        ]
        
        for tool, description in tools_to_check:
            try:
                result = subprocess.run(
                    ["which", tool] if os.name != 'nt' else ["where", tool],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.passed.append(f"✅ {tool} - {description}")
                else:
                    self.warnings.append(f"⚠️  {tool} - {description} (Not found - Install for full functionality)")
            except:
                self.warnings.append(f"⚠️  {tool} - {description} (Check failed)")
    
    async def check_core_functionality(self):
        """Test core functionality"""
        self.print_section("Core Functionality Tests")
        
        try:
            # Test settings loading
            from config.settings import load_settings
            settings = load_settings()
            self.passed.append("✅ Settings loading")
            
            # Test logger setup
            from utils.logger import setup_logger
            logger = setup_logger(settings)
            self.passed.append("✅ Logger initialization")
            
            # Test core initialization
            from core.lewis_core import LewisCore
            lewis_core = LewisCore(settings, logger)
            await lewis_core.initialize()
            self.passed.append("✅ LEWIS core initialization")
            
            # Test command processing (mock)
            result = await lewis_core.process_command("help", "test_user")
            if result and isinstance(result, dict):
                self.passed.append("✅ Command processing")
            else:
                self.warnings.append("⚠️  Command processing (Unexpected result format)")
            
        except Exception as e:
            self.errors.append(f"❌ Core functionality test failed: {str(e)}")
    
    def run_unit_tests(self):
        """Run unit tests if available"""
        self.print_section("Unit Tests")
        
        test_file = project_root / "tests" / "test_lewis.py"
        if test_file.exists():
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", str(test_file), "-v"],
                    capture_output=True,
                    text=True,
                    cwd=str(project_root)
                )
                
                if result.returncode == 0:
                    self.passed.append("✅ Unit tests passed")
                else:
                    self.warnings.append("⚠️  Some unit tests failed")
                    
            except Exception as e:
                self.warnings.append(f"⚠️  Unit test execution failed: {str(e)}")
        else:
            self.warnings.append("⚠️  Unit test file not found")
    
    def print_summary(self):
        """Print validation summary"""
        print(f"\n{'═' * 70}")
        print("VALIDATION SUMMARY")
        print(f"{'═' * 70}")
        
        print(f"\n✅ PASSED: {len(self.passed)} checks")
        for item in self.passed:
            print(f"   {item}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS: {len(self.warnings)} items")
            for item in self.warnings:
                print(f"   {item}")
        
        if self.errors:
            print(f"\n❌ ERRORS: {len(self.errors)} critical issues")
            for item in self.errors:
                print(f"   {item}")
        
        print(f"\n{'─' * 70}")
        
        if not self.errors:
            if not self.warnings:
                print("🎉 EXCELLENT! LEWIS is fully validated and ready to use!")
                status = "EXCELLENT"
            else:
                print("✅ GOOD! LEWIS is functional with some optional features missing.")
                status = "GOOD"
        else:
            print("❌ ISSUES FOUND! Please resolve the errors before using LEWIS.")
            status = "ISSUES"
        
        print(f"{'─' * 70}")
        print(f"Validation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return status
    
    async def run_all_checks(self):
        """Run all validation checks"""
        self.print_header()
        
        self.check_python_version()
        self.check_required_modules()
        self.check_optional_modules()
        self.check_project_structure()
        self.check_core_modules()
        self.check_interface_modules()
        self.check_advanced_modules()
        self.check_configuration()
        self.check_system_tools()
        await self.check_core_functionality()
        self.run_unit_tests()
        
        return self.print_summary()

async def main():
    """Main validation function"""
    validator = LEWISValidator()
    status = await validator.run_all_checks()
    
    # Exit with appropriate code
    if status == "ISSUES":
        sys.exit(1)
    elif status == "GOOD":
        sys.exit(0)
    else:  # EXCELLENT
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
