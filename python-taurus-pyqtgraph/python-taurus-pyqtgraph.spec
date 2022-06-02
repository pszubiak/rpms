%global srcname taurus-pyqtgraph

Name:           python-%{srcname}
Version:        0.5.9
Release:        1%{?dist}
Summary:        Taurus extension providing pyqtgraph-based widgets
License:        LGPL-3.0
URL:            https://www.taurus-scada.org/
Source0:        https://files.pythonhosted.org/packages/30/06/e2901f5f9bb1c0ddba5d4b2eb7cd0d5f2678e8f717d42d8b058168b74c18/taurus_pyqtgraph-0.5.9.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pyqtgraph}

%global _description %{expand:
taurus_pyqtgraph is an extension package for the Taurus package. It
adds the taurus.qt.qtgui.tpg submodule which provides pyqtgraph-based
widgets. The rationale behind taurus_pyqtgraph is described in the TEP17}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n taurus_pyqtgraph-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files taurus_pyqtgraph


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md CHANGELOG.md
%license LICENSE.txt


%changelog
* Thu Jun 2 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.5.9-1
- Init
