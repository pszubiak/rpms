Name:           opentelemetry-cpp
Version:        1.6.0
Release:        2%{?dist}
Summary:        The C++ OpenTelemetry client
License:        ASL-2.0
URL:            https://opentelemetry.io/
Source:         https://github.com/open-telemetry/opentelemetry-cpp/archive/refs/tags/v%{version}.tar.gz
Patch0:         disable_problematic_utests.patch

BuildRequires:  cmake
BuildRequires:  libcurl-devel
BuildRequires:  gcc
BuildRequires:  gmock-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  grpc-devel
BuildRequires:  gtest-devel
BuildRequires:  g++


%description
A language-specific implementation of OpenTelemetry in C++. OpenTelemetry is a collection of tools,
APIs, and SDKs. Use it to instrument, generate, collect, and export telemetry data 
(metrics, logs, and traces) to help you analyze your software's performance and behavior.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p 1 -n %{name}-%{version}


%build
%cmake -DWITH_OTLP=ON -DWITH_JAEGER=ON -DUSE_SYSTEM_GRPC=ON
%cmake_build


%install
%cmake_install


%check
%ctest

%files
%{_libdir}/*.so

%doc README.md CHANGELOG.md
%license LICENSE


%files devel
%{_includedir}/opentelemetry
%{_libdir}/cmake

%changelog
* Wed Aug 17 2022 Piotr Szubiakowski <pszubiak@eso.org> - 1.6.0-1
- Init
