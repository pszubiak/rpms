Name:           libppconsul
Version:        0.2.3
Release:        1%{?dist}
Summary:        A C++ client library for Consul
License:        BSL-1.0
URL:            https://github.com/oliora/ppconsul
Source0:        %{url}/archive/v%{version}/ppconsul-v%{version}.tar.gz
Patch0:         ppconsul_cmake_install_path.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  libcurl-devel


%description
A C++ client library for Consul. Consul is a distributed tool for 
discovering and configuring services in your infrastructure.

The goal of Ppconsul is to:
* Fully cover version 1 of Consul HTTP API. Please check the current implementation status.
* Provide simple, modular and effective API based on C++11.
* Support different platforms. At the moment, Linux, Windows and macOS platforms supported.
* Cover all the code with automated tests.

Note that this project is under development and doesn't promise a stable interface.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} == %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup - -p 1 -n ppconsul-%{version}


%build
%cmake -DBUILD_TESTS=OFF
%cmake_build


%install
%cmake_install


%check


%files
%doc README.md
%license LICENSE_1_0.txt
%{_libdir}/libppconsul.so
%{_libdir}/libppconsul.so.0.1


%files devel
%{_includedir}
%{_libdir}/pkgconfig
%{_libdir}/cmake


%changelog
* Fri Nov 11 2022 Piotr Szubiakowski <pszubiak@eso.org> - 0.2.3-1
- Init
