%global srcname guiqwt

Name:           python-%{srcname}
Version:        4.1.1
Release:        1%{?dist}
Summary:        Python tools for curve and image plotting.
License:        CeCILL
URL:            https://github.com/PierreRaybaut/guiqwt
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:      x86_64

BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist guidata}
BuildRequires:  %{py3_dist Cython}
Recommends:     %{py3_dist dicom}
Recommends:     %{py3_dist spyder}


%global _description %{expand:
Based on PythonQwt (a pure Python/PyQt reimplementation of the curve plotting Qwt C++ library,
included in guiqwt base source code) and on the scientific modules NumPy and SciPy,
guiqwt is a Python library providing efficient 2D data-plotting
features (curve/image visualization and related tools) for interactive computing and signal/image
processing application development. It is based on Qt graphical user interfaces library.}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n guiqwt-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files guiqwt


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md CHANGELOG.md
%license Licence_CeCILL_V2-en.txt
%{_bindir}/*


%changelog
* Tue May 24 2022 Piotr Szubiakowski <pszubiak@eso.org> - 4.1.1-1
- Init
