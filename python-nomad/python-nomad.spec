%global srcname nomad

Name:           python-%{srcname}
Version:        1.3.0
Release:        1%{?dist}
Summary:        Python library for Hashicorp Nomad
License:        MIT
URL:            https://github.com/jrxFive/python-nomad
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel


%global _description %{expand:
Python library for Hashicorp NomadThis library also supports environment
variables: NOMAD_ADDR, NOMAD_NAMESPACE, NOMAD_TOKEN, NOMAD_REGION for ease 
of configuration and unifying with nomad cli tools and other libraries.}


%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname} %{_description}


%prep
%autosetup -p 1 -n %{name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files nomad


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md CONTRIBUTING.md
%license LICENSE


%changelog
* Mon Oct 24 2022 Piotr Szubiakowski <pszubiak@eso.org> - 1.3.0-1
- Init