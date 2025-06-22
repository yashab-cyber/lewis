#!/usr/bin/env python3
"""
Version Consistency Checker for LEWIS
Ensures all version references across the project are consistent
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

class VersionChecker:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.version_files = {}
        self.inconsistencies = []
        
    def get_main_version(self) -> str:
        """Get the main version from __init__.py"""
        init_file = self.project_root / "__init__.py"
        if init_file.exists():
            content = init_file.read_text()
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
        return None
    
    def check_file_versions(self, file_path: Path, patterns: List[str]) -> List[Tuple[str, int, str]]:
        """Check for version patterns in a file"""
        versions = []
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        version = match.group(1)
                        if re.match(r'\d+\.\d+\.\d+', version):  # Valid semantic version
                            versions.append((str(file_path), line_num, version))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return versions
    
    def check_json_files(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """Check version in JSON files"""
        json_files = {}
        
        for json_file in self.project_root.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                versions = []
                if isinstance(data, dict):
                    if 'version' in data:
                        versions.append(('version', '', data['version']))
                    if 'lewis_version' in data:
                        versions.append(('lewis_version', '', data['lewis_version']))
                
                if versions:
                    json_files[str(json_file)] = versions
                    
            except Exception as e:
                print(f"Error reading JSON {json_file}: {e}")
        
        return json_files
    
    def check_yaml_files(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """Check version in YAML files"""
        yaml_files = {}
        
        for yaml_file in self.project_root.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                versions = []
                if isinstance(data, dict):
                    if 'version' in data:
                        versions.append(('version', '', data['version']))
                    
                    # Check nested structures
                    def check_nested(obj, path=""):
                        if isinstance(obj, dict):
                            for key, value in obj.items():
                                if key == 'version' and isinstance(value, str):
                                    versions.append((f'{path}.{key}' if path else key, '', value))
                                else:
                                    check_nested(value, f'{path}.{key}' if path else key)
                        elif isinstance(obj, list):
                            for i, item in enumerate(obj):
                                check_nested(item, f'{path}[{i}]')
                    
                    check_nested(data)
                
                if versions:
                    yaml_files[str(yaml_file)] = versions
                    
            except Exception as e:
                print(f"Error reading YAML {yaml_file}: {e}")
        
        return yaml_files
    
    def run_check(self) -> Dict[str, any]:
        """Run comprehensive version check"""
        main_version = self.get_main_version()
        if not main_version:
            return {"error": "Could not find main version in __init__.py"}
        
        print(f"🔍 Checking version consistency against main version: {main_version}")
        
        # Patterns to search for versions
        version_patterns = [
            r'version["\']?\s*[:=]\s*["\']([^"\']+)["\']',
            r'__version__\s*=\s*["\']([^"\']+)["\']',
            r'version-([0-9]+\.[0-9]+\.[0-9]+)',
            r'v([0-9]+\.[0-9]+\.[0-9]+)',
            r'Version:\s*([0-9]+\.[0-9]+\.[0-9]+)',
            r'lewis_version["\']?\s*[:=]\s*["\']>=?([^"\']+)["\']'
        ]
        
        results = {
            "main_version": main_version,
            "file_versions": {},
            "json_versions": {},
            "yaml_versions": {},
            "inconsistencies": []
        }
        
        # Check common file types
        file_types = [
            "*.py", "*.md", "*.txt", "*.sh", "*.dockerfile", "*.toml"
        ]
        
        for pattern in file_types:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    versions = self.check_file_versions(file_path, version_patterns)
                    if versions:
                        results["file_versions"][str(file_path)] = versions
        
        # Check JSON and YAML files
        results["json_versions"] = self.check_json_files()
        results["yaml_versions"] = self.check_yaml_files()
        
        # Find inconsistencies
        all_versions = set()
        
        # Collect all versions
        for file_versions in results["file_versions"].values():
            for _, _, version in file_versions:
                # Clean version strings
                clean_version = re.sub(r'[>=<~^]', '', version).strip()
                if re.match(r'\d+\.\d+\.\d+', clean_version):
                    all_versions.add(clean_version)
        
        for file_versions in results["json_versions"].values():
            for _, _, version in file_versions:
                clean_version = re.sub(r'[>=<~^]', '', version).strip()
                if re.match(r'\d+\.\d+\.\d+', clean_version):
                    all_versions.add(clean_version)
        
        for file_versions in results["yaml_versions"].values():
            for _, _, version in file_versions:
                clean_version = re.sub(r'[>=<~^]', '', version).strip()
                if re.match(r'\d+\.\d+\.\d+', clean_version):
                    all_versions.add(clean_version)
        
        # Check for inconsistencies
        if len(all_versions) > 1:
            results["inconsistencies"] = list(all_versions - {main_version})
        
        return results
    
    def print_report(self, results: Dict):
        """Print detailed version consistency report"""
        print("\n" + "="*60)
        print("LEWIS VERSION CONSISTENCY REPORT")
        print("="*60)
        
        print(f"\n📌 Main Version: {results['main_version']}")
        
        if results["inconsistencies"]:
            print(f"\n❌ Found {len(results['inconsistencies'])} inconsistent versions:")
            for version in results["inconsistencies"]:
                print(f"   - {version}")
        else:
            print("\n✅ All versions are consistent!")
        
        print(f"\n📁 Files checked:")
        total_files = len(results["file_versions"]) + len(results["json_versions"]) + len(results["yaml_versions"])
        print(f"   - Python/Text files: {len(results['file_versions'])}")
        print(f"   - JSON files: {len(results['json_versions'])}")
        print(f"   - YAML files: {len(results['yaml_versions'])}")
        print(f"   - Total: {total_files}")
        
        if results["inconsistencies"]:
            print(f"\n🔍 Detailed inconsistencies:")
            
            # Show files with inconsistent versions
            for file_path, versions in results["file_versions"].items():
                for file_name, line_num, version in versions:
                    clean_version = re.sub(r'[>=<~^]', '', version).strip()
                    if clean_version in results["inconsistencies"]:
                        print(f"   📄 {file_path}:{line_num} -> {version}")
            
            for file_path, versions in results["json_versions"].items():
                for field, _, version in versions:
                    clean_version = re.sub(r'[>=<~^]', '', version).strip()
                    if clean_version in results["inconsistencies"]:
                        print(f"   📄 {file_path} ({field}) -> {version}")
            
            for file_path, versions in results["yaml_versions"].items():
                for field, _, version in versions:
                    clean_version = re.sub(r'[>=<~^]', '', version).strip()
                    if clean_version in results["inconsistencies"]:
                        print(f"   📄 {file_path} ({field}) -> {version}")

def main():
    """Main function"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    checker = VersionChecker(project_root)
    results = checker.run_check()
    checker.print_report(results)
    
    # Exit with error code if inconsistencies found
    if results.get("inconsistencies"):
        exit(1)
    else:
        print("\n🎉 Version consistency check passed!")
        exit(0)

if __name__ == "__main__":
    main()
