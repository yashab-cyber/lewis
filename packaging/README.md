# LEWIS Package Distribution

This directory contains all the necessary files and scripts to create distribution packages for LEWIS across different platforms and package managers.

## Supported Package Formats

### 1. Debian/Ubuntu (.deb)
- **Location**: `debian/`
- **Build Script**: `build_deb.sh`
- **Supported Architectures**: all, amd64, arm64
- **Dependencies**: dpkg-dev, debhelper, fakeroot

### 2. RHEL/CentOS/Fedora (.rpm)
- **Location**: `rpm/`
- **Build Script**: `build_rpm.sh`
- **Supported Architectures**: noarch, x86_64, aarch64
- **Dependencies**: rpmbuild, rpm-build

### 3. Windows (.msi)
- **Location**: `windows/`
- **Build Tool**: WiX Toolset
- **Supported Architectures**: x64, x86
- **Dependencies**: WiX Toolset, .NET Framework

## Building Packages

### Prerequisites

#### For DEB packages (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install dpkg-dev debhelper fakeroot lintian
```

#### For RPM packages (RHEL/CentOS/Fedora):
```bash
# RHEL/CentOS
sudo yum install rpm-build rpm-devel rpmlint

# Fedora
sudo dnf install rpm-build rpm-devel rpmlint
```

#### For MSI packages (Windows):
- Install WiX Toolset 3.11+
- Install Visual Studio 2019+ or Build Tools
- Install .NET Framework 4.7.2+

### Build Commands

#### Build DEB package:
```bash
cd packaging/
chmod +x build_deb.sh
./build_deb.sh

# With custom version
./build_deb.sh --version 1.0.1

# With custom architecture
./build_deb.sh --architecture amd64
```

#### Build RPM package:
```bash
cd packaging/
chmod +x build_rpm.sh
./build_rpm.sh

# With custom version and release
./build_rpm.sh --version 1.0.1 --release 2
```

#### Build MSI package (Windows):
```cmd
cd packaging\windows
candle lewis.wxs
light lewis.wixobj -o lewis.msi
```

## Package Contents

All packages include:

### Core Components
- LEWIS application files (`/opt/lewis/` or `C:\Program Files\ZehraSec\LEWIS\`)
- Configuration files (`/etc/lewis/` or `%ProgramData%\LEWIS\`)
- Systemd service files (Linux) or Windows Service
- Command-line tools and utilities

### Documentation
- User manual and guides
- API reference documentation
- Configuration examples
- Changelog and release notes

### Dependencies
- Python 3.8+ runtime
- Required Python packages
- Database drivers (PostgreSQL, Redis)
- Web server configuration (Nginx/Apache)

## Installation

### DEB Package Installation:
```bash
# Install package
sudo dpkg -i lewis_1.0.0_all.deb

# Install dependencies if missing
sudo apt-get install -f

# Enable and start service
sudo systemctl enable lewis
sudo systemctl start lewis
```

### RPM Package Installation:
```bash
# Install package (Fedora/CentOS 8+)
sudo dnf install lewis-1.0.0-1.noarch.rpm

# Install package (RHEL/CentOS 7)
sudo yum install lewis-1.0.0-1.noarch.rpm

# Enable and start service
sudo systemctl enable lewis
sudo systemctl start lewis
```

### MSI Package Installation (Windows):
```cmd
# Silent installation
msiexec /i lewis.msi /quiet

# Interactive installation
lewis.msi

# Install with custom parameters
msiexec /i lewis.msi INSTALLFOLDER="C:\CustomPath\LEWIS"
```

## Package Verification

### DEB Package:
```bash
# Verify package integrity
dpkg-deb --info lewis_1.0.0_all.deb
dpkg-deb --contents lewis_1.0.0_all.deb

# Lint package
lintian lewis_1.0.0_all.deb
```

### RPM Package:
```bash
# Verify package integrity
rpm -qip lewis-1.0.0-1.noarch.rpm
rpm -qlp lewis-1.0.0-1.noarch.rpm

