#!/usr/bin/env python3
"""
LEWIS Python Version Validator
Validates Python 3.11.9 compatibility and dependencies
"""

import sys
import subprocess
import pkg_resources
from packaging import version

def check_python_version():
    """Check if Python version is 3.11.9"""
    current_version = sys.version_info
    required_version = (3, 11, 9)
    
    print(f"Current Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
    print(f"Required Python version: {required_version[0]}.{required_version[1]}.{required_version[2]}")
    
    if current_version[:3] == required_version:
        print("✅ Python version is correct!")
        return True
    elif current_version[:2] == required_version[:2]:
        print("⚠️  Python minor version matches (3.11), but patch version differs")
        print("   This should still be compatible with LEWIS")
        return True
    else:
        print("❌ Python version mismatch!")
        print(f"   Expected Python 3.11.x, got {current_version.major}.{current_version.minor}.{current_version.micro}")
        return False

def check_critical_packages():
    """Check if critical packages are installed and compatible"""
    critical_packages = [
        'torch',
        'transformers', 
        'flask',
        'numpy',
        'requests'
    ]
    
    print("\nChecking critical packages:")
    all_ok = True
    
    for package in critical_packages:
        try:
            pkg = pkg_resources.get_distribution(package)
            print(f"✅ {package}: {pkg.version}")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package}: Not installed")
            all_ok = False
        except Exception as e:
            print(f"⚠️  {package}: Error checking - {e}")
            all_ok = False
    
    return all_ok

def test_imports():
    """Test importing critical LEWIS modules"""
    test_imports = [
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
        ('flask', 'Flask'),
        ('numpy', 'NumPy'),
        ('sklearn', 'Scikit-learn')
    ]
    
    print("\nTesting imports:")
    all_ok = True
    
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name}: Import successful")
        except ImportError as e:
            print(f"❌ {name}: Import failed - {e}")
            all_ok = False
        except Exception as e:
            print(f"⚠️  {name}: Import error - {e}")
            all_ok = False
    
    return all_ok

def main():
    """Main validation function"""
    print("LEWIS Python Environment Validator")
    print("=" * 40)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check packages
    packages_ok = check_critical_packages()
    
    # Test imports
    imports_ok = test_imports()
    
    # Overall result
    print("\n" + "=" * 40)
    if python_ok and packages_ok and imports_ok:
        print("🎉 All checks passed! LEWIS should work correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some issues found. LEWIS may not work properly.")
        if not python_ok:
            print("   - Fix Python version by using pyenv")
        if not packages_ok:
            print("   - Install missing packages with pip")
        if not imports_ok:
            print("   - Resolve import errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
