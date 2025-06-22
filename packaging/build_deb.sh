#!/bin/bash
# LEWIS DEB Package Build Script
# Author: Yashab Alam (ZehraSec)
# Project: LEWIS - Linux Environment Working Intelligence System

set -euo pipefail

# Configuration
PACKAGE_NAME="lewis"
VERSION="1.0.0"
MAINTAINER="Yashab Alam <yashabalam707@gmail.com>"
ARCHITECTURE="all"
BUILD_DIR="build"
DIST_DIR="dist"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1" >&2; exit 1; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites for DEB package build..."
    
    command -v dpkg-deb >/dev/null 2>&1 || error "dpkg-deb is required but not installed"
    command -v fakeroot >/dev/null 2>&1 || error "fakeroot is required but not installed"
    command -v lintian >/dev/null 2>&1 || warning "lintian is recommended for package validation"
    
    success "Prerequisites check passed"
}

# Clean previous builds
clean_build() {
    log "Cleaning previous build artifacts..."
    
    rm -rf $BUILD_DIR
    mkdir -p $BUILD_DIR $DIST_DIR
    
    success "Build directory cleaned"
}

# Prepare package structure
prepare_package() {
    log "Preparing package structure..."
    
    # Create directory structure
    mkdir -p $BUILD_DIR/DEBIAN
    mkdir -p $BUILD_DIR/opt/lewis
    mkdir -p $BUILD_DIR/etc/lewis
    mkdir -p $BUILD_DIR/var/log/lewis
    mkdir -p $BUILD_DIR/var/lib/lewis
    mkdir -p $BUILD_DIR/usr/share/doc/lewis
    mkdir -p $BUILD_DIR/lib/systemd/system
    mkdir -p $BUILD_DIR/etc/nginx/sites-available
    mkdir -p $BUILD_DIR/usr/bin
    
    # Copy application files
    cp -r . $BUILD_DIR/opt/lewis/
    
    # Remove unnecessary files
    rm -rf $BUILD_DIR/opt/lewis/.git
    rm -rf $BUILD_DIR/opt/lewis/build
    rm -rf $BUILD_DIR/opt/lewis/dist
    rm -rf $BUILD_DIR/opt/lewis/__pycache__
    find $BUILD_DIR/opt/lewis -name "*.pyc" -delete
    find $BUILD_DIR/opt/lewis -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Copy configuration files
    cp config/lewis.conf.example $BUILD_DIR/etc/lewis/lewis.conf
    cp templates/lewis.service.template $BUILD_DIR/lib/systemd/system/lewis.service
    cp deployment/configs/nginx.conf $BUILD_DIR/etc/nginx/sites-available/lewis
    
    # Copy documentation
    cp README.md $BUILD_DIR/usr/share/doc/lewis/
    cp CHANGELOG.md $BUILD_DIR/usr/share/doc/lewis/
    cp LICENSE $BUILD_DIR/usr/share/doc/lewis/
    
    # Create executable symlinks
    ln -sf /opt/lewis/lewis-cli.py $BUILD_DIR/usr/bin/lewis
    ln -sf /opt/lewis/lewis-server.py $BUILD_DIR/usr/bin/lewis-server
    
    success "Package structure prepared"
}

# Generate control file
generate_control() {
    log "Generating control file..."
    
    cat > $BUILD_DIR/DEBIAN/control << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: net
Priority: optional
Architecture: $ARCHITECTURE
Maintainer: $MAINTAINER
Depends: python3 (>= 3.8), python3-flask, python3-sqlalchemy, python3-redis, python3-celery, python3-requests, python3-cryptography, python3-jwt, python3-werkzeug, python3-jinja2, python3-click, python3-marshmallow, python3-psycopg2, python3-gunicorn, redis-server, postgresql-client
Recommends: postgresql-server, nginx
Suggests: docker.io, docker-compose
Homepage: https://github.com/ZehraSec/LEWIS
Description: Linux Environment Working Intelligence System
 LEWIS is an advanced cybersecurity platform that provides comprehensive
 web intelligence and security analysis capabilities. It includes features
 for threat detection, vulnerability assessment, security monitoring,
 and automated response systems.
 .
 Key features include:
  * Real-time threat detection and analysis
  * Comprehensive vulnerability scanning
  * Advanced security monitoring dashboard
  * Automated incident response capabilities
  * Machine learning-powered threat intelligence
  * Extensible plugin architecture
  * RESTful API for integration
  * Multi-tenant architecture support
EOF

    success "Control file generated"
}

# Generate postinst script
generate_postinst() {
    log "Generating postinst script..."
    
    cat > $BUILD_DIR/DEBIAN/postinst << 'EOF'
#!/bin/bash
# LEWIS post-installation script

set -e

# Create lewis user if it doesn't exist
if ! getent passwd lewis >/dev/null; then
    useradd -r -m -d /var/lib/lewis -s /bin/bash lewis
fi

# Set proper permissions
chown -R lewis:lewis /var/log/lewis
chown -R lewis:lewis /var/lib/lewis
chown -R lewis:lewis /opt/lewis
chmod 750 /var/log/lewis
chmod 750 /var/lib/lewis
chmod 600 /etc/lewis/lewis.conf

# Enable and start systemd service
if command -v systemctl >/dev/null 2>&1; then
    systemctl daemon-reload
    systemctl enable lewis
    systemctl start lewis
fi

# Configure nginx (if installed)
if command -v nginx >/dev/null 2>&1; then
    if [ ! -L /etc/nginx/sites-enabled/lewis ]; then
        ln -sf /etc/nginx/sites-available/lewis /etc/nginx/sites-enabled/lewis
    fi
    
    # Test nginx configuration
    if nginx -t 2>/dev/null; then
        systemctl reload nginx 2>/dev/null || true
    fi
fi

echo "LEWIS installation completed successfully!"
echo "You can access LEWIS at http://localhost:8080"
echo "For configuration help, see /usr/share/doc/lewis/README.md"

exit 0
EOF

    chmod 755 $BUILD_DIR/DEBIAN/postinst
    success "Postinst script generated"
}

