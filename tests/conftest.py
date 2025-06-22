"""
Test configuration and shared utilities for LEWIS tests
"""

import os
import sys
import pytest
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test configuration
TEST_CONFIG = {
    "database": {
        "mongodb_uri": "mongodb://localhost:27017/",
        "database_name": "lewis_test_db",
        "collections": {
            "users": "test_users",
            "logs": "test_logs",
            "knowledge": "test_knowledge",
            "reports": "test_reports"
        }
    },
    "security": {
        "secret_key": "test_secret_key_do_not_use_in_production",
        "encryption_enabled": False
    },
    "logging": {
        "level": "DEBUG",
        "file": "tests/logs/test.log"
    }
}

@pytest.fixture
def test_config():
    """Provide test configuration"""
    return TEST_CONFIG

@pytest.fixture
def temp_dir(tmp_path):
    """Provide temporary directory for tests"""
    return tmp_path

@pytest.fixture
def sample_data_dir():
    """Provide sample data directory"""
    return Path(__file__).parent / "data"
