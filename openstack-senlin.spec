# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

#FIXME(jpena): re-enable doc build once we have Sphinx > 1.6.5 or docutils > 0.11
%global with_doc 0

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
BuildRequires:  python%{pyver}-oslo-db
BuildRequires:  python%{pyver}-docker
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-jsonschema
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-keystonemiddleware
BuildRequires:  python%{pyver}-microversion-parse
BuildRequires:  python%{pyver}-openstacksdk
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-context
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-messaging
BuildRequires:  python%{pyver}-oslo-middleware
BuildRequires:  python%{pyver}-oslo-policy
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-oslo-service
BuildRequires:  python%{pyver}-oslo-upgradecheck
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-oslo-versionedobjects
BuildRequires:  python%{pyver}-osprofiler
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-routes
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-sqlalchemy
BuildRequires:  python%{pyver}-stevedore
BuildRequires:  python%{pyver}-webob
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git

# Required to compile translation files
BuildRequires:  python%{pyver}-babel

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-pep8
BuildRequires:  python-jsonpath-rw
BuildRequires:  python-paste-deploy
BuildRequires:  python-migrate
%else
BuildRequires:  python%{pyver}-pep8
BuildRequires:  python%{pyver}-jsonpath-rw
BuildRequires:  python%{pyver}-paste-deploy
BuildRequires:  python%{pyver}-migrate
%endif

Requires:       openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils

%{?systemd_requires}
BuildRequires:  systemd

%description
%{common_desc}


%package -n python%{pyver}-%{service}
Summary:        Senlin Python libraries
%{?python_provide:%python_provide python%{pyver}-%{service}}

Requires:       python%{pyver}-oslo-db >= 4.27.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-docker >= 2.4.2
Requires:       python%{pyver}-eventlet >= 0.18.2
Requires:       python%{pyver}-jsonschema >= 2.6.0
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-keystonemiddleware >= 4.17.0
Requires:       python%{pyver}-microversion-parse >= 0.2.1
Requires:       python%{pyver}-openstacksdk >= 0.11.2
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-context >= 2.19.2
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-messaging >= 5.29.0
Requires:       python%{pyver}-oslo-middleware >= 3.31.0
Requires:       python%{pyver}-oslo-policy >= 1.30.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-service >= 1.24.0
Requires:       python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-oslo-versionedobjects >= 1.31.2
Requires:       python%{pyver}-osprofiler >= 1.4.0
Requires:       python%{pyver}-requests
Requires:       python%{pyver}-pytz
Requires:       python%{pyver}-routes >= 2.3.1
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-sqlalchemy >= 1.0.10
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-webob >= 1.7.1
Requires:       python%{pyver}-tenacity >= 4.9.0

# Handle python2 exception
%if %{pyver} == 2
Requires:       python-jsonpath-rw >= 1.2.0
Requires:       python-paste-deploy >= 1.5.0
Requires:       PyYAML
Requires:       python-migrate >= 0.11.0
%else
Requires:       python%{pyver}-jsonpath-rw >= 1.2.0
Requires:       python%{pyver}-paste-deploy >= 1.5.0
Requires:       python%{pyver}-PyYAML
Requires:       python%{pyver}-migrate >= 0.11.0
%endif

%description -n python%{pyver}-%{service}
%{common_desc}

This package contains the Senlin Python library.

%package -n python%{pyver}-%{service}-tests-unit
Summary:        Senlin unit tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests-unit}

Requires:       python%{pyver}-testscenarios
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-stestr
Requires:       python%{pyver}-mock
Requires:       python%{pyver}-%{service} = %{version}-%{release}
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-openstackdocstheme >= 1.11.0
BuildRequires:  python%{pyver}-oslotest >= 1.10.0
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-PyMySQL >= 0.7.6
BuildRequires:  python%{pyver}-testscenarios >= 0.4
BuildRequires:  python%{pyver}-testtools >= 1.4.0

%description -n python%{pyver}-%{service}-tests-unit
%{common_desc}

This package contains the Senlin unit test files.


%package common
Summary:        Senlin common files

Requires:       python%{pyver}-%{service} = %{version}-%{release}

%description common
%{common_desc}

This package contains Senlin common files.

%if 0%{?with_doc}
%package doc
Summary:        Senlin documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-debtcollector

%description doc
%{common_desc}

This package contains the documentation.
%endif

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
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

oslo-config-generator-%{pyver} --config-file tools/config-generator.conf \
                      --output-file etc/%{service}.conf.sample

%install
%{pyver_install}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}%{_prefix}/etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini
# Remove duplicate config files under /usr/etc/senlin
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
OS_TEST_PATH=./%{service}/tests/unit stestr-%{pyver} run

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

%files -n python%{pyver}-%{service}-tests-unit
%license LICENSE
%{pyver_sitelib}/%{service}/tests

%files -n python%{pyver}-%{service}
%{pyver_sitelib}/%{service}
%{pyver_sitelib}/%{service}-*.egg-info
%exclude %{pyver_sitelib}/%{service}/tests


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
%{_bindir}/%{service}-status
%{_bindir}/%{service}-wsgi-api

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
# REMOVEME: error caused by commit https://github.com/openstack/senlin/commit/b30b2b8496b2b8af243ccd5292f38aec7a95664f
