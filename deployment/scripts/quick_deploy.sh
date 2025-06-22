#!/bin/bash
# LEWIS Quick Deployment Script
# Author: Yashab Alam (ZehraSec)
# Project: LEWIS - Linux Environment Working Intelligence System

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
LEWIS_VERSION="${LEWIS_VERSION:-latest}"
DEPLOYMENT_TYPE="${DEPLOYMENT_TYPE:-docker}"
DOMAIN="${DOMAIN:-localhost}"
SSL_ENABLED="${SSL_ENABLED:-false}"
DB_TYPE="${DB_TYPE:-sqlite}"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    case $DEPLOYMENT_TYPE in
        "docker")
            command -v docker >/dev/null 2>&1 || error "Docker is required but not installed"
            command -v docker-compose >/dev/null 2>&1 || error "Docker Compose is required but not installed"
            ;;
        "kubernetes")
            command -v kubectl >/dev/null 2>&1 || error "kubectl is required but not installed"
            command -v helm >/dev/null 2>&1 || warning "Helm is recommended for Kubernetes deployment"
            ;;
        "native")
            command -v python3 >/dev/null 2>&1 || error "Python 3 is required but not installed"
            command -v pip3 >/dev/null 2>&1 || error "pip3 is required but not installed"
            ;;
        *)
            error "Unknown deployment type: $DEPLOYMENT_TYPE"
            ;;
    esac
    
    success "Prerequisites check passed"
}

# Generate configuration
generate_config() {
    log "Generating configuration..."
    
    mkdir -p ./config
    
    cat > ./config/lewis.env << EOF
# LEWIS Configuration
LEWIS_VERSION=$LEWIS_VERSION
LEWIS_DOMAIN=$DOMAIN
LEWIS_SSL_ENABLED=$SSL_ENABLED
LEWIS_DB_TYPE=$DB_TYPE
LEWIS_SECRET_KEY=$(openssl rand -hex 32)
LEWIS_JWT_SECRET=$(openssl rand -hex 32)

# Database Configuration
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-lewis}
DB_USER=${DB_USER:-lewis}
DB_PASSWORD=${DB_PASSWORD:-$(openssl rand -hex 16)}

# Security Settings
CORS_ORIGINS=${CORS_ORIGINS:-*}
MAX_UPLOAD_SIZE=${MAX_UPLOAD_SIZE:-100MB}
RATE_LIMIT=${RATE_LIMIT:-1000/hour}

# Performance Settings
WORKERS=${WORKERS:-4}
WORKER_CONNECTIONS=${WORKER_CONNECTIONS:-1000}
CACHE_TTL=${CACHE_TTL:-3600}

# Monitoring
PROMETHEUS_ENABLED=${PROMETHEUS_ENABLED:-true}
GRAFANA_ENABLED=${GRAFANA_ENABLED:-true}
LOG_LEVEL=${LOG_LEVEL:-INFO}
EOF

    success "Configuration generated"
}

