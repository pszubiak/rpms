# Even though this package does not install any ELF files, it does compute
# pointer sizes.  Therefore, this package cannot be noarch, but it also does
# not produce any debug information.
%global debug_package %{nil}

Name:           cli11
Version:        1.9.1
Release:        4%{?dist}.eso.1
Summary:        Command line parser for C++11

License:        BSD
URL:            https://github.com/CLIUtils/CLI11
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Use the system gmock/gtest instead of requiring that they be downloaded
Patch0:         %{name}-gtest.patch
Patch1:         %{name}-pkg-config.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  python3-devel

%description
CLI11 is a command line parser for C++11 and beyond that provides a
rich feature set with a simple and intuitive interface.

%package devel
Summary:        Command line parser for C++11
Provides:       %{name}-static = %{version}-%{release}

%description devel
CLI11 is a command line parser for C++11 and beyond that provides a
rich feature set with a simple and intuitive interface.

%package        docs
Summary:        Documentation for CLI11
BuildArch:      noarch

%description    docs
Documentation for CLI11.

%prep
%setup -n CLI11-%{version}
%patch0 -p0
%patch1 -p1


%build
%cmake -DCLI11_BUILD_DOCS:BOOL=TRUE -DCLI11_BUILD_TESTS:BOOL=TRUE
%cmake_build

# Build the documentation
%cmake_build --target docs

%install
%cmake_install

%check
%ctest

%files devel
%doc CHANGELOG.md README.md
%license LICENSE
%{_includedir}/CLI/
%{_libdir}/pkgconfig/CLI11.pc
%{_libdir}/cmake/CLI11/

%files docs
%doc %{_vpath_builddir}/docs/html
%doc docs/CLI11.svg docs/CLI11_100.png docs/CLI11_300.png

%changelog
* Mon Sep 12 2022 Piotr Szubiakowski <pszubiak@eso.org> - 1.9.1-4.fc34.eso.1
- Add pkg-config patch

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jerry James <loganjerry@gmail.com> - 1.9.1-2
- Adapt to cmake changes in Rawhide

* Sun Jun 21 2020 Jerry James <loganjerry@gmail.com> - 1.9.1-1
- Version 1.9.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Jerry James <loganjerry@gmail.com> - 1.9.0-1
- Version 1.9.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun  8 2019 Jerry James <loganjerry@gmail.com> - 1.8.0-1
- Initial RPM