# Verify signature (if signed)
rpm --checksig lewis-1.0.0-1.noarch.rpm
```

### MSI Package:
```cmd
# Verify package
msiexec /i lewis.msi /l*v install.log
```

## Package Configuration

### Post-Installation Configuration

#### Linux (DEB/RPM):
1. Edit configuration: `sudo nano /etc/lewis/lewis.conf`
2. Configure database: `sudo -u lewis lewis-setup --init-db`
3. Restart service: `sudo systemctl restart lewis`
4. Access web interface: `http://localhost:8080`

#### Windows (MSI):
1. Edit configuration: `C:\ProgramData\LEWIS\config\lewis.conf`
2. Configure database: `lewis-setup.exe --init-db`
3. Restart service: `net start LEWIS`
4. Access web interface: `http://localhost:8080`

## Uninstallation

### DEB Package:
```bash
# Remove package (keep configuration)
sudo apt-get remove lewis

# Remove package and configuration
sudo apt-get purge lewis
```

### RPM Package:
```bash
# Remove package
sudo dnf remove lewis

# or
sudo yum remove lewis
```

### MSI Package (Windows):
```cmd
# Uninstall via Control Panel
appwiz.cpl

# Or via command line
msiexec /x lewis.msi
```

## Troubleshooting

### Common Issues

#### Permission Errors:
```bash
# Fix permissions
sudo chown -R lewis:lewis /var/lib/lewis /var/log/lewis
sudo chmod 750 /var/lib/lewis /var/log/lewis
```

#### Service Start Failures:
```bash
# Check service status
sudo systemctl status lewis

# View service logs
sudo journalctl -u lewis -f

# Check configuration
lewis-config --validate
```

#### Database Connection Issues:
```bash
# Test database connection
lewis-cli --test-db

# Reset database
sudo -u lewis lewis-setup --reset-db
```

## Package Metadata

### Maintainer Information
- **Maintainer**: Yashab Alam (ZehraSec)
- **Email**: yashabalam707@gmail.com
- **Homepage**: https://github.com/ZehraSec/LEWIS
- **Bug Reports**: https://github.com/ZehraSec/LEWIS/issues

### Package Versioning
- Version format: `MAJOR.MINOR.PATCH`
- Release format: `VERSION-RELEASE` (RPM only)
- Pre-release suffix: `-alpha`, `-beta`, `-rc1` etc.

### License
- **License**: MIT License
- **License File**: `/usr/share/doc/lewis/LICENSE`

## Building Custom Packages

### Customizing Package Contents
1. Modify control/spec files in respective directories
2. Update build scripts with custom dependencies
3. Add custom pre/post installation scripts
4. Rebuild packages with custom configurations

### Adding Platform Support
1. Create new platform directory under `packaging/`
2. Implement build script following existing patterns
3. Add platform-specific configuration files
4. Update main documentation

## Repository Distribution

### Creating APT Repository:
```bash
# Create repository structure
mkdir -p repo/deb/pool/main
cp dist/*.deb repo/deb/pool/main/

# Generate package index
cd repo/deb
dpkg-scanpackages pool/main | gzip > dists/stable/main/binary-amd64/Packages.gz
```

### Creating YUM Repository:
```bash
# Create repository structure
mkdir -p repo/rpm
cp dist/*.rpm repo/rpm/

# Generate repository metadata
createrepo repo/rpm/
```

## Continuous Integration

The package building process is automated through GitHub Actions:
- **Workflow**: `.github/workflows/ci-cd.yml`
- **Triggers**: Release creation, manual dispatch
- **Artifacts**: Packages uploaded to GitHub Releases
- **Distribution**: Automatic repository updates

For manual package building in CI/CD environments, use the provided build scripts with appropriate environment variables and credentials.

## Support

For package-related issues:
1. Check the troubleshooting section above
2. Review installation logs
3. Submit bug reports with package version and system details
4. Contact maintainer: yashabalam707@gmail.com

---

**Note**: This packaging system is designed for production deployment of LEWIS. For development installations, consider using the Docker containers or direct source installation methods described in the main project documentation.