# Docker deployment
deploy_docker() {
    log "Deploying LEWIS with Docker..."
    
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  lewis:
    image: lewis/platform:$LEWIS_VERSION
    ports:
      - "8080:8080"
      - "443:443"
    environment:
      - LEWIS_CONFIG=/app/config/lewis.conf
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    depends_on:
      - database
      - redis

  database:
    image: postgres:13
    environment:
      - POSTGRES_DB=lewis
      - POSTGRES_USER=lewis
      - POSTGRES_PASSWORD=\${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - lewis
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
EOF

    docker-compose up -d
    success "Docker deployment completed"
}

# Kubernetes deployment
deploy_kubernetes() {
    log "Deploying LEWIS to Kubernetes..."
    
    kubectl apply -f ../kubernetes/namespace.yaml
    kubectl apply -f ../kubernetes/configmap.yaml
    kubectl apply -f ../kubernetes/storage.yaml
    kubectl apply -f ../kubernetes/deployment.yaml
    kubectl apply -f ../kubernetes/service.yaml
    kubectl apply -f ../kubernetes/ingress.yaml
    kubectl apply -f ../kubernetes/autoscaling.yaml
    
    log "Waiting for deployment to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/lewis-deployment -n lewis
    
    success "Kubernetes deployment completed"
}

# Native deployment
deploy_native() {
    log "Deploying LEWIS natively..."
    
    # Create user and directories
    sudo useradd -r -s /bin/false lewis || true
    sudo mkdir -p /opt/lewis /var/log/lewis /var/lib/lewis
    sudo chown lewis:lewis /var/log/lewis /var/lib/lewis
    
    # Install Python dependencies
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    
    # Copy files
    sudo cp -r . /opt/lewis/
    sudo chown -R lewis:lewis /opt/lewis
    
    # Create systemd service
    sudo cp ../templates/lewis.service.template /etc/systemd/system/lewis.service
    sudo systemctl daemon-reload
    sudo systemctl enable lewis
    sudo systemctl start lewis
    
    success "Native deployment completed"
}

# SSL setup
setup_ssl() {
    if [ "$SSL_ENABLED" = "true" ]; then
        log "Setting up SSL certificates..."
        
        mkdir -p ./ssl
        
        if [ "$DOMAIN" != "localhost" ]; then
            # Use Let's Encrypt for real domains
            docker run --rm \
                -v $(pwd)/ssl:/etc/letsencrypt \
                -p 80:80 \
                certbot/certbot certonly \
                --standalone \
                --agree-tos \
                --email admin@$DOMAIN \
                -d $DOMAIN
        else
            # Generate self-signed certificate for localhost
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout ./ssl/privkey.pem \
                -out ./ssl/fullchain.pem \
                -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
        fi
        
        success "SSL certificates configured"
    fi
}

# Generate nginx configuration
setup_nginx() {
    log "Setting up Nginx configuration..."
    
    cat > nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream lewis_backend {
        server lewis:8080;
    }

    server {
        listen 80;
        server_name $DOMAIN;
        
        location / {
            return 301 https://\$server_name\$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name $DOMAIN;
        
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        
        location / {
            proxy_pass http://lewis_backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

    success "Nginx configuration created"
}

# Main deployment function
main() {
    log "Starting LEWIS deployment..."
    log "Deployment type: $DEPLOYMENT_TYPE"
    log "Version: $LEWIS_VERSION"
    log "Domain: $DOMAIN"
    
    check_prerequisites
    generate_config
    setup_ssl
    
    case $DEPLOYMENT_TYPE in
        "docker")
            setup_nginx
            deploy_docker
            ;;
        "kubernetes")
            deploy_kubernetes
            ;;
        "native")
            deploy_native
            ;;
    esac
    
    log "Deployment completed successfully!"
    log "LEWIS is available at: http${SSL_ENABLED:+s}://$DOMAIN"
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        log "To view logs: docker-compose logs -f"
        log "To stop: docker-compose down"
    elif [ "$DEPLOYMENT_TYPE" = "kubernetes" ]; then
        log "To view logs: kubectl logs -f deployment/lewis-deployment -n lewis"
        log "To check status: kubectl get pods -n lewis"
    elif [ "$DEPLOYMENT_TYPE" = "native" ]; then
        log "To view logs: sudo journalctl -u lewis -f"
        log "To restart: sudo systemctl restart lewis"
    fi
}

# Help function
show_help() {
    cat << EOF
LEWIS Quick Deployment Script

Usage: $0 [OPTIONS]

Options:
    -t, --type TYPE         Deployment type (docker, kubernetes, native)
    -v, --version VERSION   LEWIS version to deploy (default: latest)
    -d, --domain DOMAIN     Domain name (default: localhost)
    -s, --ssl               Enable SSL/TLS
    --db-type TYPE          Database type (sqlite, postgres, mysql)
    -h, --help              Show this help message

Environment Variables:
    DEPLOYMENT_TYPE         Same as --type
    LEWIS_VERSION          Same as --version
    DOMAIN                 Same as --domain
    SSL_ENABLED            Enable SSL (true/false)
    DB_TYPE                Database type

Examples:
    $0 --type docker --domain example.com --ssl
    $0 --type kubernetes --version v1.0.0
    DEPLOYMENT_TYPE=native $0
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            DEPLOYMENT_TYPE="$2"
            shift 2
            ;;
        -v|--version)
            LEWIS_VERSION="$2"
            shift 2
            ;;
        -d|--domain)
            DOMAIN="$2"
            shift 2
            ;;
        -s|--ssl)
            SSL_ENABLED="true"
            shift
            ;;
        --db-type)
            DB_TYPE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            ;;
    esac
done

# Run main function
main
