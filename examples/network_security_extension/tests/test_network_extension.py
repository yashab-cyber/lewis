"""
Tests for Network Security Extension
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from examples.network_security_extension.extension import NetworkSecurityExtension
from examples.network_security_extension.commands.network_commands import NetworkCommands
from examples.network_security_extension.tools.network_tools import NetworkTools

class TestNetworkSecurityExtension:
    """Test cases for NetworkSecurityExtension"""
    
    @pytest.fixture
    def config(self):
        """Test configuration"""
        return {
            'scan_timeout': 60,
            'max_threads': 10,
            'port_range': '1-1000'
        }
    
    @pytest.fixture
    async def extension(self, config):
        """Create extension instance for testing"""
        ext = NetworkSecurityExtension(config)
        await ext.initialize()
        yield ext
        await ext.cleanup()
    
    async def test_extension_initialization(self, extension):
        """Test extension initialization"""
        assert extension.name == "network-security-extension"
        assert extension.version == "1.0.0"
        assert extension.scan_timeout == 60
        assert extension.max_threads == 10
        assert extension.port_range == '1-1000'
    
    async def test_comprehensive_network_scan(self, extension):
        """Test comprehensive network scan functionality"""
        target = "192.168.1.100"
        result = await extension.comprehensive_network_scan(target)
        
        assert result['scan_type'] == 'network_comprehensive'
        assert result['target'] == target
        assert 'results' in result
        assert 'details' in result
        assert isinstance(result['results']['hosts_discovered'], int)
    
    async def test_ssl_certificate_analyzer(self, extension):
        """Test SSL certificate analysis"""
        target = "example.com"
        result = await extension.analyze_ssl_certificate(target)
        
        assert result['tool'] == 'ssl-certificate-analyzer'
        assert result['target'] == target
        assert result['port'] == 443
        assert 'certificate_info' in result
        assert 'security_issues' in result

class TestNetworkCommands:
    """Test cases for NetworkCommands"""
    
    @pytest.fixture
    def mock_extension(self):
        """Mock extension for testing"""
        return Mock()
    
    @pytest.fixture
    def commands(self, mock_extension):
        """Create NetworkCommands instance"""
        return NetworkCommands(mock_extension)
    
    async def test_advanced_port_scan(self, commands):
        """Test advanced port scan command"""
        context = Mock()
        args = {
            'target': '192.168.1.100',
            'ports': '1-1000',
            'type': 'syn'
        }
        
        result = await commands.advanced_port_scan(context, args)
        
        assert result['command'] == 'advanced-port-scan'
        assert result['target'] == '192.168.1.100'
        assert result['status'] == 'completed'
        assert 'results' in result
    
    async def test_port_scan_missing_target(self, commands):
        """Test port scan with missing target"""
        context = Mock()
        args = {}
        
        result = await commands.advanced_port_scan(context, args)
        
        assert result['status'] == 'error'
        assert 'Target is required' in result['message']
    
    async def test_vulnerability_assessment(self, commands):
        """Test vulnerability assessment command"""
        context = Mock()
        args = {
            'target': '192.168.1.100',
            'type': 'comprehensive',
            'exploits': True
        }
        
        result = await commands.vulnerability_assessment(context, args)
        
        assert result['command'] == 'vulnerability-assessment'
        assert result['target'] == '192.168.1.100'
        assert result['status'] == 'completed'
        assert 'vulnerabilities' in result
        assert 'risk_score' in result

class TestNetworkTools:
    """Test cases for NetworkTools"""
    
    @pytest.fixture
    def mock_extension(self):
        """Mock extension for testing"""
        return Mock()
    
    @pytest.fixture
    def tools(self, mock_extension):
        """Create NetworkTools instance"""
        return NetworkTools(mock_extension)
    
    async def test_network_performance_monitor(self, tools):
        """Test network performance monitoring"""
        target = "192.168.1.1"
        duration = 30
        
        result = await tools.monitor_network_performance(target, duration)
        
        assert result['tool'] == 'network-performance-monitor'
        assert result['target'] == target
        assert result['duration'] == duration
        assert result['status'] == 'completed'
        assert 'metrics' in result
    
    async def test_dns_security_analyzer(self, tools):
        """Test DNS security analysis"""
        domain = "example.com"
        
        result = await tools.analyze_dns_security(domain)
        
        assert result['tool'] == 'dns-security-analyzer'
        assert result['domain'] == domain
        assert result['status'] == 'completed'
        assert 'analysis' in result
    
    async def test_packet_analyzer(self, tools):
        """Test network packet analysis"""
        interface = "eth0"
        count = 50
        
        result = await tools.analyze_network_packets(interface, count)
        
        assert result['tool'] == 'network-packet-analyzer'
        assert result['interface'] == interface
        assert result['packet_count'] == count
        assert result['status'] == 'completed'
        assert 'analysis' in result

class TestNetworkToolsIntegration:
    """Integration tests for network tools"""
    
    @pytest.fixture
    def config(self):
        """Integration test configuration"""
        return {
            'scan_timeout': 30,
            'max_threads': 5,
            'port_range': '80,443,22'
        }
    
    @pytest.mark.integration
    async def test_full_scan_workflow(self, config):
        """Test complete scan workflow"""
        extension = NetworkSecurityExtension(config)
        await extension.initialize()
        
        try:
            # Test scan workflow
            target = "127.0.0.1"  # Safe target for testing
            
            # Perform scan
            scan_result = await extension.comprehensive_network_scan(target)
            
            # Verify results
            assert scan_result['target'] == target
            assert 'results' in scan_result
            assert 'details' in scan_result
            
        finally:
            await extension.cleanup()
    
    @pytest.mark.performance
    async def test_concurrent_scans(self, config):
        """Test concurrent scan performance"""
        extension = NetworkSecurityExtension(config)
        await extension.initialize()
        
        try:
            targets = ["127.0.0.1", "localhost"]
            
            # Run concurrent scans
            tasks = [
                extension.comprehensive_network_scan(target)
                for target in targets
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Verify all scans completed
            assert len(results) == len(targets)
            for result in results:
                assert 'results' in result
                assert 'details' in result
                
        finally:
            await extension.cleanup()

# Test configuration
pytest_plugins = ['pytest_asyncio']

# Custom markers
pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.network_security
]
