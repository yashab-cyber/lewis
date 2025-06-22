# LEWIS Development Guide

Comprehensive guide for developers who want to contribute to LEWIS, create plugins, or extend functionality.

## 👨‍💻 Overview

This guide provides detailed information for developers working with LEWIS, including setup instructions, architecture overview, coding standards, and contribution guidelines.

## 📋 Table of Contents

1. [Development Environment](#development-environment)
2. [Architecture Overview](#architecture-overview)
3. [Coding Standards](#coding-standards)
4. [Testing Framework](#testing-framework)
5. [Plugin Development](#plugin-development)
6. [API Development](#api-development)
7. [Database Development](#database-development)
8. [Frontend Development](#frontend-development)

## 🛠️ Development Environment

### Prerequisites

```bash
# System requirements
Python 3.9+
Node.js 16+
PostgreSQL 12+
Redis 6+
Git
Docker (optional)
```

### Local Setup

```bash
# Clone repository
git clone https://github.com/yashab-cyber/lewis.git
cd lewis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Setup database
python lewis.py db init --dev

# Run tests
python -m pytest

# Start development server
python lewis.py --dev
```

### Development Tools

```yaml
# .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Docker Development

```dockerfile
# Dockerfile.dev
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Copy source code
COPY . .

# Development command
CMD ["python", "lewis.py", "--dev", "--reload"]
```

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  lewis-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
      - "5678:5678"  # debugpy
    volumes:
      - .:/app
      - /app/venv
    environment:
      - LEWIS_ENV=development
      - LEWIS_DEBUG=true
    depends_on:
      - postgres-dev
      - redis-dev
  
  postgres-dev:
    image: postgres:13
    environment:
      POSTGRES_DB: lewis_dev
      POSTGRES_USER: lewis
      POSTGRES_PASSWORD: lewis_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data
  
  redis-dev:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_dev_data:
```

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────┐
│                 Web Interface                   │
├─────────────────────────────────────────────────┤
│                   REST API                      │
├─────────────────────────────────────────────────┤
│  CLI Interface  │  Core Engine  │  AI Engine   │
├─────────────────────────────────────────────────┤
│  Tool Manager   │  Security Mgr │  Report Gen  │
├─────────────────────────────────────────────────┤
│    Database     │     Cache     │  Message Q   │
└─────────────────────────────────────────────────┘
```

### Core Components

```python
# core/lewis_core.py
class LEWISCore:
    """Main LEWIS system orchestrator"""
    
    def __init__(self, config_path=None):
        self.config = ConfigManager(config_path)
        self.database = DatabaseManager(self.config.database)
        self.cache = CacheManager(self.config.cache)
        self.security = SecurityManager(self.config.security)
        self.ai_engine = AIEngine(self.config.ai)
        self.tool_manager = ToolManager(self.config.tools)
        
    async def initialize(self):
        """Initialize all system components"""
        await self.database.initialize()
        await self.cache.initialize()
        await self.ai_engine.initialize()
        
    async def execute_scan(self, target, scan_config):
        """Execute security scan"""
        scan_id = await self.create_scan_session(target, scan_config)
        
        try:
            # Execute scan phases
            results = await self._execute_scan_phases(scan_id, target, scan_config)
            
            # Process results with AI
            analyzed_results = await self.ai_engine.analyze(results)
            
            # Store results
            await self.database.store_scan_results(scan_id, analyzed_results)
            
            return scan_id
            
        except Exception as e:
            await self.handle_scan_error(scan_id, e)
            raise
```

### Module Structure

```
lewis/
├── core/                   # Core system components
│   ├── lewis_core.py      # Main orchestrator
│   ├── config_manager.py  # Configuration management
│   ├── plugin_manager.py  # Plugin system
│   └── workflow_engine.py # Workflow management
│
├── ai/                    # AI and ML components
│   ├── ai_engine.py       # Main AI engine
│   ├── nlp_processor.py   # Natural language processing
│   ├── threat_analyzer.py # Threat analysis
│   └── models/            # ML models
│
├── scanning/              # Scanning engines
│   ├── network_scanner.py # Network scanning
│   ├── web_scanner.py     # Web application scanning
│   ├── host_scanner.py    # Host-based scanning
│   └── cloud_scanner.py   # Cloud security scanning
│
├── interfaces/            # User interfaces
│   ├── cli_interface.py   # Command-line interface
│   ├── web_interface.py   # Web interface
│   ├── api_interface.py   # REST API
│   └── templates/         # Web templates
│
├── integrations/          # External tool integrations
│   ├── base_integration.py # Base integration class
│   ├── nmap_integration.py # Nmap integration
│   ├── burp_integration.py # Burp Suite integration
│   └── siem_integrations/ # SIEM integrations
│
└── utils/                 # Utility modules
    ├── database.py        # Database utilities
    ├── cache.py           # Caching utilities
    ├── encryption.py      # Encryption utilities
    └── validators.py      # Input validators
```

## 📝 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# File header template
"""
LEWIS - Linux Environment Working Intelligence System
Copyright (c) 2024 ZehraSec

Module: [module_description]
Author: [author_name]
Created: [date]
"""

# Import organization
import os
import sys
from typing import Dict, List, Optional, Union

import asyncio
import aiohttp
from pydantic import BaseModel

from core.lewis_core import LEWISCore
from utils.validators import validate_target

# Class structure
class ScanEngine(BaseModel):
    """Base class for all scanning engines.
    
    This class provides the foundation for implementing specific
    scanning capabilities within LEWIS.
    
    Attributes:
        name: Human-readable name of the scanning engine
        version: Version of the scanning engine
        config: Configuration parameters for the engine
    """
    
    name: str
    version: str
    config: Dict
    
    def __init__(self, config: Dict):
        """Initialize the scanning engine.
        
        Args:
            config: Configuration dictionary containing engine parameters
            
        Raises:
            ValidationError: If configuration is invalid
        """
        super().__init__(**config)
        self.validate_config()
    
    async def scan(self, target: str) -> Dict:
        """Perform security scan on target.
        
        Args:
            target: Target to scan (URL, IP, etc.)
            
        Returns:
            Dictionary containing scan results
            
        Raises:
            ScanError: If scan fails
        """
        raise NotImplementedError("Subclasses must implement scan method")
    
    def validate_config(self) -> None:
        """Validate engine configuration."""
        required_fields = self.get_required_config_fields()
        missing_fields = [
            field for field in required_fields 
            if field not in self.config
        ]
        
        if missing_fields:
            raise ValueError(f"Missing required config fields: {missing_fields}")
```

### Error Handling

```python
# Custom exception hierarchy
class LEWISError(Exception):
    """Base exception for all LEWIS errors."""
    pass

class ConfigurationError(LEWISError):
    """Raised when configuration is invalid."""
    pass

class ScanError(LEWISError):
    """Raised when scan operations fail."""
    pass

class ValidationError(LEWISError):
    """Raised when input validation fails."""
    pass

# Error handling pattern
async def execute_scan(self, target: str) -> Dict:
    """Execute scan with proper error handling."""
    try:
        # Validate input
        if not self.validate_target(target):
            raise ValidationError(f"Invalid target: {target}")
        
        # Execute scan
        results = await self._perform_scan(target)
        
        # Validate results
        if not self.validate_results(results):
            raise ScanError("Invalid scan results")
        
        return results
        
    except ValidationError:
        self.logger.error(f"Target validation failed: {target}")
        raise
    except ScanError:
        self.logger.error(f"Scan execution failed: {target}")
        raise
    except Exception as e:
        self.logger.error(f"Unexpected error during scan: {e}")
        raise ScanError(f"Scan failed: {e}") from e
```

### Async Programming

```python
# Async best practices
import asyncio
from typing import List, AsyncGenerator

class AsyncScanManager:
    """Manages asynchronous scanning operations."""
    
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def scan_targets(self, targets: List[str]) -> AsyncGenerator[Dict, None]:
        """Scan multiple targets concurrently."""
        async def scan_with_semaphore(target: str) -> Dict:
            async with self.semaphore:
                return await self.scan_target(target)
        
        # Create tasks for all targets
        tasks = [scan_with_semaphore(target) for target in targets]
        
        # Yield results as they complete
        for coro in asyncio.as_completed(tasks):
            result = await coro
            yield result
    
    async def scan_target(self, target: str) -> Dict:
        """Scan individual target."""
        try:
            async with self.session.get(target) as response:
                data = await response.text()
                return self.analyze_response(data)
        except Exception as e:
            return {"error": str(e), "target": target}
```

## 🧪 Testing Framework

### Test Structure

```
tests/
├── unit/                  # Unit tests
│   ├── test_core.py
│   ├── test_scanners.py
│   └── test_utils.py
├── integration/           # Integration tests
│   ├── test_api.py
│   ├── test_database.py
│   └── test_integrations.py
├── e2e/                   # End-to-end tests
│   ├── test_workflows.py
│   └── test_ui.py
├── fixtures/              # Test data
│   ├── scan_results.json
│   └── test_configs.yaml
└── conftest.py           # Pytest configuration
```

### Test Examples

```python
# tests/unit/test_scan_engine.py
import pytest
from unittest.mock import AsyncMock, MagicMock

from scanning.network_scanner import NetworkScanner
from core.exceptions import ValidationError

class TestNetworkScanner:
    """Test cases for NetworkScanner class."""
    
    @pytest.fixture
    def scanner_config(self):
        """Default scanner configuration."""
        return {
            "timeout": 30,
            "max_ports": 1000,
            "scan_technique": "tcp_syn"
        }
    
    @pytest.fixture
    def network_scanner(self, scanner_config):
        """NetworkScanner instance for testing."""
        return NetworkScanner(scanner_config)
    
    @pytest.mark.asyncio
    async def test_scan_valid_target(self, network_scanner):
        """Test scanning a valid target."""
        target = "192.168.1.1"
        
        # Mock the actual scanning process
        network_scanner._perform_scan = AsyncMock(
            return_value={"open_ports": [22, 80, 443]}
        )
        
        result = await network_scanner.scan(target)
        
        assert "open_ports" in result
        assert len(result["open_ports"]) == 3
        network_scanner._perform_scan.assert_called_once_with(target)
    
    @pytest.mark.asyncio
    async def test_scan_invalid_target(self, network_scanner):
        """Test scanning an invalid target."""
        invalid_target = "invalid_target"
        
        with pytest.raises(ValidationError):
            await network_scanner.scan(invalid_target)
    
    def test_validate_config_missing_fields(self):
        """Test configuration validation with missing fields."""
        incomplete_config = {"timeout": 30}
        
        with pytest.raises(ValueError):
            NetworkScanner(incomplete_config)

# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient

from interfaces.api_interface import app

class TestAPI:
    """Integration tests for REST API."""
    
    @pytest.fixture
    def client(self):
        """Test client for API."""
        return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_scan_endpoint(self, client):
        """Test scan creation endpoint."""
        scan_data = {
            "target": "https://example.com",
            "scan_type": "web",
            "options": {}
        }
        
        response = client.post("/api/v1/scans", json=scan_data)
        
        assert response.status_code == 201
        assert "scan_id" in response.json()
    
    def test_unauthorized_access(self, client):
        """Test unauthorized API access."""
        response = client.get("/api/v1/scans")
        
        assert response.status_code == 401

# conftest.py
import pytest
import asyncio
from unittest.mock import MagicMock

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_database():
    """Mock database for testing."""
    return MagicMock()

@pytest.fixture
def test_config():
    """Test configuration."""
    return {
        "database": {
            "url": "sqlite:///:memory:",
            "pool_size": 1
        },
        "cache": {
            "backend": "memory"
        },
        "security": {
            "secret_key": "test_secret_key"
        }
    }
```

### Test Configuration

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=lewis
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --asyncio-mode=auto
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
    unit: marks tests as unit tests
```

## 🔌 Plugin Development

### Plugin Architecture

```python
# plugins/base_plugin.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BasePlugin(ABC):
    """Base class for all LEWIS plugins."""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.enabled = True
        
    @abstractmethod
    def initialize(self, lewis_core) -> bool:
        """Initialize plugin with LEWIS core."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of plugin capabilities."""
        pass
    
    def get_config_schema(self) -> Dict:
        """Return plugin configuration schema."""
        return {}
    
    def validate_config(self) -> bool:
        """Validate plugin configuration."""
        return True
    
    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass

# Example plugin implementation
class CustomScannerPlugin(BasePlugin):
    """Example custom scanner plugin."""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.name = "Custom Scanner"
        self.version = "1.0.0"
        
    def initialize(self, lewis_core) -> bool:
        """Initialize plugin."""
        self.lewis_core = lewis_core
        
        # Register scanner
        self.lewis_core.register_scanner(
            "custom_scan",
            self.perform_custom_scan
        )
        
        return True
    
    def get_capabilities(self) -> List[str]:
        """Return plugin capabilities."""
        return ["scanning", "analysis"]
    
    async def perform_custom_scan(self, target: str) -> Dict:
        """Perform custom scan."""
        # Implement custom scanning logic
        return {
            "target": target,
            "findings": [],
            "scanner": self.name
        }
    
    def get_config_schema(self) -> Dict:
        """Return configuration schema."""
        return {
            "type": "object",
            "properties": {
                "timeout": {"type": "integer", "default": 30},
                "max_depth": {"type": "integer", "default": 3}
            }
        }
```

### Plugin Manager

```python
# core/plugin_manager.py
import importlib
import os
from typing import Dict, List
from plugins.base_plugin import BasePlugin

class PluginManager:
    """Manages LEWIS plugins."""
    
    def __init__(self, plugin_directory: str = "plugins"):
        self.plugin_directory = plugin_directory
        self.plugins: Dict[str, BasePlugin] = {}
        self.enabled_plugins: List[str] = []
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins."""
        plugin_files = []
        
        for file in os.listdir(self.plugin_directory):
            if file.endswith("_plugin.py") and not file.startswith("__"):
                plugin_files.append(file[:-3])  # Remove .py extension
        
        return plugin_files
    
    def load_plugin(self, plugin_name: str, config: Dict = None) -> bool:
        """Load and initialize a plugin."""
        try:
            # Import plugin module
            module_name = f"plugins.{plugin_name}"
            module = importlib.import_module(module_name)
            
            # Find plugin class
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BasePlugin) and 
                    attr != BasePlugin):
                    plugin_class = attr
                    break
            
            if not plugin_class:
                raise ValueError(f"No plugin class found in {module_name}")
            
            # Create plugin instance
            plugin = plugin_class(config)
            
            # Validate configuration
            if not plugin.validate_config():
                raise ValueError(f"Invalid configuration for plugin {plugin_name}")
            
            # Initialize plugin
            if plugin.initialize(self.lewis_core):
                self.plugins[plugin_name] = plugin
                self.enabled_plugins.append(plugin_name)
                return True
            
        except Exception as e:
            print(f"Failed to load plugin {plugin_name}: {e}")
        
        return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            plugin.cleanup()
            del self.plugins[plugin_name]
            
            if plugin_name in self.enabled_plugins:
                self.enabled_plugins.remove(plugin_name)
            
            return True
        
        return False
    
    def get_plugin_info(self, plugin_name: str) -> Dict:
        """Get plugin information."""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            return {
                "name": plugin.name,
                "version": plugin.version,
                "enabled": plugin.enabled,
                "capabilities": plugin.get_capabilities(),
                "config_schema": plugin.get_config_schema()
            }
        
        return {}
```

## 📊 Database Development

### Database Schema

```python
# models/database_models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

Base = declarative_base()

class Scan(Base):
    """Scan session model."""
    __tablename__ = "scans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target = Column(String(255), nullable=False)
    scan_type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    config = Column(JSONB)
    
    # Relationships
    findings = relationship("Finding", back_populates="scan")
    reports = relationship("Report", back_populates="scan")

class Finding(Base):
    """Security finding model."""
    __tablename__ = "findings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"))
    severity = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    risk_score = Column(Integer)
    cve_id = Column(String(20))
    remediation = Column(Text)
    evidence = Column(JSONB)
    
    # Relationships
    scan = relationship("Scan", back_populates="findings")

class Report(Base):
    """Report model."""
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id"))
    report_type = Column(String(50), nullable=False)
    format = Column(String(20), nullable=False)
    generated_at = Column(DateTime, nullable=False)
    file_path = Column(String(500))
    
    # Relationships
    scan = relationship("Scan", back_populates="reports")
```

### Database Migrations

```python
# migrations/migration_manager.py
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from models.database_models import Base

class MigrationManager:
    """Manages database migrations."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        
    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(self.engine)
    
    def run_migrations(self):
        """Run pending migrations."""
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", self.database_url)
        command.upgrade(alembic_cfg, "head")
    
    def create_migration(self, message: str):
        """Create new migration."""
        alembic_cfg = Config("alembic.ini")
        command.revision(alembic_cfg, message=message, autogenerate=True)
```

## 🌐 Frontend Development

### Web Interface Stack

- **Framework**: React + TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit
- **API Client**: Axios
- **Charts**: Chart.js
- **Build Tool**: Vite

### Component Structure

```typescript
// src/components/ScanDashboard.tsx
import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchScans, createScan } from '../store/scanSlice';

interface ScanDashboardProps {
  className?: string;
}

const ScanDashboard: React.FC<ScanDashboardProps> = ({ className }) => {
  const dispatch = useDispatch();
  const { scans, loading, error } = useSelector((state: RootState) => state.scans);
  const [selectedScan, setSelectedScan] = useState<string | null>(null);
  
  useEffect(() => {
    dispatch(fetchScans());
  }, [dispatch]);
  
  const handleCreateScan = async (target: string, scanType: string) => {
    try {
      await dispatch(createScan({ target, scan_type: scanType }));
    } catch (error) {
      console.error('Failed to create scan:', error);
    }
  };
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return (
    <div className={`scan-dashboard ${className}`}>
      <ScanControls onCreateScan={handleCreateScan} />
      <ScanList 
        scans={scans}
        selectedScan={selectedScan}
        onSelectScan={setSelectedScan}
      />
      {selectedScan && (
        <ScanDetails scanId={selectedScan} />
      )}
    </div>
  );
};

export default ScanDashboard;
```

### API Integration

```typescript
// src/api/lewis-api.ts
import axios, { AxiosInstance, AxiosResponse } from 'axios';

class LEWISApi {
  private client: AxiosInstance;
  
  constructor(baseURL: string = '/api/v1') {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    this.setupInterceptors();
  }
  
  private setupInterceptors() {
    // Request interceptor for auth
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
    
    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          localStorage.removeItem('authToken');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }
  
  // Scan operations
  async createScan(scanData: CreateScanRequest): Promise<Scan> {
    const response = await this.client.post('/scans', scanData);
    return response.data;
  }
  
  async getScans(): Promise<Scan[]> {
    const response = await this.client.get('/scans');
    return response.data;
  }
  
  async getScanResults(scanId: string): Promise<ScanResults> {
    const response = await this.client.get(`/scans/${scanId}/results`);
    return response.data;
  }
}

export const api = new LEWISApi();
```

## 🔧 Build and Deployment

### Build Scripts

```json
{
  "name": "lewis",
  "scripts": {
    "dev": "python lewis.py --dev",
    "test": "pytest",
    "test:coverage": "pytest --cov=lewis --cov-report=html",
    "lint": "flake8 lewis/ && black --check lewis/",
    "format": "black lewis/ && isort lewis/",
    "build": "python setup.py sdist bdist_wheel",
    "build:web": "cd web && npm run build",
    "docker:build": "docker build -t lewis:latest .",
    "docker:dev": "docker-compose -f docker-compose.dev.yml up",
    "docs": "cd docs && make html"
  }
}
```

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=lewis --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
  
  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t lewis:${{ github.sha }} .
        docker tag lewis:${{ github.sha }} lewis:latest
    
    - name: Run security scan
      run: |
        docker run --rm -v $(pwd):/app lewis:latest python lewis.py scan /app
```

---

**Next:** [Deployment Guide](12-deployment.md) | **Previous:** [Troubleshooting Guide](10-troubleshooting.md)

---
*This guide is part of the LEWIS documentation. For more information, visit the [main documentation](README.md).*
