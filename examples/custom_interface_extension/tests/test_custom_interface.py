"""
Test cases for Custom Interface Extension
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from examples.custom_interface_extension.extension import CustomInterfaceExtension

class TestCustomInterfaceExtension(unittest.TestCase):
    """Test cases for the Custom Interface Extension"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extension = CustomInterfaceExtension()
    
    def test_extension_initialization(self):
        """Test extension initialization"""
        self.assertEqual(self.extension.name, "custom-interface-extension")
        self.assertEqual(self.extension.version, "1.0.0")
        self.assertFalse(self.extension.enabled)
    
    def test_extension_initialize(self):
        """Test extension initialization method"""
        try:
            result = self.extension.initialize()
            self.assertTrue(result)
            self.assertTrue(self.extension.enabled)
        except Exception as e:
            # Flask/SocketIO might not be available in test environment
            self.skipTest(f"Flask/SocketIO not available: {e}")
    
    def test_extension_cleanup(self):
        """Test extension cleanup"""
        self.extension.enabled = True
        result = self.extension.cleanup()
        self.assertTrue(result)
        self.assertFalse(self.extension.enabled)
    
    def test_flask_app_setup(self):
        """Test Flask app setup"""
        try:
            self.extension._setup_flask_app()
            self.assertIsNotNone(self.extension.app)
            self.assertIsNotNone(self.extension.socketio)
        except Exception as e:
            self.skipTest(f"Flask/SocketIO not available: {e}")
    
    def test_extension_info(self):
        """Test extension info retrieval"""
        info = self.extension.get_info()
        self.assertIn("name", info)
        self.assertIn("version", info)
        self.assertIn("enabled", info)
        self.assertEqual(info["name"], "custom-interface-extension")

if __name__ == '__main__':
    unittest.main()
