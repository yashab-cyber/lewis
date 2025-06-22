# LEWIS Deployment Guide

This directory contains comprehensive deployment configurations and scripts for LEWIS across different environments and platforms.

## Directory Structure

```
deployment/
├── kubernetes/          # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── storage.yaml
│   └── autoscaling.yaml
├── cloud/              # Cloud platform configurations
│   ├── aws/
│   │   └── infrastructure.yaml
│   ├── gcp/
│   │   └── infrastructure.yaml
│   └── azure/
│       └── infrastructure.json
├── scripts/            # Deployment scripts
│   ├── quick_deploy.sh
│   └── production_setup.sh
├── monitoring/         # Monitoring stack
│   ├── prometheus.yml
│   ├── grafana.ini
│   └── docker-compose.yml
├── configs/           # Server configurations
│   ├── nginx.conf
│   └── apache.conf
├── templates/         # Configuration templates
└── README.md         # This file
```

## Deployment Types

### 1. Kubernetes Deployment
- **Production-ready** Kubernetes manifests
- **Auto-scaling** and load balancing
- **Persistent storage** configuration
- **Ingress** for external access
- **Monitoring** integration

### 2. Cloud Platform Deployment
- **AWS CloudFormation** templates
- **Google Cloud Deployment Manager** configs
- **Azure Resource Manager** templates
- **Auto-scaling** and managed services
- **Load balancing** and SSL termination

### 3. Docker Deployment
- **Multi-container** setup with docker-compose
- **Development** and production configurations
- **Monitoring stack** integration
- **Network isolation** and security

### 4. Traditional/Native Deployment
- **System packages** (DEB, RPM, MSI)
- **Systemd services** configuration
- **Web server** reverse proxy setup
- **Database** and cache configuration

## Quick Start Deployments

### 1. Docker Quick Deploy
```bash
# Clone and navigate to LEWIS
git clone https://github.com/ZehraSec/LEWIS.git
cd LEWIS

# Quick deploy with defaults
./deployment/scripts/quick_deploy.sh --type docker

# Deploy with SSL and custom domain
./deployment/scripts/quick_deploy.sh --type docker --domain yourdomain.com --ssl
```

### 2. Kubernetes Deploy
```bash
# Deploy to existing Kubernetes cluster
./deployment/scripts/quick_deploy.sh --type kubernetes

# Check deployment status
kubectl get pods -n lewis
kubectl logs -f deployment/lewis-deployment -n lewis
```

### 3. Production Setup (Linux)
```bash
# Full production setup on Ubuntu/CentOS
sudo ./deployment/scripts/production_setup.sh

# This installs:
# - Python 3.9+, Node.js, Docker
# - PostgreSQL, Redis, Nginx
# - LEWIS application and services
# - Monitoring stack (Prometheus, Grafana)
# - SSL certificates and security hardening
```

## Cloud Platform Deployments

### AWS Deployment
```bash
# Deploy infrastructure with CloudFormation
aws cloudformation create-stack \
  --stack-name lewis-infrastructure \
  --template-body file://deployment/cloud/aws/infrastructure.yaml \
  --capabilities CAPABILITY_IAM

# Deploy application
./deployment/scripts/quick_deploy.sh --type docker --domain $(aws cloudformation describe-stacks --stack-name lewis-infrastructure --query 'Stacks[0].Outputs[?OutputKey==`PublicIP`].OutputValue' --output text)
```

### Google Cloud Platform
```bash
# Deploy infrastructure
gcloud deployment-manager deployments create lewis-infrastructure \
  --config deployment/cloud/gcp/infrastructure.yaml

# Get external IP
gcloud compute instances describe lewis-compute --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

### Microsoft Azure
```bash
# Create resource group
az group create --name lewis-rg --location "East US"

# Deploy infrastructure
az deployment group create \
  --resource-group lewis-rg \
  --template-file deployment/cloud/azure/infrastructure.json

