%global srcname opcua

Name:           python-%{srcname}
Version:        0.98.13
Release:        1%{?dist}
Summary:        Pure Python OPC UA / IEC 62541 Client and Server
License:        LGPLv3
URL:            https://github.com/FreeOpcUa/python-opcua
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}
BuildRequires:  python


%global _description %{expand:
Pure Python OPC UA / IEC 62541 Client and Server.}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n %{name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
sh run-tests.sh


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license COPYING
%{_bindir}/*


%changelog
* Fri May 27 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.98.13
- Init