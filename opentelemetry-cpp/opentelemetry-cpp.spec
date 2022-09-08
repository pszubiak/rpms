%define         cpp_version         1.6.0
%define         proto_version       0.18.0

Name:           opentelemetry-cpp
Version:        %{cpp_version}
Release:        3%{?dist}
Summary:        The C++ OpenTelemetry client
License:        ASL-2.0
URL:            https://opentelemetry.io
Source0:        https://github.com/open-telemetry/%{name}/archive/v%{cpp_version}/%{name}-%{cpp_version}.tar.gz
Source2:        opentelemetry_api.pc
Source3:        opentelemetry_sdk.pc
Patch0:         disable_curl_utests.patch
Patch1:         cmake_adapt_to_shared_libraries.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gmock-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  grpc-devel
BuildRequires:  gtest-devel
BuildRequires:  g++
BuildRequires:  json-devel
BuildRequires:  libcurl-devel
BuildRequires:  thrift-devel

Requires:       opentelemetry-proto


%description
A language-specific implementation of OpenTelemetry in C++. OpenTelemetry is a collection of tools,
APIs, and SDKs. Use it to instrument, generate, collect, and export telemetry data 
(metrics, logs, and traces) to help you analyze your software's performance and behavior.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} == %{version}-%{release}


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
Summary:        Development files for opentelemetry-proto
Requires:       opentelemetry-proto%{?_isa} == %{proto_version}-%{release}


%description -n opentelemetry-proto-devel
The opentelemetry-proto-devel package contains libraries and header files for
developing applications that use opentelemetry-proto.


%prep
%setup -T -a 1 -n %{name}-%{cpp_version}/third_party -c
%autosetup -D -p 1 -n %{name}-%{cpp_version}
# Replace Git submodule with SOURCE1
rmdir third_party/opentelemetry-proto
ln -rs ./third_party/opentelemetry-proto-%{proto_version} ./third_party/opentelemetry-proto
# Trick CMake to treat SOURCE1 as Git submodule
mkdir third_party/opentelemetry-proto/.git


%build
%cmake -DWITH_OTLP=ON -DWITH_JAEGER=ON
%cmake_build


%install
%cmake_install

# Install pkg-config files
install -p -D -m644 %{SOURCE2} -t %{buildroot}/usr/lib64/pkgconfig/
install -p -D -m644 %{SOURCE3} -t %{buildroot}/usr/lib64/pkgconfig/


%check
%ctest


%files
%{_libdir}/libhttp_client_nosend.so
%{_libdir}/libopentelemetry_common.so
%{_libdir}/libopentelemetry_exporter_*.so
%{_libdir}/libopentelemetry_http_client_curl.so
%{_libdir}/libopentelemetry_metrics.so
%{_libdir}/libopentelemetry_otlp_recordable.so
%{_libdir}/libopentelemetry_resources.so
%{_libdir}/libopentelemetry_trace.so
%{_libdir}/libopentelemetry_version.so


%doc README.md CHANGELOG.md
%license LICENSE


%files devel
%{_includedir}/opentelemetry/*.h
%{_includedir}/opentelemetry/_metrics
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
%{_libdir}/cmake
%{_libdir}/pkgconfig


%files -n opentelemetry-proto
%{_libdir}/libopentelemetry_proto.so


%files -n opentelemetry-proto-devel
%{_includedir}/opentelemetry/proto


%changelog
* Thu Sep 08 2022 Piotr Szubiakowski <pszubiak@eso.org> - 1.6.0-3
- Add API and SDK pkg-config files

* Wed Sep 07 2022 Piotr Szubiakowski <pszubiak@eso.org> - 1.6.0-2
- Switch build to shared libraries
- Add opentelemetry-proto
- Add -DWITH_OTLP=ON -DWITH_JAEGER=ON flags

* Wed Aug 17 2022 Piotr Szubiakowski <pszubiak@eso.org> - 1.6.0-1
- Init