# Get public IP
az vm show -d -g lewis-rg -n lewis-vm --query publicIps -o tsv
```

## Advanced Configurations

### Production Monitoring Stack
```bash
# Deploy monitoring stack
cd deployment/monitoring
docker-compose up -d

# Access monitoring:
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/lewis_admin_password)
# - AlertManager: http://localhost:9093
```

### Web Server Configuration

#### Nginx Setup
```bash
# Copy nginx configuration
sudo cp deployment/configs/nginx.conf /etc/nginx/sites-available/lewis
sudo ln -s /etc/nginx/sites-available/lewis /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

#### Apache Setup
```bash
# Copy apache configuration
sudo cp deployment/configs/apache.conf /etc/apache2/sites-available/lewis.conf
sudo a2ensite lewis
sudo systemctl reload apache2
```

### SSL/TLS Configuration

#### Let's Encrypt (Automated)
```bash
# Automatic SSL setup for production domains
./deployment/scripts/quick_deploy.sh --type docker --domain yourdomain.com --ssl

# Manual certbot setup
sudo certbot --nginx -d yourdomain.com
```

#### Self-Signed Certificates (Development)
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/lewis.key \
  -out /etc/ssl/certs/lewis.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

## Package Installations

### Debian/Ubuntu (.deb)
```bash
# Build and install DEB package
cd packaging/
./build_deb.sh
sudo dpkg -i dist/lewis_1.0.0_all.deb
sudo apt-get install -f  # Install dependencies
```

### RHEL/CentOS/Fedora (.rpm)
```bash
# Build and install RPM package
cd packaging/
./build_rpm.sh
sudo dnf install dist/lewis-1.0.0-1.noarch.rpm
```

### Windows (.msi)
```cmd
# Build MSI package (requires WiX Toolset)
cd packaging\windows
candle lewis.wxs
light lewis.wixobj -o lewis.msi

# Install MSI package
msiexec /i lewis.msi
```

## Security Configurations

### Firewall Setup
```bash
# Ubuntu/Debian (ufw)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# RHEL/CentOS (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### SELinux Configuration (RHEL/CentOS)
```bash
# Set SELinux contexts for LEWIS
sudo setsebool -P httpd_can_network_connect 1
sudo semanage fcontext -a -t httpd_exec_t "/opt/lewis/lewis-server.py"
sudo restorecon -R /opt/lewis/
```

## High Availability Setup

### Load Balancer Configuration
```bash
# HAProxy configuration for multiple LEWIS instances
# Edit /etc/haproxy/haproxy.cfg:
backend lewis_backend
    balance roundrobin
    server lewis1 10.0.1.10:8080 check
    server lewis2 10.0.1.11:8080 check
    server lewis3 10.0.1.12:8080 check
```

### Database Clustering
```bash
# PostgreSQL streaming replication setup
# Master configuration in postgresql.conf:
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64

# Slave configuration:
standby_mode = 'on'
primary_conninfo = 'host=master_ip port=5432 user=replicator'
```

## Monitoring and Logging

### Application Metrics
- **Prometheus** metrics endpoint: `/metrics`
- **Health check** endpoint: `/health`
- **Application logs**: `/var/log/lewis/`
- **System metrics**: Node Exporter, cAdvisor

### Log Aggregation
```bash
# Centralized logging with ELK stack
docker run -d --name elasticsearch elasticsearch:7.14.0
docker run -d --name logstash logstash:7.14.0
docker run -d --name kibana -p 5601:5601 kibana:7.14.0
```

## Backup and Recovery

### Database Backup
```bash
# PostgreSQL backup
sudo -u postgres pg_dump lewis > lewis_backup_$(date +%Y%m%d).sql

# Automated backup script
sudo crontab -e
0 2 * * * /opt/lewis/scripts/backup_database.sh
```

### Application Backup
```bash
# Full application backup
tar -czf lewis_full_backup_$(date +%Y%m%d).tar.gz \
  /opt/lewis/ \
  /etc/lewis/ \
  /var/lib/lewis/ \
  /var/log/lewis/
