#!/usr/bin/env python3
"""
Environment Setup Script for LEWIS
Performs comprehensive environment configuration and testing
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    banner = """
    ██╗     ███████╗██╗    ██╗██╗███████╗
    ██║     ██╔════╝██║    ██║██║██╔════╝
    ██║     █████╗  ██║ █╗ ██║██║███████╗
    ██║     ██╔══╝  ██║███╗██║██║╚════██║
    ███████╗███████╗╚███╔███╔╝██║███████║
    ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝
    
    LEWIS Environment Setup Script
    """
    print(banner)

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} (3.8+ required)")
        return False
    
    # Operating system
    system = platform.system()
    print(f"✅ Operating System: {system}")
    
    # Available tools
    tools = ["git", "curl", "wget"]
    for tool in tools:
        if shutil.which(tool):
            print(f"✅ {tool} available")
        else:
            print(f"⚠️ {tool} not found (optional)")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        "data/database",
        "data/uploads", 
        "data/reports",
        "data/backups",
        "logs",
        "cache/model_cache",
        "cache/threat_feeds",
        "cache/temp_uploads",
        "models"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created {directory}")
        else:
            print(f"✅ {directory} exists")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    requirements_files = ["requirements.txt", "requirements-dev.txt"]
    
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"Installing from {req_file}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", req_file
                ])
                print(f"✅ {req_file} installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {req_file}: {e}")
                return False
        else:
            print(f"⚠️ {req_file} not found")
    
    return True

def test_imports():
    """Test critical imports"""
    print("\n🧪 Testing critical imports...")
    
    critical_modules = [
        "flask",
        "transformers", 
        "torch",
        "numpy",
        "pandas",
        "pymongo"
    ]
    
    failed_imports = []
    
    for module in critical_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️ Failed imports: {', '.join(failed_imports)}")
        print("Some LEWIS features may not work properly.")
        return False
    
    return True

def setup_configuration():
    """Setup initial configuration"""
    print("\n⚙️ Setting up configuration...")
    
    config_file = Path("config/config.yaml")
    if config_file.exists():
        print("✅ Configuration file exists")
        
        # Test configuration loading
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            print("✅ Configuration file is valid")
        except Exception as e:
            print(f"❌ Configuration file error: {e}")
            return False
    else:
        print("❌ Configuration file not found")
        return False
    
    return True

def setup_database():
    """Setup database"""
    print("\n🗄️ Setting up database...")
    
    # Create SQLite database for local storage
    try:
        import sqlite3
        db_path = Path("data/database/lewis.db")
        
        if not db_path.exists():
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create basic tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    level TEXT,
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            print("✅ SQLite database created")
        else:
            print("✅ Database already exists")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def validate_installation():
    """Validate LEWIS installation"""
    print("\n✅ Validating installation...")
    
    # Test core module import
    try:
        sys.path.insert(0, str(Path.cwd()))
        from core.lewis_core import LewisCore
        print("✅ LEWIS core module imports successfully")
    except Exception as e:
        print(f"❌ LEWIS core import failed: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print_banner()
    
    steps = [
        ("System Requirements", check_system_requirements),
        ("Directory Structure", create_directories),
        ("Dependencies", install_dependencies),
        ("Import Testing", test_imports),
        ("Configuration", setup_configuration),
        ("Database Setup", setup_database),
        ("Installation Validation", validate_installation)
    ]
    
    print("Starting LEWIS environment setup...\n")
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"{'='*60}")
        try:
            if not step_function():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ {step_name} failed with exception: {e}")
            failed_steps.append(step_name)
    
    print(f"{'='*60}")
    print("SETUP COMPLETE")
    print(f"{'='*60}")
    
    if not failed_steps:
        print("🎉 LEWIS environment setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python scripts/download_models.py")
        print("2. Run: python lewis.py --mode cli")
        print("3. Try: python validate_lewis.py")
    else:
        print(f"⚠️ Setup completed with {len(failed_steps)} issues:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nPlease resolve these issues before running LEWIS.")

if __name__ == "__main__":
    main()
