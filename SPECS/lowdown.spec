Name:           lowdown
Version:        0.9.2
Release:        1%{?dist}
Summary:        Simple markdown translator
License:        ICS
URL:            https://kristaps.bsd.lv/lowdown/
%undefine       _disable_source_fetch
Source0:        https://github.com/kristapsdz/lowdown/archive/refs/tags/VERSION_0_9_2.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  coreutils

%description
lowdown is a Markdown translator producing HTML5,
roff documents in the ms and man formats, LaTeX,
gemini, and terminal output.
The open source C source code has no dependencies.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
For details about the programming API, please see the docs
on the project's site (https://kristaps.bsd.lv/lowdown/)

%prep
echo "%SHA256SUM0  %SOURCE0" | sha256sum -c -
%setup -n %{name}-VERSION_0_9_2

%build
export CFLAGS='%{build_cflags} -fPIC'
export LDFLAGS='%{build_ldflags}'
./configure PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir}
%make_build

%install
%make_install
chmod -R u+w $RPM_BUILD_ROOT

%ldconfig_scriptlets

%files
%{_bindir}/%{name}*
%{_libdir}/*.a
%{_mandir}/man1/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_mandir}/man5/*

%changelog
* Fri Oct 15 2021 Piotr Szubiakowski - 0.9.2-1
- update to v9.2

* Thu Feb 12 2021 Piotr Szubiakowski - 0.8.6-2
- add -fPIC flag

* Thu Feb 12 2021 Piotr Szubiakowski - 0.8.6-1
- init
