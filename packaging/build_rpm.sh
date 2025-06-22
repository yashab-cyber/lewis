#!/bin/bash
# LEWIS RPM Package Build Script
# Author: Yashab Alam (ZehraSec)
# Project: LEWIS - Linux Environment Working Intelligence System

set -euo pipefail

# Configuration
PACKAGE_NAME="lewis"
VERSION="1.0.0"
RELEASE="1"
MAINTAINER="Yashab Alam <yashabalam707@gmail.com>"
ARCHITECTURE="noarch"
BUILD_DIR="rpmbuild"
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
    log "Checking prerequisites for RPM package build..."
    
    command -v rpmbuild >/dev/null 2>&1 || error "rpmbuild is required but not installed"
    command -v tar >/dev/null 2>&1 || error "tar is required but not installed"
    command -v gzip >/dev/null 2>&1 || error "gzip is required but not installed"
    
    success "Prerequisites check passed"
}

# Clean previous builds
clean_build() {
    log "Cleaning previous build artifacts..."
    
    rm -rf $BUILD_DIR
    mkdir -p $BUILD_DIR/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    mkdir -p $DIST_DIR
    
    success "Build directory cleaned"
}

# Create source tarball
create_source_tarball() {
    log "Creating source tarball..."
    
    TARBALL_NAME="${PACKAGE_NAME}-${VERSION}.tar.gz"
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    SOURCE_DIR="$TEMP_DIR/${PACKAGE_NAME}-${VERSION}"
    
    # Copy source files
    mkdir -p $SOURCE_DIR
    cp -r . $SOURCE_DIR/
    
    # Remove unnecessary files
    rm -rf $SOURCE_DIR/.git
    rm -rf $SOURCE_DIR/build
    rm -rf $SOURCE_DIR/dist
    rm -rf $SOURCE_DIR/rpmbuild
    rm -rf $SOURCE_DIR/__pycache__
    find $SOURCE_DIR -name "*.pyc" -delete
    find $SOURCE_DIR -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Create tarball
    cd $TEMP_DIR
    tar -czf $TARBALL_NAME ${PACKAGE_NAME}-${VERSION}/
    mv $TARBALL_NAME $(pwd)/$BUILD_DIR/SOURCES/
    
    # Cleanup
    rm -rf $TEMP_DIR
    
    success "Source tarball created: $BUILD_DIR/SOURCES/$TARBALL_NAME"
}

# Generate spec file
generate_spec_file() {
    log "Generating RPM spec file..."
    
    cat > $BUILD_DIR/SPECS/${PACKAGE_NAME}.spec << EOF
# LEWIS RPM Spec File
# Author: Yashab Alam (ZehraSec)
# Project: LEWIS - Linux Environment Working Intelligence System

Name:           ${PACKAGE_NAME}
Version:        ${VERSION}
Release:        ${RELEASE}%{?dist}
Summary:        Linux Environment Working Intelligence System

License:        MIT
URL:            https://github.com/ZehraSec/LEWIS
Source0:        %{name}-%{version}.tar.gz

BuildArch:      ${ARCHITECTURE}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  systemd-rpm-macros

Requires:       python3 >= 3.8
Requires:       python3-flask
Requires:       python3-sqlalchemy
Requires:       python3-redis
Requires:       python3-celery
Requires:       python3-requests
Requires:       python3-cryptography
Requires:       python3-PyJWT
Requires:       python3-werkzeug
Requires:       python3-jinja2
Requires:       python3-click
Requires:       python3-marshmallow
Requires:       python3-psycopg2
Requires:       python3-gunicorn
Requires:       redis
Requires:       postgresql

Recommends:     nginx
Recommends:     docker
Recommends:     docker-compose

%{?systemd_requires}

%description
LEWIS is an advanced cybersecurity platform that provides comprehensive
web intelligence and security analysis capabilities. It includes features
for threat detection, vulnerability assessment, security monitoring,
and automated response systems.

Key features include:
* Real-time threat detection and analysis
* Comprehensive vulnerability scanning
* Advanced security monitoring dashboard
* Automated incident response capabilities
* Machine learning-powered threat intelligence
* Extensible plugin architecture
* RESTful API for integration
* Multi-tenant architecture support

%prep
%autosetup

%build
# No build phase needed for Python application

%install
# Create directories
install -d %{buildroot}%{_datadir}/lewis
install -d %{buildroot}%{_sysconfdir}/lewis
install -d %{buildroot}%{_localstatedir}/log/lewis
install -d %{buildroot}%{_localstatedir}/lib/lewis
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_bindir}

# Install application files
cp -r . %{buildroot}%{_datadir}/lewis/

# Install configuration file
install -m 644 config/lewis.conf.example %{buildroot}%{_sysconfdir}/lewis/lewis.conf

# Install systemd service file
install -m 644 templates/lewis.service.template %{buildroot}%{_unitdir}/lewis.service

