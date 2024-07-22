%define         cpp_version         1.16.1
%define         proto_version       1.3.2

Name:           opentelemetry-cpp
Version:        %{cpp_version}
Release:        2%{?dist}
Summary:        The C++ OpenTelemetry client
License:        ASL-2.0
URL:            https://opentelemetry.io
Source0:        https://github.com/open-telemetry/%{name}/archive/v%{cpp_version}/%{name}-%{cpp_version}.tar.gz
Patch0:         opentelemetry-cpp_use_shared_zlib.patch

BuildRequires:  cmake
BuildRequires:  g++
BuildRequires:  gcc
BuildRequires:  gmock-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  grpc-devel
BuildRequires:  gtest-devel
BuildRequires:  json-devel
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  thrift-devel
BuildRequires:  zlib-ng-compat-devel
BuildRequires:  zlib-ng-compat-static # To satisfy GRPC CMake 

%description
A language-specific implementation of OpenTelemetry in C++. OpenTelemetry is a collection of tools,
APIs, and SDKs. Use it to instrument, generate, collect, and export telemetry data
(metrics, logs, and traces) to help you analyze your software's performance and behavior.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} == %{version}-%{release}
Requires:       opentelemetry-proto-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n     opentelemetry-proto
Version:        %{proto_version}
Summary:        Protobuf definitions for the OpenTelemetry protocol (OTLP)
Source1:        https://github.com/open-telemetry/opentelemetry-proto/archive/v%{proto_version}/opentelemetry-proto-%{proto_version}.tar.gz


%description -n opentelemetry-proto
OpenTelemetry Protocol (OTLP) specification describes the encoding, transport,
and delivery mechanism of telemetry data between telemetry sources,
intermediate nodes such as collectors and telemetry backends.

OTLP is a general-purpose telemetry data delivery protocol designed
in the scope of OpenTelemetry project.


%package -n     opentelemetry-proto-devel
Version:        %{proto_version}
Summary:        Development files for opentelemetry-proto
Requires:       opentelemetry-proto%{?_isa} == %{proto_version}-%{release}


%description -n opentelemetry-proto-devel
The opentelemetry-proto-devel package contains libraries and header files for
developing applications that use opentelemetry-proto.


%prep
%autosetup -p 1 -n %{name}-%{cpp_version}
%autosetup -N -T -D -a1


%build
%cmake\
 -DWITH_OTLP_GRPC=ON\
 -DWITH_OTLP_HTTP=ON\
 -DBUILD_SHARED_LIBS=ON\
 -DWITH_BENCHMARK=OFF\
 -DWITH_STL=ON\
 -DOTELCPP_VERSIONED_LIBS=ON\
 -DOTELCPP_PROTO_PATH=opentelemetry-proto-%{proto_version}

%cmake_build


%install
%cmake_install


%check
%ctest


%files
%{_libdir}/libopentelemetry_common.so.1*
%{_libdir}/libopentelemetry_exporter_*.so.1*
%{_libdir}/libopentelemetry_metrics.so.1*
%{_libdir}/libopentelemetry_otlp_recordable.so.1*
%{_libdir}/libopentelemetry_resources.so.1*
%{_libdir}/libopentelemetry_trace.so.1*
%{_libdir}/libopentelemetry_version.so.1*
%{_libdir}/libopentelemetry_http_client_curl.so.1*
%{_libdir}/libopentelemetry_logs.so.1*

%doc README.md CHANGELOG.md
%license LICENSE


%files devel
%{_includedir}/opentelemetry/*.h
%{_includedir}/opentelemetry/baggage
%{_includedir}/opentelemetry/common
%{_includedir}/opentelemetry/context
%{_includedir}/opentelemetry/detail
%{_includedir}/opentelemetry/exporters
%{_includedir}/opentelemetry/ext
%{_includedir}/opentelemetry/logs
%{_includedir}/opentelemetry/metrics
%{_includedir}/opentelemetry/nostd
%{_includedir}/opentelemetry/plugin
%{_includedir}/opentelemetry/sdk
%{_includedir}/opentelemetry/std
%{_includedir}/opentelemetry/trace
%{_libdir}/libopentelemetry_common.so
%{_libdir}/libopentelemetry_exporter_*.so
%{_libdir}/libopentelemetry_metrics.so
%{_libdir}/libopentelemetry_otlp_recordable.so
%{_libdir}/libopentelemetry_resources.so
%{_libdir}/libopentelemetry_trace.so
%{_libdir}/libopentelemetry_version.so
%{_libdir}/libopentelemetry_http_client_curl.so
%{_libdir}/libopentelemetry_logs.so
%{_libdir}/cmake
%{_libdir}/pkgconfig


%files -n opentelemetry-proto
%{_libdir}/libopentelemetry_proto*.so


%files -n opentelemetry-proto-devel
%{_includedir}/opentelemetry/proto


%changelog
* Mon Jul 15 2024 Piotr Szubiakowski <pszubiak@eso.org> - 1.16.1, proto-version 1.3.2
- Init
