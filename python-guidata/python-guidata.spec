%global srcname guidata

Name:           python-%{srcname}
Version:        2.2.0
Release:        1%{?dist}
Summary:        Automatic GUI generation for easy dataset editing and display with Python.
License:        CeCILL
URL:            https://github.com/PierreRaybaut/guidata
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist qtpy}


%global _description %{expand:
Based on the Qt library, guidata is a Python library generating graphical user interfaces for easy dataset
editing and display. It also provides helpers and application development tools for Qt.}


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
%pyproject_save_files %{srcname}


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md CHANGELOG.md
%license Licence_CeCILL_V2-en.txt
%{_bindir}/*


%changelog
* Fri May 20 2022 Piotr Szubiakowski <pszubiak@eso.org> - 2.2.0-1
- Init