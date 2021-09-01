%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name networking-bgpvpn
%global sname networking_bgpvpn
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
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

License:        ASL 2.0
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
BuildRequires:  python3-webob
BuildRequires:  python3-hacking
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-neutron
BuildRequires:  python3-osc-lib-tests
BuildRequires:  python3-oslotest
BuildRequires:  python3-openstackclient
BuildRequires:  python3-openvswitch
BuildRequires:  python3-pbr
BuildRequires:  python3-subunit
BuildRequires:  python3-stestr
BuildRequires:  python3-testrepository
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-devel

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        API and Framework to interconnect bgpvpn to neutron networks
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-pbr >= 4.0.0
Requires:       python3-neutron-lib >= 1.30.0
Requires:       python3-neutronclient >= 6.3.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-db >= 4.37.0
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-debtcollector >= 1.19.0
Requires:       openstack-neutron-common >= 1:16.0.0

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        networking-bgpvpn documentation

BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-blockdiag
BuildRequires:  python3-sphinxcontrib-seqdiag

%description -n python-%{pypi_name}-doc
Documentation for networking-bgpvpn
%endif

%package -n python3-%{pypi_name}-tests
%{?python_provide:%python_provide python3-%{pypi_name}-tests}
Summary:        networking-bgpvpn tests
Requires:   python3-%{pypi_name} = %{version}-%{release}

Requires:   python3-webob >= 1.2.3

%description -n python3-%{pypi_name}-tests
Networking-bgpvpn set of tests

%package -n python3-%{pypi_name}-dashboard
Summary:    networking-bgpvpn dashboard
%{?python_provide:%python_provide python3-%{pypi_name}-dashboard}
Requires: python3-%{pypi_name} = %{version}-%{release}
Requires: openstack-dashboard >= 1:17.1.0

%description -n python3-%{pypi_name}-dashboard
Dashboard to be able to handle BGPVPN functionality via Horizon

%package -n python3-%{pypi_name}-heat
Summary:    networking-bgpvpn heat
%{?python_provide:%python_provide python3-%{pypi_name}-heat}
Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-heat
Networking-bgpvpn heat resources

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build
%if 0%{?with_doc}
# generate html docs
PYTHONPATH=. sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf %{docpath}/.{doctrees,buildinfo}
%endif

%install
%py3_install

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
stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/networking_bgpvpn-*.egg-info
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
