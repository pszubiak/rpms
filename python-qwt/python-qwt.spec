%global srcname qwt

Name:           python-%{srcname}
Version:        0.10.0
Release:        1%{?dist}
Summary:        Qt plotting widgets for Python.
License:        LGPLv2 and MIT
URL:            https://github.com/PierreRaybaut/PythonQwt
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist qtpy}
BuildRequires:  %{py3_dist pyside2}
BuildRequires:  %{py3_dist numpy}


%global _description %{expand:
The PythonQwt project was initiated to solve -at least temporarily- the obsolescence
issue of PyQwt (the Python-Qwt C++ bindings library) which is no longer maintained.
The idea was to translate the original Qwt C++ code to Python and then to optimize some
parts of the code by writing new modules based on NumPy and other libraries.}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n PythonQwt-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files qwt


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md CHANGELOG.md
%license LICENSE
%{_bindir}/*


%changelog
* Tue May 24 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.10.0-1
- Init