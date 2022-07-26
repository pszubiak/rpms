%global srcname elasticsearch

Name:           python-%{srcname}
Version:        6.8.2
Release:        1%{?dist}
Summary:        Elasticsearch Python Client
License:        ASL 2.0
URL:            https://github.com/elastic/elasticsearch-py
Source:         %{url}/archive/%{version}/%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel


%global _description %{expand:
The official Python client for Elasticsearch.}


%description    %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname} %{_description}


%prep
%autosetup -p 1 -n %{srcname}-py-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
* Tue Jul 26 2022 Piotr Szubiakowski <pszubiak@eso.org> - 6.8.2-1
- Init
