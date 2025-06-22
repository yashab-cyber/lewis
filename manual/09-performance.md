# LEWIS Performance Guide

This guide covers performance optimization, monitoring, and tuning for LEWIS deployments to ensure optimal operation at scale.

## ⚡ Overview

LEWIS is designed for high-performance security operations. This guide provides comprehensive guidance on optimizing performance for various deployment scenarios.

## 📋 Table of Contents

1. [Performance Architecture](#performance-architecture)
2. [System Requirements](#system-requirements)
3. [Performance Optimization](#performance-optimization)
4. [Scaling Strategies](#scaling-strategies)
5. [Monitoring & Metrics](#monitoring--metrics)
6. [Troubleshooting](#troubleshooting)
7. [Benchmarking](#benchmarking)
8. [Best Practices](#best-practices)

## 🏗️ Performance Architecture

### System Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                Load Balancer                    │
├─────────────────────────────────────────────────┤
│  LEWIS Instance 1  │  LEWIS Instance 2  │ ...   │
├─────────────────────────────────────────────────┤
│              Caching Layer                      │
├─────────────────────────────────────────────────┤
│              Message Queue                      │
├─────────────────────────────────────────────────┤
│              Database Cluster                   │
└─────────────────────────────────────────────────┘
```

### Performance Components

1. **Asynchronous Processing**: Background task execution
2. **Caching Layer**: Redis/Memcached for fast data access
3. **Database Optimization**: Indexed queries and connection pooling
4. **Load Balancing**: Distribute traffic across instances
5. **Message Queues**: Decouple heavy processing tasks

## 💻 System Requirements

### Minimum Requirements

| Component | Minimum | Recommended | High-Performance |
|-----------|---------|-------------|------------------|
| CPU       | 2 cores | 4 cores     | 8+ cores        |
| RAM       | 4 GB    | 8 GB        | 16+ GB          |
| Storage   | 50 GB   | 100 GB      | 500+ GB SSD     |
| Network   | 100 Mbps| 1 Gbps      | 10+ Gbps        |

### Performance Sizing Guidelines

```python
# utils/performance_calculator.py
class PerformanceSizer:
    def __init__(self):
        self.base_requirements = {
            'cpu_cores': 2,
            'memory_gb': 4,
            'storage_gb': 50,
            'network_mbps': 100
        }
        
        self.scaling_factors = {
            'scans_per_hour': 0.1,      # CPU scaling
            'concurrent_users': 0.5,     # Memory scaling
            'data_retention_days': 1.0,  # Storage scaling
            'network_intensive': 2.0     # Network scaling
        }
    
    def calculate_requirements(self, workload):
        """Calculate system requirements based on workload"""
        requirements = self.base_requirements.copy()
        
        # Scale CPU based on scan frequency
        cpu_factor = 1 + (workload['scans_per_hour'] * self.scaling_factors['scans_per_hour'])
        requirements['cpu_cores'] = int(self.base_requirements['cpu_cores'] * cpu_factor)
        
        # Scale memory based on concurrent users
        memory_factor = 1 + (workload['concurrent_users'] * self.scaling_factors['concurrent_users'])
        requirements['memory_gb'] = int(self.base_requirements['memory_gb'] * memory_factor)
        
        # Scale storage based on data retention
        storage_factor = 1 + (workload['data_retention_days'] * self.scaling_factors['data_retention_days'])
        requirements['storage_gb'] = int(self.base_requirements['storage_gb'] * storage_factor)
        
        return requirements

# Example usage
sizer = PerformanceSizer()
workload = {
    'scans_per_hour': 100,
    'concurrent_users': 20,
    'data_retention_days': 365,
    'network_intensive': True
}
requirements = sizer.calculate_requirements(workload)
print(f"Recommended specs: {requirements}")
```

## 🚀 Performance Optimization

### Application-Level Optimization

```python
# core/performance_optimizer.py
import asyncio
import concurrent.futures
from functools import lru_cache
import time

class PerformanceOptimizer:
    def __init__(self):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        self.process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=4)
        
    @lru_cache(maxsize=1000)
    def cached_vulnerability_lookup(self, cve_id):
        """Cached vulnerability database lookup"""
        # Expensive database operation
        return self._lookup_vulnerability(cve_id)
    
    async def parallel_scan_execution(self, targets):
        """Execute scans in parallel"""
        semaphore = asyncio.Semaphore(10)  # Limit concurrent scans
        
        async def scan_with_semaphore(target):
            async with semaphore:
                return await self.scan_target(target)
        
        tasks = [scan_with_semaphore(target) for target in targets]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    def cpu_intensive_task(self, data):
        """Offload CPU-intensive tasks to process pool"""
        future = self.process_pool.submit(self._process_data, data)
        return future.result()
    
    def io_intensive_task(self, operation):
        """Offload I/O-intensive tasks to thread pool"""
        future = self.thread_pool.submit(operation)
        return future.result()

class DatabaseOptimizer:
    def __init__(self, db_config):
        self.connection_pool = self.create_connection_pool(db_config)
        
    def create_connection_pool(self, config):
        """Create optimized database connection pool"""
        return {
            'pool_size': 20,
            'max_overflow': 30,
            'pool_timeout': 30,
            'pool_recycle': 3600,
            'pool_pre_ping': True
        }
    
    def optimize_queries(self):
        """Apply database query optimizations"""
        optimizations = [
            "CREATE INDEX IF NOT EXISTS idx_scans_timestamp ON scans(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity)",
            "CREATE INDEX IF NOT EXISTS idx_targets_status ON targets(status)",
            "ANALYZE TABLE scans",
            "ANALYZE TABLE findings",
            "ANALYZE TABLE targets"
        ]
        return optimizations
```

### Caching Implementation

```python
# utils/caching.py
import redis
import pickle
import json
from typing import Any, Optional
import hashlib

class CacheManager:
    def __init__(self, redis_url='redis://localhost:6379'):
        self.redis_client = redis.Redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour
        
    def cache_key(self, prefix: str, *args) -> str:
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{':'.join(map(str, args))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set cache value"""
        try:
            serialized_value = pickle.dumps(value)
            return self.redis_client.setex(
                key, 
                ttl or self.default_ttl, 
                serialized_value
            )
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        try:
            cached_value = self.redis_client.get(key)
            if cached_value:
                return pickle.loads(cached_value)
        except Exception as e:
            print(f"Cache get error: {e}")
        return None
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache keys matching pattern"""
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

# Cache decorators
def cached_result(cache_manager: CacheManager, ttl: int = 3600):
    """Decorator for caching function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = cache_manager.cache_key(
                func.__name__, *args, *kwargs.values()
            )
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
```

### Asynchronous Processing

```python
# core/async_processor.py
import asyncio
import aiohttp
from asyncio import Queue
from typing import List, Callable

class AsyncTaskProcessor:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.workers = []
    
    async def start_workers(self):
        """Start async worker tasks"""
        self.workers = [
            asyncio.create_task(self.worker(f"worker-{i}"))
            for i in range(self.max_workers)
        ]
    
    async def worker(self, name: str):
        """Async worker task"""
        while True:
            try:
                task_func, args, kwargs = await self.task_queue.get()
                
                start_time = time.time()
                result = await task_func(*args, **kwargs)
                duration = time.time() - start_time
                
                await self.result_queue.put({
                    'worker': name,
                    'result': result,
                    'duration': duration,
                    'success': True
                })
                
                self.task_queue.task_done()
                
            except Exception as e:
                await self.result_queue.put({
                    'worker': name,
                    'error': str(e),
                    'success': False
                })
                self.task_queue.task_done()
    
    async def submit_task(self, task_func: Callable, *args, **kwargs):
        """Submit task for async processing"""
        await self.task_queue.put((task_func, args, kwargs))
    
    async def get_results(self, timeout: float = None) -> List:
        """Get processing results"""
        results = []
        deadline = time.time() + (timeout or float('inf'))
        
        while time.time() < deadline:
            try:
                result = await asyncio.wait_for(
                    self.result_queue.get(), 
                    timeout=min(1.0, deadline - time.time())
                )
                results.append(result)
            except asyncio.TimeoutError:
                break
        
        return results

class NetworkOptimizer:
    def __init__(self):
        self.session = None
        self.connector_limit = 100
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def create_session(self):
        """Create optimized aiohttp session"""
        connector = aiohttp.TCPConnector(
            limit=self.connector_limit,
            limit_per_host=20,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=self.timeout
        )
    
    async def batch_http_requests(self, urls: List[str]) -> List:
        """Execute batch HTTP requests efficiently"""
        if not self.session:
            await self.create_session()
        
        semaphore = asyncio.Semaphore(20)  # Limit concurrent requests
        
        async def fetch_with_semaphore(url):
            async with semaphore:
                try:
                    async with self.session.get(url) as response:
                        return {
                            'url': url,
                            'status': response.status,
                            'data': await response.text(),
                            'success': True
                        }
                except Exception as e:
                    return {
                        'url': url,
                        'error': str(e),
                        'success': False
                    }
        
        tasks = [fetch_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        return results
```

## 📈 Scaling Strategies

### Horizontal Scaling

```python
# scaling/horizontal_scaler.py
import kubernetes
from typing import Dict, List

class HorizontalScaler:
    def __init__(self, k8s_config_path=None):
        if k8s_config_path:
            kubernetes.config.load_kube_config(k8s_config_path)
        else:
            kubernetes.config.load_incluster_config()
        
        self.apps_v1 = kubernetes.client.AppsV1Api()
        self.metrics_client = kubernetes.client.CustomObjectsApi()
    
    def scale_deployment(self, deployment_name: str, namespace: str, replicas: int):
        """Scale Kubernetes deployment"""
        body = {'spec': {'replicas': replicas}}
        
        try:
            self.apps_v1.patch_namespaced_deployment_scale(
                name=deployment_name,
                namespace=namespace,
                body=body
            )
            return True
        except Exception as e:
            print(f"Scaling error: {e}")
            return False
    
    def auto_scale_based_on_metrics(self, deployment_config: Dict):
        """Auto-scale based on custom metrics"""
        current_load = self.get_current_load(deployment_config)
        target_load = deployment_config.get('target_load', 70)
        
        current_replicas = self.get_current_replicas(
            deployment_config['name'],
            deployment_config['namespace']
        )
        
        if current_load > target_load:
            # Scale up
            new_replicas = min(
                current_replicas + 1,
                deployment_config.get('max_replicas', 10)
            )
        elif current_load < target_load * 0.5:
            # Scale down
            new_replicas = max(
                current_replicas - 1,
                deployment_config.get('min_replicas', 1)
            )
        else:
            new_replicas = current_replicas
        
        if new_replicas != current_replicas:
            self.scale_deployment(
                deployment_config['name'],
                deployment_config['namespace'],
                new_replicas
            )

class LoadBalancer:
    def __init__(self):
        self.instances = []
        self.health_checks = {}
        
    def add_instance(self, instance_url: str, weight: int = 1):
        """Add instance to load balancer"""
        self.instances.append({
            'url': instance_url,
            'weight': weight,
            'active': True,
            'connections': 0
        })
    
    def get_next_instance(self, algorithm='round_robin'):
        """Get next instance using specified algorithm"""
        healthy_instances = [
            inst for inst in self.instances 
            if inst['active'] and self.is_healthy(inst['url'])
        ]
        
        if not healthy_instances:
            return None
        
        if algorithm == 'round_robin':
            return self.round_robin_selection(healthy_instances)
        elif algorithm == 'least_connections':
            return self.least_connections_selection(healthy_instances)
        elif algorithm == 'weighted':
            return self.weighted_selection(healthy_instances)
        
        return healthy_instances[0]
    
    def round_robin_selection(self, instances: List) -> Dict:
        """Round-robin instance selection"""
        if not hasattr(self, '_rr_index'):
            self._rr_index = 0
        
        instance = instances[self._rr_index % len(instances)]
        self._rr_index += 1
        
        return instance
```

### Vertical Scaling

```python
# scaling/vertical_scaler.py
import psutil
import time
from typing import Dict

class VerticalScaler:
    def __init__(self):
        self.metrics_history = []
        self.scaling_thresholds = {
            'cpu_scale_up': 80,
            'cpu_scale_down': 30,
            'memory_scale_up': 85,
            'memory_scale_down': 40
        }
    
    def get_system_metrics(self) -> Dict:
        """Get current system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters(),
            'timestamp': time.time()
        }
    
    def recommend_scaling(self, current_config: Dict) -> Dict:
        """Recommend vertical scaling based on metrics"""
        metrics = self.get_system_metrics()
        recommendations = {
            'cpu_cores': current_config['cpu_cores'],
            'memory_gb': current_config['memory_gb'],
            'scaling_needed': False,
            'reasons': []
        }
        
        # CPU scaling recommendations
        if metrics['cpu_percent'] > self.scaling_thresholds['cpu_scale_up']:
            recommendations['cpu_cores'] = min(
                current_config['cpu_cores'] * 2,
                32  # Max CPU limit
            )
            recommendations['scaling_needed'] = True
            recommendations['reasons'].append('High CPU usage')
        
        # Memory scaling recommendations
        if metrics['memory_percent'] > self.scaling_thresholds['memory_scale_up']:
            recommendations['memory_gb'] = min(
                current_config['memory_gb'] * 2,
                128  # Max memory limit
            )
            recommendations['scaling_needed'] = True
            recommendations['reasons'].append('High memory usage')
        
        return recommendations
    
    def apply_scaling_recommendations(self, recommendations: Dict):
        """Apply vertical scaling recommendations"""
        if not recommendations['scaling_needed']:
            return False
        
        # Implementation depends on deployment environment
        # Docker, Kubernetes, VM, etc.
        return self.update_resource_limits(recommendations)
```

## 📊 Monitoring & Metrics

### Performance Metrics Collection

```python
# monitoring/metrics_collector.py
import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
import json

class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(deque)
        self.metric_types = {
            'counter': self.update_counter,
            'gauge': self.update_gauge,
            'histogram': self.update_histogram,
            'timer': self.update_timer
        }
        self.lock = threading.Lock()
        
    def record_metric(self, name: str, value: float, metric_type: str = 'gauge', tags: Dict = None):
        """Record a metric value"""
        with self.lock:
            timestamp = time.time()
            metric_data = {
                'timestamp': timestamp,
                'value': value,
                'tags': tags or {},
                'type': metric_type
            }
            
            # Keep only recent metrics (last hour)
            cutoff_time = timestamp - 3600
            while (self.metrics[name] and 
                   self.metrics[name][0]['timestamp'] < cutoff_time):
                self.metrics[name].popleft()
            
            self.metrics[name].append(metric_data)
    
    def get_metric_stats(self, name: str, duration_seconds: int = 300) -> Dict:
        """Get metric statistics for specified duration"""
        with self.lock:
            cutoff_time = time.time() - duration_seconds
            recent_values = [
                m['value'] for m in self.metrics[name]
                if m['timestamp'] >= cutoff_time
            ]
            
            if not recent_values:
                return {'count': 0}
            
            return {
                'count': len(recent_values),
                'min': min(recent_values),
                'max': max(recent_values),
                'avg': sum(recent_values) / len(recent_values),
                'sum': sum(recent_values)
            }

class PerformanceProfiler:
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        
    def profile_function(self, func_name: str):
        """Decorator to profile function performance"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                except Exception as e:
                    result = e
                    success = False
                
                duration = time.time() - start_time
                
                # Record metrics
                self.metrics.record_metric(
                    f"{func_name}.duration",
                    duration,
                    'timer'
                )
                self.metrics.record_metric(
                    f"{func_name}.calls",
                    1,
                    'counter'
                )
                
                if success:
                    self.metrics.record_metric(
                        f"{func_name}.success",
                        1,
                        'counter'
                    )
                else:
                    self.metrics.record_metric(
                        f"{func_name}.errors",
                        1,
                        'counter'
                    )
                
                if not success:
                    raise result
                
                return result
            return wrapper
        return decorator

# Performance monitoring dashboard
class PerformanceDashboard:
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        
    def generate_dashboard_data(self) -> Dict:
        """Generate performance dashboard data"""
        dashboard_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'system_metrics': self.get_system_performance(),
            'application_metrics': self.get_application_performance(),
            'scan_metrics': self.get_scan_performance(),
            'alerts': self.check_performance_alerts()
        }
        
        return dashboard_data
    
    def get_system_performance(self) -> Dict:
        """Get system-level performance metrics"""
        return {
            'cpu_usage': self.metrics.get_metric_stats('system.cpu_percent'),
            'memory_usage': self.metrics.get_metric_stats('system.memory_percent'),
            'disk_io': self.metrics.get_metric_stats('system.disk_io'),
            'network_io': self.metrics.get_metric_stats('system.network_io')
        }
    
    def get_application_performance(self) -> Dict:
        """Get application-level performance metrics"""
        return {
            'request_rate': self.metrics.get_metric_stats('app.requests_per_second'),
            'response_time': self.metrics.get_metric_stats('app.response_time'),
            'error_rate': self.metrics.get_metric_stats('app.error_rate'),
            'active_connections': self.metrics.get_metric_stats('app.active_connections')
        }
    
    def get_scan_performance(self) -> Dict:
        """Get scan-specific performance metrics"""
        return {
            'scans_per_hour': self.metrics.get_metric_stats('scans.per_hour'),
            'avg_scan_duration': self.metrics.get_metric_stats('scans.duration'),
            'scan_success_rate': self.calculate_scan_success_rate(),
            'queue_length': self.metrics.get_metric_stats('scans.queue_length')
        }
```

### Real-time Performance Monitoring

```python
# monitoring/realtime_monitor.py
import asyncio
import websockets
import json
from typing import Set, Dict

class RealTimeMonitor:
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.connected_clients: Set = set()
        self.monitoring_active = False
        
    async def start_monitoring(self, host='localhost', port=8765):
        """Start real-time monitoring WebSocket server"""
        self.monitoring_active = True
        
        async def handle_client(websocket, path):
            self.connected_clients.add(websocket)
            try:
                await websocket.wait_closed()
            finally:
                self.connected_clients.remove(websocket)
        
        # Start WebSocket server
        server = await websockets.serve(handle_client, host, port)
        
        # Start metrics broadcasting
        asyncio.create_task(self.broadcast_metrics())
        
        return server
    
    async def broadcast_metrics(self):
        """Broadcast real-time metrics to connected clients"""
        while self.monitoring_active:
            if self.connected_clients:
                metrics_data = self.collect_realtime_metrics()
                message = json.dumps(metrics_data)
                
                # Send to all connected clients
                disconnected_clients = set()
                for client in self.connected_clients:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        disconnected_clients.add(client)
                
                # Remove disconnected clients
                self.connected_clients -= disconnected_clients
            
            await asyncio.sleep(1)  # Broadcast every second
    
    def collect_realtime_metrics(self) -> Dict:
        """Collect real-time metrics for broadcasting"""
        return {
            'timestamp': time.time(),
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'active_scans': self.metrics.get_metric_stats('scans.active', 60)['count'],
            'requests_per_second': self.calculate_requests_per_second(),
            'error_rate': self.calculate_error_rate()
        }
```

## 🔧 Troubleshooting

### Performance Issue Diagnosis

```python
# troubleshooting/performance_diagnostics.py
import psutil
import tracemalloc
import cProfile
import pstats
from io import StringIO

class PerformanceDiagnostics:
    def __init__(self):
        self.profiler = None
        self.memory_tracer_active = False
        
    def start_memory_profiling(self):
        """Start memory profiling"""
        tracemalloc.start()
        self.memory_tracer_active = True
    
    def get_memory_snapshot(self) -> Dict:
        """Get current memory usage snapshot"""
        if not self.memory_tracer_active:
            self.start_memory_profiling()
            return {"error": "Memory profiling just started, take another snapshot"}
        
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        
        memory_stats = {
            'total_memory_mb': sum(stat.size for stat in top_stats) / 1024 / 1024,
            'top_memory_consumers': []
        }
        
        for stat in top_stats[:10]:
            memory_stats['top_memory_consumers'].append({
                'file': stat.traceback.format()[0],
                'size_mb': stat.size / 1024 / 1024,
                'count': stat.count
            })
        
        return memory_stats
    
    def start_cpu_profiling(self):
        """Start CPU profiling"""
        self.profiler = cProfile.Profile()
        self.profiler.enable()
    
    def stop_cpu_profiling(self) -> str:
        """Stop CPU profiling and return results"""
        if not self.profiler:
            return "CPU profiling not started"
        
        self.profiler.disable()
        
        # Capture profiling results
        output = StringIO()
        stats = pstats.Stats(self.profiler, stream=output)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        
        profiling_results = output.getvalue()
        output.close()
        
        self.profiler = None
        return profiling_results
    
    def diagnose_performance_bottlenecks(self) -> Dict:
        """Comprehensive performance bottleneck diagnosis"""
        diagnosis = {
            'system_resources': self.check_system_resources(),
            'database_performance': self.check_database_performance(),
            'network_performance': self.check_network_performance(),
            'application_performance': self.check_application_performance(),
            'recommendations': []
        }
        
        # Generate recommendations
        diagnosis['recommendations'] = self.generate_recommendations(diagnosis)
        
        return diagnosis
    
    def check_system_resources(self) -> Dict:
        """Check system resource utilization"""
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_usage_percent': cpu_usage,
            'memory_usage_percent': memory.percent,
            'memory_available_gb': memory.available / 1024**3,
            'disk_usage_percent': disk.percent,
            'disk_free_gb': disk.free / 1024**3,
            'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }
    
    def generate_recommendations(self, diagnosis: Dict) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        # CPU recommendations
        if diagnosis['system_resources']['cpu_usage_percent'] > 80:
            recommendations.append("High CPU usage detected. Consider scaling up CPU or optimizing algorithms.")
        
        # Memory recommendations
        if diagnosis['system_resources']['memory_usage_percent'] > 85:
            recommendations.append("High memory usage detected. Consider increasing RAM or implementing memory optimization.")
        
        # Disk recommendations
        if diagnosis['system_resources']['disk_usage_percent'] > 90:
            recommendations.append("Disk space is critically low. Clean up old data or increase storage capacity.")
        
        return recommendations

class PerformanceAlerting:
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.alert_thresholds = {
            'cpu_usage': 85,
            'memory_usage': 90,
            'disk_usage': 95,
            'response_time': 5.0,
            'error_rate': 5.0
        }
        self.alert_history = []
    
    def check_performance_alerts(self) -> List[Dict]:
        """Check for performance alerts"""
        alerts = []
        current_time = time.time()
        
        # Check each threshold
        for metric, threshold in self.alert_thresholds.items():
            current_value = self.get_current_metric_value(metric)
            
            if current_value > threshold:
                alert = {
                    'timestamp': current_time,
                    'metric': metric,
                    'current_value': current_value,
                    'threshold': threshold,
                    'severity': self.calculate_alert_severity(current_value, threshold),
                    'message': f"{metric} is {current_value:.2f}, exceeding threshold of {threshold}"
                }
                alerts.append(alert)
                self.alert_history.append(alert)
        
        return alerts
    
    def calculate_alert_severity(self, current_value: float, threshold: float) -> str:
        """Calculate alert severity"""
        ratio = current_value / threshold
        
        if ratio >= 1.5:
            return 'critical'
        elif ratio >= 1.2:
            return 'high'
        elif ratio >= 1.1:
            return 'medium'
        else:
            return 'low'
```

## 📊 Benchmarking

### Performance Benchmarks

```python
# benchmarking/performance_benchmarks.py
import time
import statistics
from typing import List, Dict, Callable
import concurrent.futures

class PerformanceBenchmark:
    def __init__(self):
        self.benchmark_results = {}
        
    def benchmark_function(self, func: Callable, iterations: int = 100, *args, **kwargs) -> Dict:
        """Benchmark a function's performance"""
        execution_times = []
        errors = 0
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                errors += 1
                success = False
            
            end_time = time.perf_counter()
            execution_times.append(end_time - start_time)
        
        if execution_times:
            return {
                'function_name': func.__name__,
                'iterations': iterations,
                'min_time': min(execution_times),
                'max_time': max(execution_times),
                'avg_time': statistics.mean(execution_times),
                'median_time': statistics.median(execution_times),
                'std_dev': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
                'success_rate': ((iterations - errors) / iterations) * 100,
                'errors': errors
            }
        
        return {'error': 'No successful executions'}
    
    def benchmark_concurrent_execution(self, func: Callable, max_workers: int = 10, tasks: int = 100) -> Dict:
        """Benchmark concurrent function execution"""
        start_time = time.perf_counter()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func) for _ in range(tasks)]
            results = []
            errors = 0
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    errors += 1
        
        total_time = time.perf_counter() - start_time
        
        return {
            'function_name': func.__name__,
            'max_workers': max_workers,
            'total_tasks': tasks,
            'successful_tasks': len(results),
            'failed_tasks': errors,
            'total_time': total_time,
            'tasks_per_second': tasks / total_time,
            'success_rate': (len(results) / tasks) * 100
        }
    
    def load_test_endpoint(self, url: str, concurrent_users: int = 10, duration_seconds: int = 60) -> Dict:
        """Load test a web endpoint"""
        import requests
        
        results = {
            'url': url,
            'concurrent_users': concurrent_users,
            'duration_seconds': duration_seconds,
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'status_codes': {}
        }
        
        end_time = time.time() + duration_seconds
        
        def make_request():
            try:
                start = time.perf_counter()
                response = requests.get(url, timeout=10)
                duration = time.perf_counter() - start
                
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'response_time': duration
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'response_time': None
                }
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            while time.time() < end_time:
                futures = [executor.submit(make_request) for _ in range(concurrent_users)]
                
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    results['total_requests'] += 1
                    
                    if result['success']:
                        results['successful_requests'] += 1
                        results['response_times'].append(result['response_time'])
                        status_code = result['status_code']
                        results['status_codes'][status_code] = results['status_codes'].get(status_code, 0) + 1
                    else:
                        results['failed_requests'] += 1
        
        # Calculate statistics
        if results['response_times']:
            results['avg_response_time'] = statistics.mean(results['response_times'])
            results['min_response_time'] = min(results['response_times'])
            results['max_response_time'] = max(results['response_times'])
            results['p95_response_time'] = self.percentile(results['response_times'], 95)
            results['p99_response_time'] = self.percentile(results['response_times'], 99)
        
        results['requests_per_second'] = results['total_requests'] / duration_seconds
        results['success_rate'] = (results['successful_requests'] / results['total_requests']) * 100
        
        return results
    
    def percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data"""
        size = len(data)
        return sorted(data)[int(percentile / 100 * size)]
```

## 🎯 Best Practices

### Performance Optimization Checklist

```markdown
## Performance Optimization Checklist

### Application Level
- [ ] Enable asynchronous processing for I/O operations
- [ ] Implement connection pooling for databases
- [ ] Use caching for frequently accessed data
- [ ] Optimize database queries with proper indexing
- [ ] Implement pagination for large result sets
- [ ] Use compression for data transfer
- [ ] Minimize memory allocations in loops

### System Level
- [ ] Configure adequate system resources (CPU, RAM, Disk)
- [ ] Enable swap space for memory overflow
- [ ] Use SSD storage for better I/O performance
- [ ] Configure kernel parameters for network performance
- [ ] Enable CPU frequency scaling
- [ ] Configure NUMA topology awareness

### Database Level
- [ ] Create appropriate indexes on frequently queried columns
- [ ] Regular database maintenance (ANALYZE, VACUUM)
- [ ] Configure database connection pooling
- [ ] Optimize database buffer sizes
- [ ] Use read replicas for scaling read operations
- [ ] Implement database partitioning for large tables

### Network Level
- [ ] Use CDN for static content delivery
- [ ] Enable HTTP/2 for web interfaces
- [ ] Implement proper load balancing
- [ ] Configure TCP window scaling
- [ ] Use keep-alive connections
- [ ] Enable compression (gzip, brotli)

### Monitoring Level
- [ ] Set up comprehensive metrics collection
- [ ] Configure performance alerting
- [ ] Implement log aggregation and analysis
- [ ] Regular performance benchmarking
- [ ] Capacity planning based on growth projections
- [ ] Automated scaling policies
```

### Configuration Recommendations

```yaml
# config/performance.yaml
performance:
  # Threading and concurrency
  max_workers: 16
  max_concurrent_scans: 10
  thread_pool_size: 20
  
  # Caching configuration
  cache:
    enabled: true
    backend: "redis"
    default_ttl: 3600
    max_memory: "512MB"
  
  # Database optimization
  database:
    pool_size: 20
    max_overflow: 30
    pool_timeout: 30
    pool_recycle: 3600
    echo_sql: false
  
  # Network optimization
  network:
    connection_timeout: 30
    read_timeout: 60
    keep_alive: true
    max_connections: 100
  
  # Memory management
  memory:
    max_heap_size: "2GB"
    gc_threshold: 0.8
    cleanup_interval: 300
  
  # Monitoring
  monitoring:
    metrics_interval: 10
    health_check_interval: 30
    performance_logging: true
```

---

**Next:** [Troubleshooting Guide](10-troubleshooting.md) | **Previous:** [Security Guide](08-security.md)

---
*This guide is part of the LEWIS documentation. For more information, visit the [main documentation](README.md).*
