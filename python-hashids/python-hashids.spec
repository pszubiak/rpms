%global srcname hashids

Name:           python-%{srcname}
Version:        1.3.1
Release:        1%{?dist}
Summary:        Generate short unique ids from integers.
License:        MIT
URL:            http://www.hashids.org/
Source0:        https://github.com/davidaurelio/hashids-python/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist flit-core}


%global _description %{expand:
A python port of the JavaScript hashids implementation.
It generates YouTube-like hashes from one or many numbers.
Use hashids when you do not want to expose your database ids to the user.}


%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}


%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p 1 -n hashids-python-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files hashids


%check
%{pytest}


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGELOG.md
%license LICENSE


%changelog
* Fri May 27 2022 Piotr Szubiakowski <pszubiak@eso.org> - 1.3.1-1
- Init