# Generate prerm script
generate_prerm() {
    log "Generating prerm script..."
    
    cat > $BUILD_DIR/DEBIAN/prerm << 'EOF'
#!/bin/bash
# LEWIS pre-removal script

set -e

# Stop and disable service
if command -v systemctl >/dev/null 2>&1; then
    if systemctl is-active lewis >/dev/null 2>&1; then
        systemctl stop lewis
    fi
    systemctl disable lewis 2>/dev/null || true
fi

# Remove nginx configuration
if [ -L /etc/nginx/sites-enabled/lewis ]; then
    rm -f /etc/nginx/sites-enabled/lewis
    if command -v nginx >/dev/null 2>&1 && nginx -t 2>/dev/null; then
        systemctl reload nginx 2>/dev/null || true
    fi
fi

exit 0
EOF

    chmod 755 $BUILD_DIR/DEBIAN/prerm
    success "Prerm script generated"
}

# Generate postrm script
generate_postrm() {
    log "Generating postrm script..."
    
    cat > $BUILD_DIR/DEBIAN/postrm << 'EOF'
#!/bin/bash
# LEWIS post-removal script

set -e

case "$1" in
    purge)
        # Remove user and data directories
        if getent passwd lewis >/dev/null; then
            userdel lewis 2>/dev/null || true
        fi
        
        # Remove data directories
        rm -rf /var/log/lewis
        rm -rf /var/lib/lewis
        rm -rf /etc/lewis
        
        echo "LEWIS has been completely removed from the system."
        ;;
    remove|upgrade|failed-upgrade|abort-install|abort-upgrade|disappear)
        # Keep user and data for potential reinstallation
        ;;
    *)
        echo "postrm called with unknown argument \`$1'" >&2
        exit 1
        ;;
esac

exit 0
EOF

    chmod 755 $BUILD_DIR/DEBIAN/postrm
    success "Postrm script generated"
}

# Set file permissions
set_permissions() {
    log "Setting file permissions..."
    
    # Set executable permissions
    find $BUILD_DIR/opt/lewis -name "*.py" -exec chmod 755 {} \;
    find $BUILD_DIR/opt/lewis -name "*.sh" -exec chmod 755 {} \;
    
    # Set configuration file permissions
    chmod 600 $BUILD_DIR/etc/lewis/lewis.conf
    chmod 644 $BUILD_DIR/lib/systemd/system/lewis.service
    chmod 644 $BUILD_DIR/etc/nginx/sites-available/lewis
    
    # Set directory permissions
    chmod 755 $BUILD_DIR/opt/lewis
    chmod 750 $BUILD_DIR/var/log/lewis
    chmod 750 $BUILD_DIR/var/lib/lewis
    
    success "File permissions set"
}

# Build package
build_package() {
    log "Building DEB package..."
    
    # Calculate installed size
    INSTALLED_SIZE=$(du -sk $BUILD_DIR | cut -f1)
    echo "Installed-Size: $INSTALLED_SIZE" >> $BUILD_DIR/DEBIAN/control
    
    # Build the package
    fakeroot dpkg-deb --build $BUILD_DIR $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb
    
    success "DEB package built: $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
}

# Validate package
validate_package() {
    if command -v lintian >/dev/null 2>&1; then
        log "Validating package with lintian..."
        
        if lintian $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb; then
            success "Package validation passed"
        else
            warning "Package validation completed with warnings"
        fi
    else
        warning "Lintian not available, skipping validation"
    fi
}

# Show package information
show_package_info() {
    log "Package information:"
    
    dpkg-deb --info $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb
    
    echo
    log "Package contents:"
    dpkg-deb --contents $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb | head -20
    
    if [ $(dpkg-deb --contents $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb | wc -l) -gt 20 ]; then
        echo "... (truncated, $(dpkg-deb --contents $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb | wc -l) files total)"
    fi
}

# Main function
main() {
    log "Starting LEWIS DEB package build..."
    
    check_prerequisites
    clean_build
    prepare_package
    generate_control
    generate_postinst
    generate_prerm
    generate_postrm
    set_permissions
    build_package
    validate_package
    show_package_info
    
    success "DEB package build completed successfully!"
    log "Package location: $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
    log "To install: sudo dpkg -i $DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCHITECTURE}.deb"
    log "To install dependencies: sudo apt-get install -f"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -a|--architecture)
            ARCHITECTURE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Build DEB package for LEWIS"
            echo ""
            echo "Options:"
            echo "  -v, --version VERSION      Package version (default: $VERSION)"
            echo "  -a, --architecture ARCH    Package architecture (default: $ARCHITECTURE)"
            echo "  -h, --help                 Show this help message"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            ;;
    esac
done

# Run main function
main
