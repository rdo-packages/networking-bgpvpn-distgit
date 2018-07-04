%global pypi_name networking-bgpvpn
%global sname networking_bgpvpn
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

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
BuildArch:      noarch

BuildRequires:  openstack-macros
BuildRequires:  git
BuildRequires:  python-webob
BuildRequires:  python2-hacking
BuildRequires:  python-networking-odl
BuildRequires:  python2-networking-bagpipe
BuildRequires:  python-neutron-tests
BuildRequires:  python-neutron
BuildRequires:  python2-osc-lib-tests
BuildRequires:  python2-oslotest
BuildRequires:  python2-openstackclient
BuildRequires:  python2-openvswitch
BuildRequires:  python2-pbr
BuildRequires:  python2-subunit
BuildRequires:  python2-testrepository
BuildRequires:  python2-testresources
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
BuildRequires:  python2-devel

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        API and Framework to interconnect bgpvpn to neutron networks
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-webob >= 1.2.3
Requires:       python2-pbr >= 2.0.0
Requires:       python2-babel >= 2.3.4
Requires:       python2-neutron-lib >= 1.13.0
Requires:       python2-neutronclient >= 6.3.0
Requires:       python2-oslo-config >= 2:5.1.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-db >= 4.27.0
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-debtcollector >= 1.2.0
Requires:       openstack-neutron-common

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        networking-bgpvpn documentation

BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinx
BuildRequires:  python2-sphinxcontrib-blockdiag
BuildRequires:  python2-sphinxcontrib-seqdiag

%description -n python-%{pypi_name}-doc
Documentation for networking-bgpvpn
%endif

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

%package -n python-%{pypi_name}-tests-tempest
Summary:    %{name} Tempest plugin

Requires:   python-%{pypi_name} = %{version}-%{release}
Requires:   python-tempest
Requires:   python-testtools

%description -n python-%{pypi_name}-tests-tempest
It contains the tempest plugin for %{sname}

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%py2_install

mkdir -p %{buildroot}%{_sysconfdir}/neutron/policy.d
mv %{buildroot}/usr/etc/neutron/networking_bgpvpn.conf %{buildroot}%{_sysconfdir}/neutron/
mv %{buildroot}/usr/etc/neutron/policy.d/bgpvpn.conf %{buildroot}%{_sysconfdir}/neutron/policy.d/

# Make sure neutron-server loads new configuration file
mkdir -p %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/networking_bgpvpn.conf %{buildroot}%{_datadir}/neutron/server/networking_bgpvpn.conf

# Create a fake tempest plugin entry point
%py2_entrypoint %{sname} %{pypi_name}

%check
%{__python2} setup.py testr

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/networking_bgpvpn-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/networking_bgpvpn.conf
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/policy.d/bgpvpn.conf
%{_datadir}/neutron/server/networking_bgpvpn.conf
%exclude %{python2_sitelib}/%{sname}/tests
%exclude %{python2_sitelib}/bgpvpn_dashboard

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

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

%files -n python-%{pypi_name}-tests-tempest
%{python2_sitelib}/networking_bgpvpn_tempest
%{python2_sitelib}/%{sname}_tests.egg-info

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/networking-bgpvpn/commit/?id=e9ab21a29d944f298616538fd1442201519be507
