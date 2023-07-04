%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name networking-bgpvpn
%global sname networking_bgpvpn
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order pylint isort
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global docpath doc/build/html


%global with_doc 1

%global common_desc \
BGPMPLS VPN Extension for OpenStack Networking This project provides an API and \
Framework to interconnect BGP/MPLS VPNs to Openstack Neutron networks, routers \
and ports.The Border Gateway Protocol and MultiProtocol Label Switching are \
widely used Wide Area Networking technologies. The primary purpose of this \
project is to allow attachment of Neutron networks and/or routers to carrier \
provided.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        API and Framework to interconnect bgpvpn to neutron networks

License:        Apache-2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  openstack-macros
BuildRequires:  git-core
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-osc-lib-tests
BuildRequires:  python3-devel
BuildRequires:  openstack-dashboard
BuildRequires:  pyproject-rpm-macros

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        API and Framework to interconnect bgpvpn to neutron networks

Requires:       openstack-neutron-common >= 1:16.0.0

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        networking-bgpvpn documentation

%description -n python-%{pypi_name}-doc
Documentation for networking-bgpvpn
%endif

%package -n python3-%{pypi_name}-tests
Summary:        networking-bgpvpn tests
Requires:   python3-%{pypi_name} = %{version}-%{release}
Requires:   python3-webob >= 1.2.3

%description -n python3-%{pypi_name}-tests
Networking-bgpvpn set of tests

%package -n python3-%{pypi_name}-dashboard
Summary:    networking-bgpvpn dashboard

Requires: openstack-dashboard >= 1:17.1.0

Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-dashboard
Dashboard to be able to handle BGPVPN functionality via Horizon

%package -n python3-%{pypi_name}-heat
Summary:    networking-bgpvpn heat
Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-heat
Networking-bgpvpn heat resources

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

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
rm -rf %{docpath}/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

mkdir -p %{buildroot}%{_sysconfdir}/neutron/policy.d
mv %{buildroot}/usr/etc/neutron/networking_bgpvpn.conf %{buildroot}%{_sysconfdir}/neutron/

# Make sure neutron-server loads new configuration file
mkdir -p %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/networking_bgpvpn.conf %{buildroot}%{_datadir}/neutron/server/networking_bgpvpn.conf

%check
export OS_TEST_PATH="./networking_bgpvpn/tests/unit"
# We want to skip the bagpipe tests, and the only way to prevent them
# from being discovered is to remove them
rm -rf networking_bgpvpn/tests/unit/services/bagpipe
export PYTHONPATH=%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}:/usr/share/openstack-dashboard/
%tox -e %{default_toxenv}

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/networking_bgpvpn-*.dist-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/networking_bgpvpn.conf
%{_datadir}/neutron/server/networking_bgpvpn.conf
%exclude %{python3_sitelib}/%{sname}/tests
%exclude %{python3_sitelib}/bgpvpn_dashboard

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{sname}/tests

%files -n python3-%{pypi_name}-dashboard
%license LICENSE
%{python3_sitelib}/bgpvpn_dashboard/

%files -n python3-%{pypi_name}-heat
%license LICENSE
%{python3_sitelib}/networking_bgpvpn_heat

%changelog
