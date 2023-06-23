%global srcname pytest-qt

Name:           python-%{srcname}
Version:        4.2.0
Release:        1%{?dist}
Summary:        pytest plugin that allows programmers to write tests for PySide, and PyQt applications.
License:        MIT
URL:            https://github.com/pytest-dev/pytest-qt
Source0:        https://files.pythonhosted.org/packages/a9/bc/b9ace56bded8ab9d37f078253b5d38e7b06c1447d2acd9c67a5ffa166ee0/pytest-qt-4.2.0.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pyqt5}
BuildRequires:  %{py3_dist pyside2}
BuildRequires:  %{py3_dist tomli}

%global _description %{expand:
pytest-qt is a pytest plugin that allows programmers to write tests for PyQt5, PyQt6, PySide2 and PySide6 applications.

The main usage is to use the qtbot fixture, responsible for handling qApp creation as needed and
provides methods to simulate user interaction, like key presses and mouse clicks:

This allows you to test and make sure your view layer is behaving the way you expect after each code change.}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files pytestqt


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
* Fri Jun 23 2023 Federico Pellegrin <fede@evolware.org> - 4.2.0-1
- Bump to 4.2.0

* Tue May 17 2022 Piotr Szubiakowski <pszubiak@eso.org> - 4.0.2-1
- Init
