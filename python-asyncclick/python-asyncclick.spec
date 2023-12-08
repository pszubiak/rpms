%global srcname asyncclick

Name:           python-%{srcname}
Version:        8.0.3.2
Release:        2%{?dist}
Summary:        AsyncClick is a fork of Click that works well with trio or asyncio.
License:        BSD-3-Clause
URL:            https://github.com/python-trio/asyncclick
Source0:        https://files.pythonhosted.org/packages/c2/ae/6e4d9557a0625490a99e096eb9686b317e989a83eb5c422220eb36cb689f/asyncclick-8.0.3.2.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist anyio}
BuildRequires:  %{py3_dist trio}
BuildRequires:  %{py3_dist curio}
BuildRequires:  %{py3_dist attrs}
BuildRequires:  %{py3_dist packaging}
BuildRequires:  %{py3_dist pluggy}
BuildRequires:  %{py3_dist py}
BuildRequires:  %{py3_dist pytest}

Requires:  %{py3_dist anyio}


%global _description %{expand:
Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
It's the "Command Line Interface Creation Kit". It's highly configurable but comes with sensible defaults out of the box.

It aims to make the process of writing command line tools quick and fun while also preventing any frustration
caused by the inability to implement an intended CLI API.

AsyncClick in four points:

* Arbitrary nesting of commands
* Automatic help page generation
* Supports lazy loading of subcommands at runtime
* Seamlessly use async-enabled command and subcommand handlers
}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files asyncclick

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE.rst


%changelog
* Fri Dec 08 2023 Federico Pellegrin <fede@evolware.org> - 8.0.3.2-2
- Add missing anyio runtime dependency

* Tue May 17 2022 Piotr Szubiakowski <pszubiak@eso.org> - 8.0.3.2-1
- Init
