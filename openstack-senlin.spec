%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1

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
License:        Apache-2.0
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
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core

Requires:       openstack-%{service}-common = %{version}-%{release}

Requires(pre): shadow-utils

%{?systemd_ordering}

BuildRequires:  systemd

%description
%{common_desc}


%package -n python3-%{service}
Summary:        Senlin Python libraries

%description -n python3-%{service}
%{common_desc}

This package contains the Senlin Python library.

%package -n python3-%{service}-tests-unit
Summary:        Senlin unit tests

Requires:       python3-%{service} = %{version}-%{release}

Requires:       python3-testscenarios
Requires:       python3-testtools
Requires:       python3-oslotest
Requires:       python3-stestr

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


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslo-config-generator --config-file tools/config-generator.conf \
                      --output-file etc/%{service}.conf.sample


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
%tox -e %{default_toxenv}

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
%{python3_sitelib}/%{service}-*.dist-info
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
