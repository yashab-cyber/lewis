# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set metadata
LABEL maintainer="Yashab Alam <yashabalam707@gmail.com>"
LABEL version="1.0.0"
LABEL description="LEWIS - Linux Environment Working Intelligence System"
LABEL org.opencontainers.image.source="https://github.com/yashab-cyber/lewis"
LABEL org.opencontainers.image.description="AI-Powered Cybersecurity Intelligence Platform"
LABEL org.opencontainers.image.licenses="MIT"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    LEWIS_HOME=/opt/lewis \
    LEWIS_CONFIG=/etc/lewis \
    LEWIS_DATA=/var/lib/lewis \
    LEWIS_LOGS=/var/log/lewis

# Create non-root user
RUN groupadd -r lewis && useradd -r -g lewis -d $LEWIS_HOME -s /bin/bash lewis

# Set working directory
WORKDIR $LEWIS_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Network tools
    nmap \
    masscan \
    nikto \
    dirb \
    dnsutils \
    whois \
    curl \
    wget \
    # Build tools
    build-essential \
    python3-dev \
    # SSL/TLS tools
    openssl \
    ca-certificates \
    # Database clients
    postgresql-client \
    # Additional utilities
    git \
    vim \
    jq \
    htop \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir flask flask-socketio

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Copy examples directory with proper permissions
COPY examples/ ./examples/
RUN chown -R lewis:lewis ./examples/

# Install LEWIS
RUN pip install -e .

# Create directories
RUN mkdir -p $LEWIS_CONFIG $LEWIS_DATA $LEWIS_LOGS \
    logs data outputs temp models reports \
    && chown -R lewis:lewis $LEWIS_HOME $LEWIS_CONFIG $LEWIS_DATA $LEWIS_LOGS

# Create necessary directories for extensions
RUN mkdir -p $LEWIS_DATA/extensions \
    && mkdir -p $LEWIS_LOGS/extensions \
    && mkdir -p $LEWIS_CONFIG/extensions \
    && chown -R lewis:lewis $LEWIS_DATA $LEWIS_LOGS $LEWIS_CONFIG

# Create default configuration
RUN mkdir -p $LEWIS_CONFIG \
    && cp config/config.yaml $LEWIS_CONFIG/config.yaml \
    && chown -R lewis:lewis $LEWIS_CONFIG

# Set proper permissions
RUN chown -R lewis:lewis $LEWIS_HOME \
    && chmod +x install.sh uninstall.sh start_lewis.sh start_lewis.ps1

# Switch to non-root user
USER lewis

# Create volume mount points
VOLUME ["$LEWIS_CONFIG", "$LEWIS_DATA", "$LEWIS_LOGS"]

# Expose ports
EXPOSE 8000 8443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command
ENTRYPOINT ["python", "lewis.py"]
CMD ["--mode", "server", "--host", "0.0.0.0", "--port", "8000"]

# Add labels for better container management
LABEL org.opencontainers.image.title="LEWIS"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.created="2025-06-21"
LABEL org.opencontainers.image.authors="Yashab Alam <yashabalam707@gmail.com>"
LABEL org.opencontainers.image.vendor="ZehraSec"
LABEL org.opencontainers.image.url="https://www.zehrasec.com"
LABEL org.opencontainers.image.documentation="https://docs.lewis-security.com"
