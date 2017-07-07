%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global service senlin

Name:		openstack-%{service}
Version:        4.0.0.0b3.dev17
Release:        1
Summary:	OpenStack Senlin Service
License:	ASL 2.0
URL:		http://launchpad.net/%{service}/

Source0:	http://tarballs.openstack.org/%{service}/%{service}-master.tar.gz
Source1:	%{service}.logrotate
Source2:	openstack-%{service}-api.service
Source3:	openstack-%{service}-engine.service
Source4:        %{service}-dist.conf

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
BuildRequires:  git
BuildRequires:	systemd
BuildRequires:	systemd-units
# Required to compile translation files
BuildRequires:  python-babel

Requires:	openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

%package -n python-%{service}
Summary:	Senlin Python libraries

Requires:	python-oslo-db >= 2.0

%description -n python-%{service}
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains the Senlin Python library.


%package -n python-%{service}-tests
Summary:	Senlin tests
Requires:	python-%{service} = %{version}-%{release}

%description -n python-%{service}-tests
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains the Senlin test files.

%package common
Summary:	Senlin common files

BuildRequires: python2-osprofiler
BuildRequires: python2-keystoneauth1
BuildRequires: python2-oslo-middleware
BuildRequires: python2-oslo-policy
BuildRequires: python2-oslo-versionedobjects

Requires:	python-%{service} = %{version}-%{release}

%description common
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains Senlin common files.

%package doc
Summary:	Senlin documentation

BuildRequires: python2-oslo-config
BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-oslo-i18n
BuildRequires: python2-debtcollector

%description doc
Senlin is a clustering service for OpenStack cloud.
It creates and operates clusters of homogenous objects exposed by other
OpenStack services.
The goal is to make orchestration of collections of similar objects easier.

This package contains the documentation.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
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

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests


%files -n python-%{service}
%license LICENSE
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

