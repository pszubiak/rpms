Name:           nix
Version:        2.11.1
Release:        1%{?dist}
Summary:        Nix is a purely functional package manager

License:        LGPLv2+
URL:            https://nixos.org/nix
Source0:        https://github.com/NixOS/nix/archive/%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  aws-sdk-cpp-devel
BuildRequires:  bison
BuildRequires:  busybox
BuildRequires:  chrpath
BuildRequires:  boost-devel
BuildRequires:  brotli-devel
BuildRequires:  bzip2-devel
BuildRequires:  editline-devel
BuildRequires:  flex
BuildRequires:  gc-devel
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  gmock-devel
BuildRequires:  json-devel
BuildRequires:  jq
BuildRequires:  libarchive-devel
BuildRequires:  libcpuid-devel
BuildRequires:  libcurl-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libsodium-devel
BuildRequires:  lowdown-devel
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel
BuildRequires:  xz-devel

Requires:       busybox


%description
Nix is a powerful package manager for Linux and other Unix systems
that makes package management reliable and reproducible.
Please refer to the Nix manual for more details.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}


%build
%undefine _hardened_build

./bootstrap.sh
%configure --disable-doc-gen --localstatedir=/nix/var --with-sandbox-shell=/sbin/busybox
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install

# Create Nix store
mkdir -p %{buildroot}/nix/store

# Remove init scripts
rm -r %{buildroot}%{_sysconfdir}/init

# fix permission of nix profile
# (until this is fixed in the relevant Makefile)
chmod -x %{buildroot}%{_sysconfdir}/profile.d/nix.sh

# make per-user directories
for d in profiles gcroots;
do
  mkdir -p %{buildroot}/nix/var/nix/$d/per-user
  chmod 1777 %{buildroot}/nix/var/nix/$d/per-user
done
for i in db temproots ; do
  mkdir %{buildroot}/nix/var/nix/$i
done

# Remove RPATHs for check-rpaths
chrpath -d %{buildroot}/usr/bin/nix
chrpath -d %{buildroot}/usr/lib64/*.so

%check
make check


%pre
# Setup build group
if ! getent group "nixbld" >/dev/null; then
  groupadd -r "nixbld"
fi

# Setup build users
for i in $(seq 32); do
  if ! getent passwd "nixbld$i" >/dev/null; then
    useradd -r -g "nixbld" -G "nixbld" -d /var/empty \
      -s /sbin/nologin \
      -c "Nix build user $i" "nixbld$i"
  fi
done


%files
%{_bindir}/nix*
%{_libdir}/*.so
%{_libexecdir}/nix
%{_prefix}/lib/*
%config(noreplace) %{_sysconfdir}/*
%{_datadir}/*
%dir /nix
%attr(1775,root,nixbld) /nix/store
%dir /nix/var
%dir %attr(775,root,nixbld) /nix/var/nix
%ghost /nix/var/nix/daemon-socket/socket
%attr(775,root,nixbld) /nix/var/nix/temproots
%attr(775,root,nixbld) /nix/var/nix/db

%files devel
%{_includedir}/nix
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Jul 26 2022 Piotr Szubiakowski - 2.10.3-1
- update

* Thu Oct 14 2021 Piotr Szubiakowski - 2.4.0~pre.rc1-1
- update

* Thu Aug 19 2021 Piotr Szubiakowski - 2.4.0~1.g2cd1a5b8-2
- make busybox a runtime dependency
- remove init files
- crete /nix/var structure

* Fri Aug 13 2021 Piotr Szubiakowski - 2.4.0~1.g2cd1a5b8-1
- adjust upstream spec file
