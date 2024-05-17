Name:           xdg-dbus-proxy
Version:        0.1.3
Release:        1%{?dist}
Summary:        Filtering proxy for D-Bus connections

License:        LGPLv2+
URL:            https://github.com/flatpak/xdg-dbus-proxy/
Source0:        https://github.com/flatpak/xdg-dbus-proxy/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: make
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  /usr/bin/xsltproc

Requires:       dbus

%description
xdg-dbus-proxy is a filtering proxy for D-Bus connections. It was originally
part of the flatpak project, but it has been broken out as a standalone module
to facilitate using it in other contexts.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/xdg-dbus-proxy
%{_mandir}/man1/xdg-dbus-proxy.1*

%changelog
* Tue Mar 22 2022 Debarshi Ray <rishi@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3
Resolves: #2060089

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 0.1.2-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.1.2-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Kalev Lember <klember@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Kalev Lember <klember@redhat.com> - 0.1.1-1
- Update to 0.1.1
- Build man pages
- Include COPYING file as license

* Fri Nov 23 2018 Kalev Lember <klember@redhat.com> - 0.1.0-1
- Initial Fedora packaging
