# LEWIS Deployment Guide

Comprehensive guide for deploying LEWIS in various environments, from development to enterprise production.

## 🚀 Overview

This guide covers deployment strategies, configuration, and best practices for LEWIS across different environments and platforms.

## 📋 Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Environment Types](#environment-types)
3. [Container Deployment](#container-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud Deployments](#cloud-deployments)
6. [High Availability Setup](#high-availability-setup)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Backup & Recovery](#backup--recovery)

## 🏗️ Deployment Overview

### Architecture Components

```
┌─────────────────────────────────────────────────┐
│              Load Balancer                      │
├─────────────────────────────────────────────────┤
│  LEWIS Web UI  │  LEWIS API  │  LEWIS Worker   │
├─────────────────────────────────────────────────┤
│    Redis Cache    │     Message Queue          │
├─────────────────────────────────────────────────┤
│              PostgreSQL Database               │
└─────────────────────────────────────────────────┘
```

### Deployment Options

| Environment | Complexity | Scalability | Maintenance | Best For |
|-------------|------------|-------------|-------------|----------|
| Single Node | Low | Limited | Easy | Development, Small Teams |
| Docker Compose | Medium | Moderate | Medium | Small Production |
| Kubernetes | High | High | Complex | Enterprise, Large Scale |
| Cloud Managed | Medium | Very High | Low | Enterprise, Multi-region |

## 🌍 Environment Types

### Development Environment

**Quick Setup:**
```bash
# Clone and setup
git clone https://github.com/yashab-cyber/lewis.git
cd lewis

# Install dependencies
pip install -r requirements-dev.txt

# Setup development database
python lewis.py db init --dev

# Start development server
python lewis.py --dev --reload
```

**Development Configuration:**
```yaml
# config/config-dev.yaml
system:
  environment: "development"
  debug: true
  log_level: "DEBUG"

database:
  url: "sqlite:///lewis_dev.db"
  echo: true

cache:
  backend: "memory"

security:
  secret_key: "dev-secret-key-change-in-production"
  ssl_required: false
  csrf_protection: false

interfaces:
  web:
    host: "0.0.0.0"
    port: 8080
    hot_reload: true
  api:
    cors_enabled: true
    cors_origins: ["http://localhost:3000"]
```

### Staging Environment

**Docker Compose Setup:**
```yaml
# docker-compose.staging.yml
version: '3.8'

services:
  lewis-web:
    image: lewis:staging
    ports:
      - "8080:8080"
    environment:
      - LEWIS_ENV=staging
      - LEWIS_CONFIG=/app/config/config-staging.yaml
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: lewis_staging
      POSTGRES_USER: lewis
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups

  redis:
    image: redis:6-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/staging.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - lewis-web

volumes:
  postgres_data:
  redis_data:
```

**Staging Configuration:**
```yaml
# config/config-staging.yaml
system:
  environment: "staging"
  debug: false
  log_level: "INFO"

database:
  url: "postgresql://lewis:${POSTGRES_PASSWORD}@postgres:5432/lewis_staging"
  pool_size: 5
  max_overflow: 10

cache:
  backend: "redis"
  url: "redis://redis:6379/0"

security:
  secret_key: "${SECRET_KEY}"
  ssl_required: true
  session_timeout: 3600

monitoring:
  metrics_enabled: true
  health_checks: true
```

### Production Environment

**Production Configuration:**
```yaml
# config/config-production.yaml
system:
  environment: "production"
  debug: false
  log_level: "WARNING"

database:
  url: "postgresql://lewis:${POSTGRES_PASSWORD}@db-cluster:5432/lewis_prod"
  pool_size: 20
  max_overflow: 30
  pool_timeout: 30
  pool_recycle: 3600

cache:
  backend: "redis"
  url: "redis://redis-cluster:6379/0"
  sentinel_enabled: true
  sentinels:
    - "redis-sentinel-1:26379"
    - "redis-sentinel-2:26379"
    - "redis-sentinel-3:26379"

security:
  secret_key: "${SECRET_KEY}"
  ssl_required: true
  ssl_cert: "/etc/ssl/certs/lewis.crt"
  ssl_key: "/etc/ssl/private/lewis.key"
  session_timeout: 1800
  password_policy:
    min_length: 12
    require_uppercase: true
    require_lowercase: true
    require_digits: true
    require_symbols: true

performance:
  max_workers: 16
  worker_timeout: 300
  max_concurrent_scans: 50

monitoring:
  metrics_enabled: true
  prometheus_enabled: true
  health_checks: true
  audit_logging: true
```

## 🐳 Container Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash lewis

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R lewis:lewis /app

# Switch to non-root user
USER lewis

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Start application
CMD ["python", "lewis.py", "--production"]
```

### Multi-Stage Dockerfile

```dockerfile
# Dockerfile.production
# Build stage
FROM node:16-alpine as web-builder

WORKDIR /app/web
COPY web/package*.json ./
RUN npm ci --only=production

COPY web/ .
RUN npm run build

# Python dependencies stage
FROM python:3.9-slim as python-deps

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim as production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd --create-home --shell /bin/bash lewis

# Copy Python dependencies
COPY --from=python-deps /root/.local /home/lewis/.local
ENV PATH=/home/lewis/.local/bin:$PATH

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=lewis:lewis . .

# Copy built web assets
COPY --from=web-builder --chown=lewis:lewis /app/web/dist ./web/dist

# Switch to non-root user
USER lewis

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080
CMD ["python", "lewis.py", "--production"]
```

### Docker Compose Production

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  lewis-web:
    image: lewis:latest
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        max_attempts: 3
    environment:
      - LEWIS_ENV=production
      - LEWIS_CONFIG=/app/config/config-production.yaml
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
      - SECRET_KEY_FILE=/run/secrets/secret_key
    volumes:
      - ./config:/app/config:ro
      - ./logs:/app/logs
    secrets:
      - postgres_password
      - secret_key
    depends_on:
      - postgres
      - redis
    networks:
      - lewis-network

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: lewis_prod
      POSTGRES_USER: lewis
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    secrets:
      - postgres_password
    networks:
      - lewis-network

  redis:
    image: redis:6-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - lewis-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/production.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - lewis-web
    networks:
      - lewis-network

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - lewis-network

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
  secret_key:
    file: ./secrets/secret_key.txt

volumes:
  postgres_data:
  redis_data:
  prometheus_data:

networks:
  lewis-network:
    driver: bridge
```

## ☸️ Kubernetes Deployment

### Namespace and ConfigMap

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: lewis-prod
  labels:
    name: lewis-prod

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: lewis-config
  namespace: lewis-prod
data:
  config.yaml: |
    system:
      environment: "production"
      debug: false
      log_level: "INFO"
    
    database:
      url: "postgresql://lewis:$(POSTGRES_PASSWORD)@postgres-service:5432/lewis_prod"
      pool_size: 20
      max_overflow: 30
    
    cache:
      backend: "redis"
      url: "redis://redis-service:6379/0"
    
    security:
      secret_key: "$(SECRET_KEY)"
      ssl_required: true
    
    performance:
      max_workers: 16
      max_concurrent_scans: 50
```

### Secrets

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: lewis-secrets
  namespace: lewis-prod
type: Opaque
data:
  postgres-password: <base64-encoded-password>
  secret-key: <base64-encoded-secret-key>
  redis-password: <base64-encoded-redis-password>
```

### Database Deployment

```yaml
# k8s/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: lewis-prod
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: "lewis_prod"
        - name: POSTGRES_USER
          value: "lewis"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: lewis-secrets
              key: postgres-password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        - name: backup-storage
          mountPath: /backups
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: lewis-prod
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

### Redis Deployment

```yaml
# k8s/redis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: lewis-prod
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:6-alpine
        command: ["redis-server"]
        args: ["--appendonly", "yes", "--requirepass", "$(REDIS_PASSWORD)"]
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: lewis-secrets
              key: redis-password
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-storage
          mountPath: /data
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: lewis-prod
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: lewis-prod
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### LEWIS Application Deployment

```yaml
# k8s/lewis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lewis-web
  namespace: lewis-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lewis-web
  template:
    metadata:
      labels:
        app: lewis-web
    spec:
      containers:
      - name: lewis
        image: lewis:latest
        ports:
        - containerPort: 8080
        env:
        - name: LEWIS_ENV
          value: "production"
        - name: LEWIS_CONFIG
          value: "/app/config/config.yaml"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: lewis-secrets
              key: postgres-password
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: lewis-secrets
              key: secret-key
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: logs-volume
          mountPath: /app/logs
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: config-volume
        configMap:
          name: lewis-config
      - name: logs-volume
        persistentVolumeClaim:
          claimName: lewis-logs-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: lewis-service
  namespace: lewis-prod
spec:
  selector:
    app: lewis-web
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: lewis-logs-pvc
  namespace: lewis-prod
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### Ingress Configuration

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: lewis-ingress
  namespace: lewis-prod
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - lewis.company.com
    secretName: lewis-tls
  rules:
  - host: lewis.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: lewis-service
            port:
              number: 80
```

### Horizontal Pod Autoscaler

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: lewis-hpa
  namespace: lewis-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: lewis-web
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## ☁️ Cloud Deployments

### AWS Deployment

**ECS Task Definition:**
```json
{
  "family": "lewis-prod",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/lewisTaskRole",
  "containerDefinitions": [
    {
      "name": "lewis-web",
      "image": "ACCOUNT.dkr.ecr.REGION.amazonaws.com/lewis:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LEWIS_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "POSTGRES_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT:secret:lewis/postgres-password"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT:secret:lewis/secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/lewis-prod",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

**Terraform Configuration:**
```hcl
# terraform/aws/main.tf
provider "aws" {
  region = var.aws_region
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "lewis-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = true
}

# RDS Database
resource "aws_db_instance" "lewis_db" {
  identifier = "lewis-prod-db"
  
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.medium"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_encrypted     = true
  
  db_name  = "lewis_prod"
  username = "lewis"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.lewis.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Sun:04:00-Sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "lewis-prod-db-final-snapshot"
  
  tags = {
    Name = "lewis-prod-db"
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "lewis" {
  name       = "lewis-cache-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_elasticache_replication_group" "lewis" {
  replication_group_id      = "lewis-redis"
  description               = "Redis cluster for LEWIS"
  
  node_type                 = "cache.t3.micro"
  port                      = 6379
  parameter_group_name      = "default.redis6.x"
  
  num_cache_clusters        = 2
  automatic_failover_enabled = true
  
  subnet_group_name = aws_elasticache_subnet_group.lewis.name
  security_group_ids = [aws_security_group.redis.id]
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.redis_auth_token
}

# ECS Cluster
resource "aws_ecs_cluster" "lewis" {
  name = "lewis-prod"
  
  capacity_providers = ["FARGATE"]
  
  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight           = 1
  }
}

# Application Load Balancer
resource "aws_lb" "lewis" {
  name               = "lewis-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = module.vpc.public_subnets
  
  enable_deletion_protection = true
}
```

### Azure Deployment

**ARM Template:**
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "appName": {
      "type": "string",
      "defaultValue": "lewis-prod",
      "metadata": {
        "description": "Name of the application"
      }
    }
  },
  "resources": [
    {
      "type": "Microsoft.ContainerInstance/containerGroups",
      "apiVersion": "2021-03-01",
      "name": "[parameters('appName')]",
      "location": "[resourceGroup().location]",
      "properties": {
        "containers": [
          {
            "name": "lewis-web",
            "properties": {
              "image": "lewis:latest",
              "ports": [
                {
                  "port": 8080,
                  "protocol": "TCP"
                }
              ],
              "environmentVariables": [
                {
                  "name": "LEWIS_ENV",
                  "value": "production"
                }
              ],
              "resources": {
                "requests": {
                  "cpu": 1,
                  "memoryInGB": 2
                }
              }
            }
          }
        ],
        "osType": "Linux",
        "ipAddress": {
          "type": "Public",
          "ports": [
            {
              "port": 8080,
              "protocol": "TCP"
            }
          ]
        }
      }
    }
  ]
}
```

### Google Cloud Deployment

**Cloud Run Service:**
```yaml
# gcp/cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: lewis-prod
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 10
      containers:
      - image: gcr.io/PROJECT_ID/lewis:latest
        ports:
        - containerPort: 8080
        env:
        - name: LEWIS_ENV
          value: "production"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: lewis-secrets
              key: postgres-password
        resources:
          limits:
            cpu: "2"
            memory: "2Gi"
        livenessProbe:
          httpGet:
            path: /health
          initialDelaySeconds: 30
```

## 🔄 High Availability Setup

### Load Balancer Configuration

**NGINX Load Balancer:**
```nginx
# nginx/production.conf
upstream lewis_backend {
    least_conn;
    server lewis-web-1:8080 max_fails=3 fail_timeout=30s;
    server lewis-web-2:8080 max_fails=3 fail_timeout=30s;
    server lewis-web-3:8080 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name lewis.company.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name lewis.company.com;
    
    ssl_certificate /etc/nginx/ssl/lewis.crt;
    ssl_certificate_key /etc/nginx/ssl/lewis.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    location / {
        proxy_pass http://lewis_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Health check
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /health {
        access_log off;
        proxy_pass http://lewis_backend;
    }
}
```

### Database High Availability

**PostgreSQL Master-Slave Configuration:**
```yaml
# docker-compose.ha.yml
services:
  postgres-master:
    image: postgres:13
    environment:
      POSTGRES_DB: lewis_prod
      POSTGRES_USER: lewis
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_REPLICATION_USER: replicator
      POSTGRES_REPLICATION_PASSWORD: ${REPLICATION_PASSWORD}
    volumes:
      - postgres_master_data:/var/lib/postgresql/data
      - ./postgres/master.conf:/etc/postgresql/postgresql.conf
      - ./postgres/pg_hba.conf:/etc/postgresql/pg_hba.conf
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    
  postgres-slave:
    image: postgres:13
    environment:
      POSTGRES_MASTER_SERVICE: postgres-master
      POSTGRES_REPLICATION_USER: replicator
      POSTGRES_REPLICATION_PASSWORD: ${REPLICATION_PASSWORD}
    volumes:
      - postgres_slave_data:/var/lib/postgresql/data
      - ./postgres/recovery.conf:/var/lib/postgresql/recovery.conf
    depends_on:
      - postgres-master
```

### Redis Sentinel Setup

```yaml
# redis-sentinel.yml
services:
  redis-master:
    image: redis:6-alpine
    command: redis-server --appendonly yes --masterauth ${REDIS_PASSWORD} --requirepass ${REDIS_PASSWORD}
    
  redis-slave-1:
    image: redis:6-alpine
    command: redis-server --slaveof redis-master 6379 --masterauth ${REDIS_PASSWORD} --requirepass ${REDIS_PASSWORD}
    
  redis-slave-2:
    image: redis:6-alpine
    command: redis-server --slaveof redis-master 6379 --masterauth ${REDIS_PASSWORD} --requirepass ${REDIS_PASSWORD}
    
  redis-sentinel-1:
    image: redis:6-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    volumes:
      - ./redis/sentinel.conf:/etc/redis/sentinel.conf
      
  redis-sentinel-2:
    image: redis:6-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    volumes:
      - ./redis/sentinel.conf:/etc/redis/sentinel.conf
      
  redis-sentinel-3:
    image: redis:6-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    volumes:
      - ./redis/sentinel.conf:/etc/redis/sentinel.conf
```

## 📊 Monitoring & Maintenance

### Prometheus Configuration

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "lewis_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'lewis'
    static_configs:
      - targets: ['lewis-web:8080']
    metrics_path: /metrics
    scrape_interval: 10s
    
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
      
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
      
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']
```

### Alerting Rules

```yaml
# monitoring/lewis_rules.yml
groups:
- name: lewis.rules
  rules:
  - alert: LewisHighCPUUsage
    expr: rate(cpu_usage_total[5m]) > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "LEWIS CPU usage is high"
      description: "CPU usage has been above 80% for more than 5 minutes"
      
  - alert: LewisHighMemoryUsage
    expr: memory_usage_bytes / memory_total_bytes > 0.9
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "LEWIS memory usage is critical"
      description: "Memory usage has been above 90% for more than 5 minutes"
      
  - alert: LewisServiceDown
    expr: up{job="lewis"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "LEWIS service is down"
      description: "LEWIS service has been down for more than 1 minute"
```

### Maintenance Scripts

```bash
#!/bin/bash
# scripts/maintenance.sh

# LEWIS Maintenance Script

set -e

BACKUP_DIR="/backups"
LOG_DIR="/var/log/lewis"
RETENTION_DAYS=30

echo "Starting LEWIS maintenance..."

# Database backup
echo "Creating database backup..."
pg_dump lewis_prod > "${BACKUP_DIR}/lewis_$(date +%Y%m%d_%H%M%S).sql"

# Log rotation
echo "Rotating logs..."
find "${LOG_DIR}" -name "*.log" -mtime +${RETENTION_DAYS} -delete

# Clean old scan results
echo "Cleaning old scan results..."
python -c "
from lewis.utils.database import DatabaseManager
db = DatabaseManager()
db.cleanup_old_scans(days=${RETENTION_DAYS})
"

# Update vulnerability database
echo "Updating vulnerability database..."
python lewis.py update-vuln-db

# Health check
echo "Performing health check..."
python lewis.py health-check

echo "Maintenance completed successfully."
```

## 💾 Backup & Recovery

### Backup Strategy

```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Database backup
echo "Backing up database..."
pg_dump -h postgres -U lewis lewis_prod | gzip > "${BACKUP_DIR}/db_backup_${DATE}.sql.gz"

# Configuration backup
echo "Backing up configuration..."
tar -czf "${BACKUP_DIR}/config_backup_${DATE}.tar.gz" /app/config/

# Application data backup
echo "Backing up application data..."
tar -czf "${BACKUP_DIR}/data_backup_${DATE}.tar.gz" /app/data/

# Upload to cloud storage (AWS S3 example)
echo "Uploading to cloud storage..."
aws s3 cp "${BACKUP_DIR}/" s3://lewis-backups/$(date +%Y/%m/%d)/ --recursive

# Clean old backups
echo "Cleaning old backups..."
find "${BACKUP_DIR}" -name "*.gz" -mtime +${RETENTION_DAYS} -delete

echo "Backup completed successfully."
```

### Recovery Procedures

```bash
#!/bin/bash
# scripts/restore.sh

BACKUP_FILE=$1
RESTORE_DATE=$2

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file> [restore_date]"
    exit 1
fi

echo "Starting restoration from ${BACKUP_FILE}..."

# Stop LEWIS services
echo "Stopping LEWIS services..."
docker-compose down

# Restore database
echo "Restoring database..."
gunzip -c "${BACKUP_FILE}" | psql -h postgres -U lewis lewis_prod

# Restore configuration
if [ -n "$RESTORE_DATE" ]; then
    echo "Restoring configuration from ${RESTORE_DATE}..."
    tar -xzf "config_backup_${RESTORE_DATE}.tar.gz" -C /
fi

# Start services
echo "Starting LEWIS services..."
docker-compose up -d

# Verify restoration
echo "Verifying restoration..."
sleep 30
curl -f http://localhost:8080/health

echo "Restoration completed successfully."
```

### Disaster Recovery Plan

```markdown
# LEWIS Disaster Recovery Plan

## Recovery Time Objectives (RTO)
- Critical: 4 hours
- High: 8 hours  
- Medium: 24 hours
- Low: 72 hours

## Recovery Point Objectives (RPO)
- Database: 1 hour
- Configuration: 24 hours
- Scan Results: 4 hours

## Recovery Procedures

### 1. Infrastructure Failure
1. Assess damage and identify failed components
2. Provision new infrastructure using Terraform/ARM templates
3. Restore from latest backups
4. Update DNS records if necessary
5. Verify system functionality

### 2. Database Corruption
1. Stop all LEWIS services
2. Restore database from latest backup
3. Apply transaction logs if available
4. Restart services and verify integrity

### 3. Complete Site Failure
1. Activate DR site
2. Restore all components from backups
3. Update DNS to point to DR site
4. Verify all services are operational
5. Communicate with stakeholders
```

---

**Next:** [Debugging Guide](13-debugging.md) | **Previous:** [Development Guide](11-development.md)

---
*This guide is part of the LEWIS documentation. For more information, visit the [main documentation](README.md).*
