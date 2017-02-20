%{!?upstream_version: %global upstream_version %{commit}}
%global commit 681a5e742fff2c03ef9b441851af508e6591286c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global pypi_name networking-bgpvpn
%global sname networking_bgpvpn

Name:           python-%{pypi_name}
Version:        6.0.0
Release:        0.1%{?alphatag}%{?dist}
Summary:        API and Framework to interconnect bgpvpn to neutron networks

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://github.com/openstack/%{pypi_name}/archive/%{commit}.tar.gz#/%{pypi_name}-%{shortcommit}.tar.gz

BuildArch:      noarch

BuildRequires:  python-webob
BuildRequires:  python-webtest
BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-networking-odl
BuildRequires:  python-networking-bagpipe
BuildRequires:  python-neutron-tests
BuildRequires:  python-neutron
BuildRequires:  python-osc-lib-tests
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-openstackclient
BuildRequires:  python-openvswitch
BuildRequires:  python-pbr
BuildRequires:  python-reno
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
#BuildRequires:  python-sphinxcontrib-blockdiag
#BuildRequires:  python-sphinxcontrib-seqdiag
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python2-devel

%description
BGPMPLS VPN Extension for OpenStack Networking This project provides an API and
Framework to interconnect BGP/MPLS VPNs to Openstack Neutron networks, routers
and ports.The Border Gateway Protocol and MultiProtocol Label Switching are
widely used Wide Area Networking technologies. The primary purpose of this
project is to allow attachment of Neutron networks and/or routers to carrier
provided.

%package -n     python2-%{pypi_name}
Summary:        API and Framework to interconnect bgpvpn to neutron networks
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-webob >= 1.2.3
Requires:       python-webtest >= 2.0
Requires:       python-pbr >= 1.8
Requires:       python-babel >= 2.3.4
Requires:       python-neutron-lib >= 1.1.0
Requires:       python-neutronclient >= 5.1.0
Requires:       python-openstackclient >= 3.3.0
Requires:       python-oslo-config >= 2:3.14.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-db >= 4.15.0
Requires:       python-oslo-log >= 3.11.0
Requires:       python-oslo-utils >= 3.18.0
Requires:       python-setuptools
Requires:       openstack-neutron-common

%description -n python2-%{pypi_name}
BGPMPLS VPN Extension for OpenStack Networking This project provides an API and
Framework to interconnect BGP/MPLS VPNs to Openstack Neutron networks, routers
and ports.The Border Gateway Protocol and MultiProtocol Label Switching are
widely used Wide Area Networking technologies. The primary purpose of this
project is to allow attachment of Neutron networks and/or routers to carrier
provided.

%package -n python-%{pypi_name}-doc
Summary:        networking-bgpvpn documentation
%description -n python-%{pypi_name}-doc
Documentation for networking-bgpvpn

%package -n python-%{pypi_name}-tests
Summary:        networking-bgpvpn tests
Requires:   python-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-tests
Networking-bgpvpn set of tests

%package -n python-%{pypi_name}-dashboard
Summary:    networking-bgpvpn dashboard
Requires: python-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-dashboard
Dashboard to be able to handle BGPVPN functionality via Horizon

%package -n python-%{pypi_name}-heat
Summary:    networking-bgpvpn heat
Requires: python-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-heat
Networking-bgpvpn heat resources

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
# generate html docs
# TODO: the doc generation is commented until python-sphinxcontrib-* packages
# are included in CBS. This needs to be fixed.
#%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

mkdir -p %{buildroot}%{_sysconfdir}/neutron/policy.d
mv %{buildroot}/usr/etc/neutron/networking_bgpvpn.conf %{buildroot}%{_sysconfdir}/neutron/
mv %{buildroot}/usr/etc/neutron/policy.d/bgpvpn.conf %{buildroot}%{_sysconfdir}/neutron/policy.d/

# Make sure neutron-server loads new configuration file
mkdir -p %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/networking_bgpvpn.conf %{buildroot}%{_datadir}/neutron/server/networking_bgpvpn.conf

%check
%{__python2} setup.py testr

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/networking_bgpvpn_tempest
%{python2_sitelib}/networking_bgpvpn-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/networking_bgpvpn.conf
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/policy.d/bgpvpn.conf
%{_datadir}/neutron/server/networking_bgpvpn.conf
%exclude %{python2_sitelib}/%{sname}/tests
%exclude %{python2_sitelib}/bgpvpn_dashboard

%files -n python-%{pypi_name}-doc
#%doc html
%license LICENSE

%files -n python-%{pypi_name}-tests
%license LICENSE
%doc networking_bgpvpn_tempest/README.rst
%{python2_sitelib}/%{sname}/tests

%files -n python-%{pypi_name}-dashboard
%license LICENSE
%{python2_sitelib}/bgpvpn_dashboard/

%files -n python-%{pypi_name}-heat
%license LICENSE
%{python2_sitelib}/networking_bgpvpn_heat

%changelog
* Mon Feb 20 2017 Alfredo Moralejo <amoralej@redhat.com> - 6.0.0-0.1.681a5e74git
- Update to pre-release 6.0.0 (681a5e742fff2c03ef9b441851af508e6591286c)
