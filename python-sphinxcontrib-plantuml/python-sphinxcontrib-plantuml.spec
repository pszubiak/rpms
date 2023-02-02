%global srcname sphinxcontrib-plantuml

Name:           python-%{srcname}
Version:        0.24.1
Release:        1%{?dist}
Summary:        Sphinx plantuml extension

License:        BSD-2-Clause
URL:            https://github.com/sphinx-contrib/plantuml
BuildArch:      noarch
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# Skip buildpdf_simple test, further investigation is needed
Patch:          %{name}-pytest.patch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist docutils}
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist wheel}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist rst2pdf}
BuildRequires:  plantuml
BuildRequires:  latexmk
BuildRequires:  tex(latex)
BuildRequires:  tex(plantuml.sty)

%global _description %{expand:
This sphinx extension provides a support for PlantUML.}


%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname} %{_description}


%prep
%autosetup -p1 -n plantuml-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files sphinxcontrib


%check
%{pytest}


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE
%{python3_sitelib}/sphinxcontrib_plantuml-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Thu Feb 02 2023 Piotr Szubiakowski <pszubiak@eso.org> - 0.24.1-1
- Init
