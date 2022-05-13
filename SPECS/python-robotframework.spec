%global srcname robotframework

Name:           python-%{srcname}
Version:        4.1.3
Release:        2%{?dist}
Summary:        Generic automation framework for acceptance testing and RPA
License:        ASL 2.0
URL:            https://github.com/robotframework/robotframework
Source0:        %{url}/archive/refs/tags/v4.1.3.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-jsonschema

%global _description %{expand:
Robot Framework is a generic open source automation framework for acceptance testing,
acceptance test driven development (ATDD), and robotic process automation (RPA).
It has simple plain text syntax and it can be extended easily with libraries implemented
using Python or Java.}


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


%check
%{python3} utest/run.py


%files -n python3-%{srcname}
%doc README.rst BUILD.rst INSTALL.rst CONTRIBUTING.rst
%license LICENSE.txt
%{python3_sitelib}/robot/
%{python3_sitelib}/robotframework-%{version}.dist-info/
%{_bindir}/*


%changelog
* Fri May 13 2022 Piotr Szubiakowski <pszubiak@eso.org> - 4.1.3-2
- Adapt to Fedora Python Packaging Guidelines

* Fri Feb 18 2022 Federico Pellegrin <fede@evolware.org> - 4.1.3-1
- First packaging of robotframework
