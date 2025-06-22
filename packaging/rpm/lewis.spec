# LEWIS RPM Spec File
# Author: Yashab Alam (ZehraSec)
# Project: LEWIS - Linux Environment Working Intelligence System

Name:           lewis
Version:        1.0.0
Release:        1%{?dist}
Summary:        Linux Environment Working Intelligence System

License:        MIT
URL:            https://github.com/ZehraSec/LEWIS
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
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

%package server
Summary:        LEWIS server components
Requires:       %{name} = %{version}-%{release}

%description server
This package provides the server components for LEWIS including
the web server, API endpoints, and background processing services.

%package client
Summary:        LEWIS client tools and libraries
Requires:       python3-requests

%description client
Command-line tools and Python libraries for interacting with LEWIS
servers. Includes CLI utilities for managing LEWIS deployments and
Python SDK for building custom integrations.

%package devel
Summary:        LEWIS development tools
Requires:       %{name} = %{version}-%{release}
Requires:       python3-pytest
Requires:       python3-coverage
Requires:       python3-flake8
Requires:       python3-black
Requires:       python3-isort

%description devel
Development tools and dependencies for LEWIS development including
testing frameworks, code quality tools, and development utilities.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

# Install configuration files
install -d %{buildroot}%{_sysconfdir}/lewis
install -m 644 config/lewis.conf.example %{buildroot}%{_sysconfdir}/lewis/lewis.conf

# Install systemd service file
install -d %{buildroot}%{_unitdir}
install -m 644 templates/lewis.service.template %{buildroot}%{_unitdir}/lewis.service

# Create directories
install -d %{buildroot}%{_localstatedir}/log/lewis
install -d %{buildroot}%{_localstatedir}/lib/lewis
install -d %{buildroot}%{_datadir}/lewis

# Install static files
cp -r static %{buildroot}%{_datadir}/lewis/

# Install documentation
install -d %{buildroot}%{_docdir}/%{name}
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 CHANGELOG.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_docdir}/%{name}/

# Install nginx configuration
install -d %{buildroot}%{_sysconfdir}/nginx/conf.d
install -m 644 deployment/configs/nginx.conf %{buildroot}%{_sysconfdir}/nginx/conf.d/lewis.conf

%pre
# Create lewis user and group
getent group lewis >/dev/null || groupadd -r lewis
getent passwd lewis >/dev/null || \
    useradd -r -g lewis -d %{_localstatedir}/lib/lewis -s /sbin/nologin \
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
%{python3_sitelib}/*
%config(noreplace) %{_sysconfdir}/lewis/lewis.conf
%{_unitdir}/lewis.service
%dir %attr(750,lewis,lewis) %{_localstatedir}/log/lewis
%dir %attr(750,lewis,lewis) %{_localstatedir}/lib/lewis
%{_datadir}/lewis/
%config(noreplace) %{_sysconfdir}/nginx/conf.d/lewis.conf

%files server
# Server-specific files would go here

%files client
# Client-specific files would go here

%files devel
# Development files would go here

%changelog
* Sun Jun 22 2025 Yashab Alam <yashabalam707@gmail.com> - 1.0.0-1
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

* Fri May 01 2025 Yashab Alam <yashabalam707@gmail.com> - 0.9.0-1
- Beta release with core functionality
- Web interface implementation
- API server development
- Basic threat detection engine
- Security monitoring capabilities
- Database integration
- Authentication and authorization
- Initial plugin architecture

* Mon Mar 01 2025 Yashab Alam <yashabalam707@gmail.com> - 0.5.0-1
- Alpha release for testing
- Core platform architecture
- Basic web interface
- Initial API implementation
- Database schema design
- Authentication system
- Basic security features
