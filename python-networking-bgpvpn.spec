%global pypi_name networking-bgpvpn
%global sname networking_bgpvpn
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global docpath doc/build/html

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
%global pyver_entrypoint %py%{pyver}_entrypoint %{sname} %{pypi_name}
# End of macros for py2/py3 compatibility

%global with_doc 1

%global common_desc \
BGPMPLS VPN Extension for OpenStack Networking This project provides an API and \
Framework to interconnect BGP/MPLS VPNs to Openstack Neutron networks, routers \
and ports.The Border Gateway Protocol and MultiProtocol Label Switching are \
widely used Wide Area Networking technologies. The primary purpose of this \
project is to allow attachment of Neutron networks and/or routers to carrier \
provided.

Name:           python-%{pypi_name}
Version:        11.0.1
Release:        1%{?dist}
Summary:        API and Framework to interconnect bgpvpn to neutron networks

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#

BuildArch:      noarch

BuildRequires:  openstack-macros
BuildRequires:  git
BuildRequires:  python%{pyver}-webob
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-networking-bagpipe
BuildRequires:  python%{pyver}-neutron-lib-tests
BuildRequires:  python%{pyver}-neutron-tests
BuildRequires:  python%{pyver}-neutron
BuildRequires:  python%{pyver}-osc-lib-tests
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-openstackclient
BuildRequires:  python%{pyver}-openvswitch
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-devel

%if %{pyver} == 2
BuildRequires:  python-networking-odl
%else
BuildRequires:  python%{pyver}-networking-odl
%endif

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        API and Framework to interconnect bgpvpn to neutron networks
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

Requires:       python%{pyver}-webob >= 1.2.3
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-neutron-lib >= 1.18.0
Requires:       python%{pyver}-neutronclient >= 6.3.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-db >= 4.27.0
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-debtcollector >= 1.2.0
Requires:       openstack-neutron-common >= 1:13.0.0

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        networking-bgpvpn documentation

BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-sphinxcontrib-blockdiag
BuildRequires:  python%{pyver}-sphinxcontrib-seqdiag

%description -n python-%{pypi_name}-doc
Documentation for networking-bgpvpn
%endif

%package -n python%{pyver}-%{pypi_name}-tests
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-tests}
Summary:        networking-bgpvpn tests
Requires:   python%{pyver}-%{pypi_name} = %{version}-%{release}

%description -n python%{pyver}-%{pypi_name}-tests
Networking-bgpvpn set of tests

%package -n python%{pyver}-%{pypi_name}-dashboard
Summary:    networking-bgpvpn dashboard
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-dashboard}
Requires: python%{pyver}-%{pypi_name} = %{version}-%{release}
Requires: openstack-dashboard >= 1:14.0.0

%description -n python%{pyver}-%{pypi_name}-dashboard
Dashboard to be able to handle BGPVPN functionality via Horizon

%package -n python%{pyver}-%{pypi_name}-heat
Summary:    networking-bgpvpn heat
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-heat}
Requires: python%{pyver}-%{pypi_name} = %{version}-%{release}

%description -n python%{pyver}-%{pypi_name}-heat
Networking-bgpvpn heat resources

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%pyver_build
%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf %{docpath}/.{doctrees,buildinfo}
%endif

%install
%pyver_install

mkdir -p %{buildroot}%{_sysconfdir}/neutron/policy.d
mv %{buildroot}/usr/etc/neutron/networking_bgpvpn.conf %{buildroot}%{_sysconfdir}/neutron/

# Make sure neutron-server loads new configuration file
mkdir -p %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/networking_bgpvpn.conf %{buildroot}%{_datadir}/neutron/server/networking_bgpvpn.conf

%check
export OS_TEST_PATH="./networking_bgpvpn/tests/unit"
# (ykarel) Ignore unit tests result until https://review.openstack.org/#/c/598347/ is in promoted repo.
stestr-%{pyver} --test-path $OS_TEST_PATH run || true

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/networking_bgpvpn-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/networking_bgpvpn.conf
%{_datadir}/neutron/server/networking_bgpvpn.conf
%exclude %{pyver_sitelib}/%{sname}/tests
%exclude %{pyver_sitelib}/bgpvpn_dashboard

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/%{sname}/tests

%files -n python%{pyver}-%{pypi_name}-dashboard
%license LICENSE
%{pyver_sitelib}/bgpvpn_dashboard/

%files -n python%{pyver}-%{pypi_name}-heat
%license LICENSE
%{pyver_sitelib}/networking_bgpvpn_heat

%changelog
* Tue Feb 18 2020 RDO <dev@lists.rdoproject.org> 11.0.1-1
- Update to 11.0.1

* Wed Oct 16 2019 RDO <dev@lists.rdoproject.org> 11.0.0-1
- Update to 11.0.0

* Fri Oct 04 2019 RDO <dev@lists.rdoproject.org> 11.0.0-0.1.0rc1
- Update to 11.0.0.0rc1

