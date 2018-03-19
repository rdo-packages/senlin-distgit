%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global service senlin
%global common_desc \
Senlin is a clustering service for OpenStack cloud. \
It creates and operates clusters of homogenous objects exposed by other \
OpenStack services. \
The goal is to make orchestration of collections of similar objects easier.

Name:           openstack-%{service}
Version:        XXX
Release:        XXX
Summary:        OpenStack Senlin Service
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:        %{service}.logrotate
Source2:        openstack-%{service}-api.service
Source3:        openstack-%{service}-engine.service
Source4:        %{service}-dist.conf

BuildArch:      noarch

BuildRequires:  openstack-macros
BuildRequires:  python-pep8
BuildRequires:  python2-oslo-db
BuildRequires:  python2-docker
BuildRequires:  python2-eventlet
BuildRequires:  python-jsonpath-rw
BuildRequires:  python2-jsonschema
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-keystonemiddleware
BuildRequires:  python2-microversion-parse
BuildRequires:  python2-openstacksdk
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-context
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-messaging
BuildRequires:  python2-oslo-middleware
BuildRequires:  python2-oslo-policy
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-oslo-service
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-oslo-versionedobjects
BuildRequires:  python2-osprofiler
BuildRequires:  python-paste-deploy
BuildRequires:  python-qpid
BuildRequires:  python2-requests
BuildRequires:  python2-routes
BuildRequires:  python2-six
BuildRequires:  python2-sqlalchemy
BuildRequires:  python-migrate
BuildRequires:  python2-stevedore
BuildRequires:  python-webob
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git

# Required to compile translation files
BuildRequires:  python2-babel

Requires:       openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils

%{?systemd_requires}
BuildRequires:  systemd

%description
%{common_desc}


%package -n python-%{service}
Summary:        Senlin Python libraries

Requires:       python2-oslo-db >= 4.27.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-babel >= 2.3.4
Requires:       python2-docker >= 2.0.0
Requires:       python2-eventlet >= 0.18.2
Requires:       python-jsonpath-rw >= 1.2.0
Requires:       python2-jsonschema >= 2.6.0
Requires:       python2-keystoneauth1 >= 3.3.0
Requires:       python2-keystonemiddleware >= 4.17.0
Requires:       python2-microversion-parse >= 0.1.2
Requires:       python2-openstacksdk >= 0.9.19
Requires:       python2-oslo-config >= 2:5.1.0
Requires:       python2-oslo-context >= 2.19.2
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-messaging >= 5.29.0
Requires:       python2-oslo-middleware >= 3.31.0
Requires:       python2-oslo-policy >= 1.30.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-service >= 1.24.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-oslo-versionedobjects >= 1.31.2
Requires:       python2-osprofiler >= 1.4.0
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-qpid
Requires:       python2-requests
Requires:       python2-pytz
Requires:       PyYAML
Requires:       python2-routes >= 2.3.1
Requires:       python2-six >= 1.10.0
Requires:       python2-sqlalchemy >= 1.0.10
Requires:       python-migrate >= 0.11.0
Requires:       python2-stevedore >= 1.20.0
Requires:       python-webob >= 1.7.1

%description -n python-%{service}
%{common_desc}

This package contains the Senlin Python library.

%package -n python-%{service}-tests-unit
Summary:        Senlin unit tests

Requires:       python2-testrepository
Requires:       python2-testscenarios
Requires:       python2-testtools
Requires:       python2-oslotest
Requires:       python2-os-testr
Requires:       python2-mock
Requires:       python-%{service} = %{version}-%{release}
BuildRequires:  python2-mock
BuildRequires:  python2-openstackdocstheme >= 1.11.0
BuildRequires:  python2-oslotest >= 1.10.0
BuildRequires:  python2-os-testr >= 0.8.0
BuildRequires:  python2-PyMySQL >= 0.7.6
BuildRequires:  python2-testrepository >= 0.0.18
BuildRequires:  python2-testscenarios >= 0.4
BuildRequires:  python2-testtools >= 1.4.0

%description -n python-%{service}-tests-unit
%{common_desc}

This package contains the Senlin unit test files.


%package common
Summary:        Senlin common files

Requires:       python-%{service} = %{version}-%{release}

%description common
%{common_desc}

This package contains Senlin common files.


%package doc
Summary:        Senlin documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-debtcollector

%description doc
%{common_desc}

This package contains the documentation.


%package api

Summary:        OpenStack Senlin API service
Requires:       %{name}-common = %{version}-%{release}

%description api
%{common_desc}

This package contains the ReST API.


%package engine

Summary:        OpenStack Senlin Engine service
Requires:       %{name}-common = %{version}-%{release}

%description engine
%{common_desc}

This package contains the Senline Engine service.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourselves
rm -f *requirements.txt

%build
%py2_build
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
oslo-config-generator --config-file tools/config-generator.conf \
                      --output-file etc/%{service}.conf.sample

%install
%py2_install

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}%{_prefix}/etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini
# Remove duplicate config files under /usr/etc/trove
rmdir %{buildroot}%{_prefix}/etc/%{service}

# Install dist conf
install -p -D -m 640 %{SOURCE3} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 etc/%{service}.conf.sample \
                     %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install systemd units
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-%{service}-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-%{service}-engine.service

%check
OS_TEST_PATH=./%{service}/tests/unit %{__python2} setup.py test

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Senlin Daemons" %{service}
exit 0

%post api
%systemd_post openstack-%{service}-api.service
%preun api
%systemd_preun openstack-%{service}-api.service
%postun api
%systemd_postun_with_restart openstack-%{service}-api.service

%post engine
%systemd_post openstack-%{service}-engine.service
%preun engine
%systemd_preun openstack-%{service}-engine.service
%postun engine
%systemd_postun_with_restart openstack-%{service}-engine.service

%files api
%license LICENSE
%{_bindir}/%{service}-api
%{_unitdir}/openstack-%{service}-api.service

%files engine
%license LICENSE
%{_bindir}/%{service}-engine
%{_unitdir}/openstack-%{service}-engine.service

%files -n python-%{service}-tests-unit
%license LICENSE
%{python2_sitelib}/%{service}/tests

%files -n python-%{service}
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common
%license LICENSE
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{service}
%dir %{_datadir}/%{service}
%dir %{_sysconfdir}/%{service}
%dir %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, root) %{_localstatedir}/log/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%{_bindir}/%{service}-manage
%{_bindir}/%{service}-wsgi-api


%files doc
%license LICENSE
%doc doc/build/html

%changelog
