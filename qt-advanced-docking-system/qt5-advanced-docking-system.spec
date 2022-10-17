Name:           qt5-advanced-docking-system
Version:        3.8.3
Release:        1%{?dist}
Summary:        Qt5 - Advanced Docking System
License:        LGPL-2.1
URL:            https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System
Source0:        ${url}/%{name}/archive/%{version}/qt-advanced-docking-system-%{version}.tar.gz
Patch0:         qt-advanced-docking-system-lib64.patch

BuildRequires:  cmake
BuildRequires:  g++
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-private-devel

# TODO creation of debuginfo package doesn't work
%global         debug_package   %{nil}

%description
Qt Advanced Docking System lets you create customizable layouts using a full
featured window docking system similar to what is found in many popular
integrated development environments (IDEs) such as Visual Studio.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} == %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p 1 -n Qt-Advanced-Docking-System-%{version}


%build
cmake -DADS_VERSION=%{version} -DBUILD_EXAMPLES=off -DCMAKE_INSTALL_PREFIX=%{_prefix}
make


%install
make DESTDIR=%{buildroot} install


%files
%doc README.md
%license LICENSE
%{_libdir}/libqtadvanceddocking.so*
%{_datadir}/licenses/ads

%files devel
%{_includedir}
%{_libdir}/cmake


%changelog
* Fri Oct 14 2022 Piotr Szubiakowski <pszubiak@eso.org> - 3.8.3-1
- Init
