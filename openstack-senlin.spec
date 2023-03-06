%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
Source5:        openstack-%{service}-conductor.service
Source6:        openstack-%{service}-health-manager.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  openstack-macros
BuildRequires:  python3-oslo-db
BuildRequires:  python3-docker
BuildRequires:  python3-eventlet
BuildRequires:  python3-jsonschema
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-keystonemiddleware
BuildRequires:  python3-microversion-parse
BuildRequires:  python3-openstacksdk
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-context
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-messaging
BuildRequires:  python3-oslo-middleware
BuildRequires:  python3-oslo-policy
BuildRequires:  python3-oslo-reports
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-service
BuildRequires:  python3-oslo-upgradecheck
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-versionedobjects
BuildRequires:  python3-osprofiler
BuildRequires:  python3-requests
BuildRequires:  python3-routes
BuildRequires:  python3-sqlalchemy
BuildRequires:  python3-stevedore
BuildRequires:  python3-webob
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-tenacity
BuildRequires:  git-core

# Required to compile translation files
BuildRequires:  python3-babel

BuildRequires:  python3-jsonpath-rw
BuildRequires:  python3-paste-deploy
BuildRequires:  python3-migrate

Requires:       openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
BuildRequires:  systemd

%description
%{common_desc}


%package -n python3-%{service}
Summary:        Senlin Python libraries
%{?python_provide:%python_provide python3-%{service}}

Requires:       python3-oslo-db >= 6.0.0
Requires:       python3-pbr >= 3.1.1
Requires:       python3-docker >= 2.4.2
Requires:       python3-eventlet >= 0.26.1
Requires:       python3-jsonschema >= 3.2.0
Requires:       python3-keystoneauth1 >= 3.18.0
Requires:       python3-keystonemiddleware >= 4.17.0
Requires:       python3-microversion-parse >= 0.2.1
Requires:       python3-openstacksdk >= 0.99.0
Requires:       python3-oslo-config >= 2:6.8.0
Requires:       python3-oslo-context >= 2.22.0
Requires:       python3-oslo-i18n >= 3.20.0
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-messaging >= 14.1.0
Requires:       python3-oslo-middleware >= 3.31.0
Requires:       python3-oslo-policy >= 3.6.0
Requires:       python3-oslo-reports >= 1.18.0
Requires:       python3-oslo-serialization >= 2.25.0
Requires:       python3-oslo-service >= 1.31.0
Requires:       python3-oslo-upgradecheck >= 1.3.0
Requires:       python3-oslo-utils >= 4.5.0
Requires:       python3-oslo-versionedobjects >= 1.31.2
Requires:       python3-osprofiler >= 2.3.0
Requires:       python3-requests >= 2.20.0
Requires:       python3-pytz >= 2015.7
Requires:       python3-routes >= 2.3.1
Requires:       python3-sqlalchemy >= 1.0.10
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-webob >= 1.7.1
Requires:       python3-tenacity >= 6.0.0

Requires:       python3-jsonpath-rw >= 1.4.0
Requires:       python3-paste-deploy >= 1.5.0
Requires:       python3-yaml >= 5.1
Requires:       python3-migrate >= 0.13.0

%description -n python3-%{service}
%{common_desc}

This package contains the Senlin Python library.

%package -n python3-%{service}-tests-unit
Summary:        Senlin unit tests
%{?python_provide:%python_provide python3-%{service}-tests-unit}

Requires:       python3-testscenarios
Requires:       python3-testtools
Requires:       python3-oslotest
Requires:       python3-stestr
Requires:       python3-mock
Requires:       python3-%{service} = %{version}-%{release}
BuildRequires:  python3-mock
BuildRequires:  python3-openstackdocstheme >= 1.11.0
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-stestr
BuildRequires:  python3-PyMySQL >= 0.7.6
BuildRequires:  python3-testscenarios >= 0.4
BuildRequires:  python3-testtools >= 1.4.0

%description -n python3-%{service}-tests-unit
%{common_desc}

This package contains the Senlin unit test files.


%package common
Summary:        Senlin common files

Requires:       python3-%{service} = %{version}-%{release}

%description common
%{common_desc}

This package contains Senlin common files.

%if 0%{?with_doc}
%package doc
Summary:        Senlin documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-debtcollector

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

%package conductor

Summary:        OpenStack Senlin Conductor service
Requires:       %{name}-common = %{version}-%{release}

%description conductor
%{common_desc}

This package contains the Senlin Conductor service.

%package health-manager

Summary:        OpenStack Senlin Health Manager service
Requires:       %{name}-common = %{version}-%{release}

%description health-manager
%{common_desc}

This package contains the Senlin Health Manager service.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

# Remove hacking tests
rm senlin/tests/unit/test_hacking.py

# Let's handle dependencies ourselves
rm -f *requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

oslo-config-generator --config-file tools/config-generator.conf \
                      --output-file etc/%{service}.conf.sample

%install
%{py3_install}

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
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/openstack-%{service}-conductor.service
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/openstack-%{service}-health-manager.service

%check
PYTHON=%{__python3} OS_TEST_PATH=./%{service}/tests/unit stestr run

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

%post conductor
%systemd_post openstack-%{service}-conductor.service
%preun conductor
%systemd_preun openstack-%{service}-conductor.service
%postun conductor
%systemd_postun_with_restart openstack-%{service}-conductor.service

%post health-manager
%systemd_post openstack-%{service}-health-manager.service
%preun health-manager
%systemd_preun openstack-%{service}-health-manager.service
%postun health-manager
%systemd_postun_with_restart openstack-%{service}-health-manager.service

%files api
%license LICENSE
%{_bindir}/%{service}-api
%{_unitdir}/openstack-%{service}-api.service

%files engine
%license LICENSE
%{_bindir}/%{service}-engine
%{_unitdir}/openstack-%{service}-engine.service

%files conductor
%license LICENSE
%{_bindir}/%{service}-conductor
%{_unitdir}/openstack-%{service}-conductor.service

%files health-manager
%license LICENSE
%{_bindir}/%{service}-health-manager
%{_unitdir}/openstack-%{service}-health-manager.service

%files -n python3-%{service}-tests-unit
%license LICENSE
%{python3_sitelib}/%{service}/tests

%files -n python3-%{service}
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info
%exclude %{python3_sitelib}/%{service}/tests


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
