%global srcname taurus

Name:           python-%{srcname}
Version:        5.1.4
Release:        1%{?dist}
Summary:        A framework for scientific/industrial CLIs and GUIs
License:        LGPL-3.0
URL:            https://www.taurus-scada.org/
Source0:        https://files.pythonhosted.org/packages/8b/24/367a16584e5a42ee8c9dd4f0745b7060978e43382768e4a7f9c1ad270a12/taurus-5.1.4.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pint}

%global _description %{expand:
Taurus is a python framework for control and data acquisition CLIs and GUIs in
scientific/industrial environments. It supports multiple control systems or data
sources: Tango, EPICS. New control system libraries can be integrated through plugins.}


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
%py3_shebang_fix %{buildroot}/usr/lib/python%{python3_version}/site-packages/taurus/core/tango/test/res/TangoSchemeTest
%py3_shebang_fix %{buildroot}/usr/lib/python%{python3_version}/site-packages/taurus/qt/qtgui/button/test/res/Timeout


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGELOG.md
%license LICENSE.txt
%{_bindir}/taurus


%changelog
* Thu Jun 2 2022 Piotr Szubiakowski <pszubiak@eso.org> - 5.1.4-1
- Init
