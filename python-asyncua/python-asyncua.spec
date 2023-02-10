%global srcname asyncua

Name:           python-%{srcname}
Version:        0.9.93
Release:        3%{?dist}
Summary:        OPC UA / IEC 62541 Client and Server for Python >= 3.7 and pypy3
License:        LGPL-3.0
URL:            https://github.com/FreeOpcUa/opcua-asyncio
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Patch0:         %{name}-disable-tests.patch
Patch1:         %{name}-eso.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist anyio}
BuildRequires:  %{py3_dist pytest-asyncio}
BuildRequires:  %{py3_dist pytest-mock}


%global _description %{expand:
opcua-asyncio is an asyncio-based asynchronous OPC UA client and server based on python-opcua,
removing support of python < 3.7. Asynchronous programming allows for simpler
code (e.g. less need for locks)and potentially performance gains. This library has also sync wrapper
over async API which may can be used in sync code instead of python-opcua}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n opcua-asyncio-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files asyncua


%check
%pytest


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license COPYING
%{_bindir}/*


%changelog
* Fri Feb 10 2023 Piotr Szubiakowski <pszubiak@eso.org> - 0.9.93-3
- Add patch from ESO

* Mon May 30 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.9.93-2
- Add unit tests execution

* Thu May 19 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.9.93-1
- Init