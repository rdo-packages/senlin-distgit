%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global service senlin

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
BuildRequires:  python-oslo-db
BuildRequires:  python-babel
BuildRequires:  python-docker
BuildRequires:  python-eventlet
BuildRequires:  python-jsonpath-rw
BuildRequires:  python-jsonschema
BuildRequires:  python-keystoneauth1
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-microversion-parse
BuildRequires:  python-openstacksdk
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-context
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  python-osprofiler
BuildRequires:  python-paste-deploy
BuildRequires:  python-qpid
BuildRequires:  python-requests
BuildRequires:  python-routes
BuildRequires:  python-six
BuildRequires:  python-sqlalchemy
BuildRequires:  python-migrate
BuildRequires:  python-stevedore
BuildRequires:  python-webob
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

# Required to compile translation files
BuildRequires:  python-babel

Requires:       openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils

%{?systemd_requires}
BuildRequires:  systemd
BuildRequires:  systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

%package -n python-%{service}
Summary:        Senlin Python libraries

Requires:       python-oslo-db >= 2.0
Requires:       python-pbr >= 2.0.0
Requires:       python-babel >= 2.3.4
Requires:       python-docker >= 2.0.0
Requires:       python-eventlet >= 0.18.2
Requires:       python-jsonpath-rw >= 1.2.0
Requires:       python-jsonschema >= 2.0.0
Requires:       python-keystoneauth1 >= 2.21.0
Requires:       python-keystonemiddleware >= 4.12.0
Requires:       python-microversion-parse >= 0.1.2
Requires:       python-openstacksdk >= 0.9.17
Requires:       python-oslo-config >= 2:4.0.0
Requires:       python-oslo-context >= 2.14.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.22.0
Requires:       python-oslo-messaging >= 5.24.2
Requires:       python-oslo-middleware >= 3.27.0
Requires:       python-oslo-policy >= 1.23.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-service >= 1.10.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-oslo-versionedobjects >= 1.17.0
Requires:       python-osprofiler >= 1.4.0
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-qpid
Requires:       python-requests
Requires:       python-routes >= 2.3.1
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 1.0.10
Requires:       python-migrate >= 0.11.0
Requires:       python-stevedore >= 1.20.0
Requires:       python-webob >= 1.7.1

%description -n python-%{service}
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains the Senlin Python library.

%package -n python-%{service}-tests-tempest
Summary:        Senlin tempest tests
Requires:       python-%{service} = %{version}-%{release}

%description -n python-%{service}-tests-tempest
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains the Senlin tempest test files.

%package -n python-%{service}-tests-unit
Summary:        Senlin unit tests

Requires:       python-testrepository
Requires:       python-testscenarios
Requires:       python-testtools
Requires:       python-oslotest
Requires:       python-os-testr
Requires:       python-mock
BuildRequires:  python-mock
BuildRequires:  python-openstackdocstheme >= 1.11.0
BuildRequires:  python-oslotest >= 1.10.0
BuildRequires:  python-os-testr >= 0.8.0
BuildRequires:  python-PyMySQL >= 0.7.6
BuildRequires:  python-testrepository >= 0.0.18
BuildRequires:  python-testscenarios >= 0.4
BuildRequires:  python-testtools >= 1.4.0


%description -n python-%{service}-tests-unit
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains the Senlin unit test files.

%package common
Summary:       Senlin common files

BuildRequires: python-osprofiler
BuildRequires: python-keystoneauth1
BuildRequires: python-oslo-middleware
BuildRequires: python-oslo-policy
BuildRequires: python-oslo-versionedobjects

Requires:      python-%{service} = %{version}-%{release}

%description common
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains Senlin common files.

%package doc
Summary:       Senlin documentation

BuildRequires: python-oslo-config
BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: python-oslo-i18n
BuildRequires: python-debtcollector

%description doc
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains the documentation.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourselves
rm -f *requirements.txt

%build
%py2_build
# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{service}/locale -D senlin
oslo-config-generator --config-file tools/config-generator.conf \
                      --output-file etc/%{service}.conf.sample

%install
%py2_install

# Create fake tempest plugin entry point
%py2_entrypoint %{service} %{service}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 640 etc/%{service}/api-paste.ini \
                     %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini
install -p -D -m 640 etc/%{service}/policy.json \
                     %{buildroot}%{_sysconfdir}/%{service}/policy.json

# Install dist conf
install -p -D -m 640 %{SOURCE3} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 etc/%{service}.conf.sample \
                     %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install systemd units
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-senlin-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-senlin-engine.service

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

%check
OS_TEST_PATH=./senlin/tests/unit %{__python2} setup.py test

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Senlin Daemons" %{service}
exit 0

%post
%systemd_post openstack-senlin-api.service
%systemd_post openstack-senlin-engine.service
%preun
%systemd_preun openstack-senlin-api.service
%systemd_preun openstack-senlin-engine.service
%postun
%systemd_postun_with_restart openstack-senlin-api.service
%systemd_postun_with_restart openstack-senlin-engine.service

%files
%license LICENSE
%{_bindir}/senlin-*
%{_unitdir}/openstack-senlin-api.service
%{_unitdir}/openstack-senlin-engine.service
%{_sysconfdir}/%{service}/api-paste.ini
%{_sysconfdir}/%{service}/policy.json

%files -n python-%{service}-tests-unit
%license LICENSE
%{python2_sitelib}/%{service}/tests

%files -n python-%{service}-tests-tempest
%license LICENSE
%{python2_sitelib}/%{service}/tests/tempest
%{python2_sitelib}/%{service}_tests.egg-info

%files -n python-%{service}
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common -f %{service}.lang
%license LICENSE
%dir %{_sysconfdir}/%{service}
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{service}
%dir %{_datadir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%dir %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, root) %{_localstatedir}/log/%{service}

%files doc
%license LICENSE
%doc doc/build/html

%changelog