```

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check service status
sudo systemctl status lewis

# View service logs
sudo journalctl -u lewis -f

# Validate configuration
lewis-config --validate
```

#### Database Connection Issues
```bash
# Test database connectivity
sudo -u lewis psql -h localhost -U lewis -d lewis -c "SELECT version();"

# Reset database
sudo -u lewis lewis-setup --reset-db
```

#### Permission Errors
```bash
# Fix file permissions
sudo chown -R lewis:lewis /opt/lewis /var/lib/lewis /var/log/lewis
sudo chmod 750 /var/lib/lewis /var/log/lewis
sudo chmod 600 /etc/lewis/lewis.conf
```

### Performance Tuning

#### Application Settings
```ini
# /etc/lewis/lewis.conf
[performance]
workers = 4                    # Number of worker processes
worker_connections = 1000      # Connections per worker
cache_ttl = 3600              # Cache timeout in seconds
max_upload_size = 100MB       # Maximum file upload size
```

#### Database Optimization
```sql
-- PostgreSQL performance tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
SELECT pg_reload_conf();
```

## Support and Maintenance

### Health Checks
```bash
# Application health check
curl -f http://localhost:8080/health

# Database health check
sudo -u postgres pg_isready

# Service health check
sudo systemctl is-active lewis
```

### Updates and Upgrades
```bash
# Update LEWIS application
git pull origin main
sudo systemctl restart lewis

# Update packages (DEB)
sudo apt-get update && sudo apt-get upgrade lewis

# Update packages (RPM)
sudo dnf update lewis
```

### Log Rotation
```bash
# Configure log rotation
sudo tee /etc/logrotate.d/lewis << EOF
/var/log/lewis/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 lewis lewis
    postrotate
        systemctl reload lewis
    endscript
}
EOF
```

## Development Deployment

### Development Environment
```bash
# Quick development setup
git clone https://github.com/ZehraSec/LEWIS.git
cd LEWIS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run development server
python app.py --debug
```

### Testing Deployment
```bash
# Run tests
pytest tests/

# Integration tests
pytest tests/integration/

# Performance tests
pytest tests/performance/
```

## Contributing

For deployment-related contributions:
1. Test deployment scripts on clean systems
2. Validate package builds on target platforms
3. Update documentation for new deployment methods
4. Submit pull requests with detailed testing information

## Support

For deployment support:
- **Documentation**: https://docs.lewis-security.com
- **Issues**: https://github.com/ZehraSec/LEWIS/issues
- **Email**: yashabalam707@gmail.com
- **Discord**: https://discord.gg/zehrasec

---

**Author**: Yashab Alam (ZehraSec)  
**Project**: LEWIS - Linux Environment Working Intelligence System  
**Last Updated**: June 22, 2025
```

### Docker Compose (Full Stack)
```bash
docker-compose -f deployment/docker/production.yml up -d
```

### Kubernetes
```bash
kubectl apply -f deployment/kubernetes/
```

## Environment Configuration

Each deployment environment has specific configurations:

### Development
- Debug mode enabled
- Local database
- Hot reloading
- Verbose logging

### Staging  
- Production-like setup
- Test databases
- Performance monitoring
- Integration testing

### Production
- Optimized performance
- High availability
- Security hardened
- Monitoring enabled

## Security Considerations

- Use secrets management for sensitive data
- Enable HTTPS/TLS in production
- Configure proper firewall rules
- Implement access controls
- Regular security updates

## Monitoring

Production deployments include:
- Health check endpoints
- Metrics collection
- Log aggregation
- Alert notifications
- Performance monitoring

## Scaling

LEWIS supports horizontal scaling:
- Load balancer configuration
- Database clustering
- Cache layer setup
- Auto-scaling policies

## Backup and Recovery

- Automated backup schedules
- Disaster recovery procedures
- Data replication
- Point-in-time recovery