# Install executables
install -m 755 lewis-cli.py %{buildroot}%{_bindir}/lewis
install -m 755 lewis-server.py %{buildroot}%{_bindir}/lewis-server

# Install nginx configuration
install -d %{buildroot}%{_sysconfdir}/nginx/conf.d
install -m 644 deployment/configs/nginx.conf %{buildroot}%{_sysconfdir}/nginx/conf.d/lewis.conf

%pre
# Create lewis user and group
getent group lewis >/dev/null || groupadd -r lewis
getent passwd lewis >/dev/null || \\
    useradd -r -g lewis -d %{_localstatedir}/lib/lewis -s /sbin/nologin \\
    -c "LEWIS service account" lewis

%post
%systemd_post lewis.service

# Set permissions
chown -R lewis:lewis %{_localstatedir}/log/lewis
chown -R lewis:lewis %{_localstatedir}/lib/lewis
chmod 750 %{_localstatedir}/log/lewis
chmod 750 %{_localstatedir}/lib/lewis
chmod 600 %{_sysconfdir}/lewis/lewis.conf

%preun
%systemd_preun lewis.service

%postun
%systemd_postun_with_restart lewis.service

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_datadir}/lewis/
%config(noreplace) %{_sysconfdir}/lewis/lewis.conf
%{_unitdir}/lewis.service
%{_bindir}/lewis
%{_bindir}/lewis-server
%dir %attr(750,lewis,lewis) %{_localstatedir}/log/lewis
%dir %attr(750,lewis,lewis) %{_localstatedir}/lib/lewis
%config(noreplace) %{_sysconfdir}/nginx/conf.d/lewis.conf

%changelog
* Sun Jun 22 2025 Yashab Alam <yashabalam707@gmail.com> - ${VERSION}-${RELEASE}
- Initial release of LEWIS platform
- Complete cybersecurity analysis platform
- Real-time threat detection capabilities
- Advanced vulnerability scanning engine
- Comprehensive security monitoring dashboard
- Machine learning-powered threat intelligence
- RESTful API for system integration
- Multi-tenant architecture support
- Extensible plugin system
- Automated incident response features
- Docker containerization support
- Kubernetes deployment manifests
- Cloud deployment templates (AWS, GCP, Azure)
- Production-ready monitoring stack
- Comprehensive documentation suite
- Developer tools and SDK
EOF

    success "RPM spec file generated"
}

# Build RPM package
build_rpm() {
    log "Building RPM package..."
    
    # Build the package
    rpmbuild --define "_topdir $(pwd)/$BUILD_DIR" -ba $BUILD_DIR/SPECS/${PACKAGE_NAME}.spec
    
    # Copy built packages to dist directory
    cp $BUILD_DIR/RPMS/$ARCHITECTURE/${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.rpm $DIST_DIR/
    cp $BUILD_DIR/SRPMS/${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.src.rpm $DIST_DIR/
    
    success "RPM packages built successfully"
}

# Validate package
validate_package() {
    log "Validating RPM package..."
    
    RPM_FILE="$DIST_DIR/${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.rpm"
    
    if command -v rpm >/dev/null 2>&1; then
        # Check package info
        rpm -qip $RPM_FILE
        
        # Check package contents
        echo
        log "Package contents:"
        rpm -qlp $RPM_FILE | head -20
        
        if [ $(rpm -qlp $RPM_FILE | wc -l) -gt 20 ]; then
            echo "... (truncated, $(rpm -qlp $RPM_FILE | wc -l) files total)"
        fi
        
        # Check dependencies
        echo
        log "Package dependencies:"
        rpm -qRp $RPM_FILE
        
        success "Package validation completed"
    else
        warning "rpm command not available, skipping detailed validation"
    fi
}

# Show package information
show_package_info() {
    log "Built packages:"
    ls -la $DIST_DIR/*.rpm
    
    echo
    log "Installation instructions:"
    echo "To install on RHEL/CentOS/Fedora:"
    echo "  sudo dnf install $DIST_DIR/${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.rpm"
    echo "or"
    echo "  sudo yum install $DIST_DIR/${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.rpm"
    echo "or"
    echo "  sudo rpm -ivh $DIST_DIR/${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.rpm"
}

# Main function
main() {
    log "Starting LEWIS RPM package build..."
    
    check_prerequisites
    clean_build
    create_source_tarball
    generate_spec_file
    build_rpm
    validate_package
    show_package_info
    
    success "RPM package build completed successfully!"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -r|--release)
            RELEASE="$2"
            shift 2
            ;;
        -a|--architecture)
            ARCHITECTURE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Build RPM package for LEWIS"
            echo ""
            echo "Options:"
            echo "  -v, --version VERSION      Package version (default: $VERSION)"
            echo "  -r, --release RELEASE      Package release (default: $RELEASE)"
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
