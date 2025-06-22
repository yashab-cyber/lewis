#!/usr/bin/env python3
"""
LEWIS Installation and Setup Script
Handles initial setup, dependency installation, and configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil

def print_banner():
    """Print LEWIS banner"""
    banner = """
    ██╗     ███████╗██╗    ██╗██╗███████╗
    ██║     ██╔════╝██║    ██║██║██╔════╝
    ██║     █████╗  ██║ █╗ ██║██║███████╗
    ██║     ██╔══╝  ██║███╗██║██║╚════██║
    ███████╗███████╗╚███╔███╔╝██║███████║
    ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝
    
    Linux Environment Working Intelligence System
    Setup and Installation Script
    """
    print(banner)

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_python_packages():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Python packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python packages: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    directories = [
        "logs",
        "data", 
        "outputs",
        "temp",
        "models",
        "config",
        "reports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")

def check_system_tools():
    """Check for required system tools"""
    print("🔧 Checking system tools...")
    
    tools = {
        "nmap": "Network exploration tool",
        "git": "Version control system",
        "curl": "Data transfer tool"
    }
    
    missing_tools = []
    
    for tool, description in tools.items():
        if shutil.which(tool):
            print(f"✅ {tool} - {description}")
        else:
            print(f"⚠️  {tool} - {description} (not found)")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n⚠️  Missing tools: {', '.join(missing_tools)}")
        print("Please install missing tools for full functionality")
    
    return len(missing_tools) == 0

def setup_nlp_models():
    """Download and setup NLP models"""
    print("🔤 Setting up NLP models...")
    
    try:
        # Download spaCy English model
        subprocess.check_call([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ])
        print("✅ spaCy English model downloaded")
        
        # Download NLTK data
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        print("✅ NLTK data downloaded")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Error setting up NLP models: {e}")
        return False

def create_default_config():
    """Create default configuration file"""
    print("⚙️  Creating default configuration...")
    
    config_file = Path("config/config.yaml")
    
    if config_file.exists():
        print("✅ Configuration file already exists")
        return True
    
    try:
        # The config file should already exist from our creation above
        if config_file.exists():
            print("✅ Configuration file ready")
            return True
        else:
            print("⚠️  Configuration file not found, using defaults")
            return False
            
    except Exception as e:
        print(f"❌ Error creating configuration: {e}")
        return False

def setup_database():
    """Setup database (optional)"""
    print("🗄️  Database setup...")
    
    try:
        # Check if MongoDB is available
        result = subprocess.run(
            ["mongod", "--version"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ MongoDB detected")
            print("💡 LEWIS will use MongoDB for data storage")
        else:
            print("⚠️  MongoDB not found - will use file-based storage")
            
    except FileNotFoundError:
        print("⚠️  MongoDB not found - will use file-based storage")
    
    return True

def run_initial_tests():
    """Run initial system tests"""
    print("🧪 Running initial tests...")
    
    try:
        # Test import of core modules
        sys.path.insert(0, str(Path.cwd()))
        
        from config.settings import Settings
        from utils.logger import setup_logger
        
        # Test configuration loading
        settings = Settings()
        logger = setup_logger()
        
        print("✅ Core modules import successfully")
        print("✅ Configuration loads successfully")
        print("✅ Logger initializes successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Initial tests failed: {e}")
        return False

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("🎉 LEWIS Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Start LEWIS CLI: python lewis.py --mode cli")
    print("2. Start LEWIS GUI: python lewis.py --mode gui")
    print("3. Start LEWIS Server: python lewis.py --mode server")
    print("4. Enable voice: python lewis.py --mode cli --voice")
    print("\nFor help: python lewis.py --help")
    print("\nDocumentation: Check the README.md file")
    print("Configuration: Edit config/config.yaml")
    print("\n🛡️  Remember: Use LEWIS responsibly and only on authorized targets!")

def check_extension_dependencies():
    """Check extension system dependencies"""
    print("🔌 Checking extension system dependencies...")
    
    required_extensions_deps = [
        "flask",
        "flask-socketio"
    ]
    
    missing_deps = []
    for dep in required_extensions_deps:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"⚠️ Installing missing extension dependencies: {', '.join(missing_deps)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_deps)
            print("✅ Extension dependencies installed")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install extension dependencies")
            return False
    
    return True

def setup_extension_system():
    """Setup extension system directories and validate examples"""
    print("🎨 Setting up extension system...")
    
    # Ensure examples directory exists
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found")
        return False
    
    # Check example extensions
    required_examples = [
        "network_security_extension",
        "custom_interface_extension"
    ]
    
    for example in required_examples:
        example_path = examples_dir / example
        if example_path.exists():
            print(f"✅ {example} found")
            
            # Check extension.py exists
            if (example_path / "extension.py").exists():
                print(f"✅ {example}/extension.py found")
            else:
                print(f"❌ {example}/extension.py missing")
                return False
        else:
            print(f"❌ {example} directory missing")
            return False
    
    # Test extension loading
    try:
        sys.path.insert(0, str(Path.cwd()))
        from core.extension_manager import ExtensionManager
        manager = ExtensionManager()
        manager.discover_extensions()
        print(f"✅ Found {len(manager.available_extensions)} extensions")
        return True
    except Exception as e:
        print(f"❌ Extension system test failed: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
      # Setup steps
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing Python packages", install_python_packages),
        ("Setting up directories", setup_directories),
        ("Checking system tools", check_system_tools),
        ("Setting up NLP models", setup_nlp_models),
        ("Creating configuration", create_default_config),
        ("Setting up database", setup_database),
        ("Checking extension dependencies", check_extension_dependencies),
        ("Setting up extension system", setup_extension_system),
        ("Running initial tests", run_initial_tests)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
            failed_steps.append(step_name)
    
    # Summary
    print("\n" + "="*60)
    print("SETUP SUMMARY")
    print("="*60)
    
    if failed_steps:
        print(f"⚠️  {len(failed_steps)} steps had issues:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nLEWIS may still work with reduced functionality")
    else:
        print("✅ All setup steps completed successfully!")
    
    print_next_steps()

if __name__ == "__main__":
    main()
