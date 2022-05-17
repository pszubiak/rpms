%global srcname aioredis

Name:           python-%{srcname}
Version:        2.0.1
Release:        1%{?dist}
Summary:        asyncio (3156) Redis client library.
License:        MIT
URL:            https://github.com/aio-libs/aioredis-py
Source0:        https://github.com/aio-libs/aioredis-py/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist async-timeout}
BuildRequires:  %{py3_dist typing-extensions}
Recommends:     hiredis

%global _description %{expand:
The library is intended to provide simple and clear interface to Redis based on asyncio.}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n %{srcname}-py-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install


%files -n python3-%{srcname}
%doc README.md CONTRIBUTORS.txt
%license LICENSE
%{python3_sitelib}/aioredis/
%{python3_sitelib}/aioredis-%{version}.dist-info/

%changelog
* Tue May 17 2022 Piotr Szubiakowski <pszubiak@eso.org> - 2.0.1-1
- Init
