%global bubblewrap_version 0.4.0
%global ostree_version 2020.8

Name:           flatpak
Version:        1.12.7
Release:        2%{?dist}
Summary:        Application deployment framework for desktop apps

License:        LGPLv2+
URL:            http://flatpak.org/
Source0:        https://github.com/flatpak/flatpak/releases/download/%{version}/%{name}-%{version}.tar.xz

%if 0%{?fedora}
# Add Fedora flatpak repositories
Source1:        flatpak-add-fedora-repos.service
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1935508
Patch0:         flatpak-dir-Use-SHA256-not-SHA1-to-name-the-cache-for-a-filt.patch

BuildRequires:  pkgconfig(appstream-glib)
BuildRequires:  pkgconfig(dconf)
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.40.0
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libarchive) >= 2.8.0
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libxml-2.0) >= 2.4
BuildRequires:  pkgconfig(libzstd) >= 0.8.1
BuildRequires:  pkgconfig(ostree-1) >= %{ostree_version}
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(xau)
BuildRequires:  bison
BuildRequires:  bubblewrap >= %{bubblewrap_version}
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  gettext
BuildRequires:  gpgme-devel
BuildRequires:  libcap-devel
BuildRequires:  python3-pyparsing
BuildRequires:  systemd
BuildRequires:  /usr/bin/xdg-dbus-proxy
BuildRequires:  /usr/bin/xmlto
BuildRequires:  /usr/bin/xsltproc

Requires:       bubblewrap >= %{bubblewrap_version}
Requires:       librsvg2%{?_isa}
Requires:       ostree-libs%{?_isa} >= %{ostree_version}
Requires:       /usr/bin/xdg-dbus-proxy
# https://fedoraproject.org/wiki/SELinux/IndependentPolicy
Requires:       (flatpak-selinux = %{?epoch:%{epoch}:}%{version}-%{release} if selinux-policy-targeted)
Requires:       %{name}-session-helper%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends:     p11-kit-server

# Make sure the document portal is installed
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:     xdg-desktop-portal > 0.10
%else
Requires:       xdg-desktop-portal > 0.10
%endif

%description
flatpak is a system for building, distributing and running sandboxed desktop
applications on Linux. See https://wiki.gnome.org/Projects/SandboxedApps for
more information.

%package devel
Summary:        Development files for %{name}
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the pkg-config file and development headers for %{name}.

%package libs
Summary:        Libraries for %{name}
License:        LGPLv2+
Requires:       bubblewrap >= %{bubblewrap_version}
Requires:       ostree%{?_isa} >= %{ostree_version}
Requires(pre):  /usr/sbin/useradd

%description libs
This package contains libflatpak.

%package selinux
Summary:        SELinux policy module for %{name}
License:        LGPLv2+
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
BuildRequires:  make
BuildArch:      noarch
%{?selinux_requires}

%description selinux
This package contains the SELinux policy module for %{name}.

%package session-helper
Summary:        User D-Bus service used by %{name} and others
License:        LGPLv2+
Conflicts:      flatpak < 1.4.1-2
Requires:       systemd

%description session-helper
This package contains the org.freedesktop.Flatpak user D-Bus service
that's used by %{name} and other packages.

%package tests
Summary:        Tests for %{name}
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-session-helper%{?_isa} = %{version}-%{release}
Requires:       bubblewrap >= %{bubblewrap_version}
Requires:       ostree%{?_isa} >= %{ostree_version}

%description tests
This package contains installed tests for %{name}.


%prep
%autosetup -p1


%build
# gobject introspection does not work with LTO.  There is an effort to fix this
# in the appropriate project upstreams, so hopefully LTO can be enabled someday
# Disable LTO.
%define _lto_cflags %{nil}

(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 # Generate consistent IDs between runs to avoid multilib problems.
 export XMLTO_FLAGS="--stringparam generate.consistent.ids=1"
 %configure \
            --enable-docbook-docs \
            --enable-installed-tests \
            --enable-selinux-module \
            --with-priv-mode=none \
            --with-system-bubblewrap \
            --with-system-dbus-proxy \
            $CONFIGFLAGS)
%make_build V=1


%install
%make_install
install -pm 644 NEWS README.md %{buildroot}/%{_pkgdocdir}
# The system repo is not installed by the flatpak build system.
install -d %{buildroot}%{_localstatedir}/lib/flatpak
install -d %{buildroot}%{_sysconfdir}/flatpak/remotes.d
rm -f %{buildroot}%{_libdir}/libflatpak.la

%if 0%{?fedora}
install -D -t %{buildroot}%{_unitdir} %{SOURCE1}
%endif

%find_lang %{name}

# Work around selinux denials, see
# https://github.com/flatpak/flatpak/issues/4128 for details. Note that we are
# going to need the system env generator if we should enable malcontent support
# in the future.
rm %{buildroot}%{_systemd_system_env_generator_dir}/60-flatpak-system-only

%pre
getent group flatpak >/dev/null || groupadd -r flatpak
getent passwd flatpak >/dev/null || \
    useradd -r -g flatpak -d / -s /sbin/nologin \
     -c "User for flatpak system helper" flatpak
exit 0


%if 0%{?fedora}
%post
%systemd_post flatpak-add-fedora-repos.service
%endif


%post selinux
%selinux_modules_install %{_datadir}/selinux/packages/flatpak.pp.bz2


%if 0%{?fedora}
%preun
%systemd_preun flatpak-add-fedora-repos.service
%endif


%if 0%{?fedora}
%postun
%systemd_postun_with_restart flatpak-add-fedora-repos.service
%endif


%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall %{_datadir}/selinux/packages/flatpak.pp.bz2
fi


%files -f %{name}.lang
%license COPYING
# Comply with the packaging guidelines about not mixing relative and absolute
# paths in doc.
%doc %{_pkgdocdir}
%{_bindir}/flatpak
%{_bindir}/flatpak-bisect
%{_bindir}/flatpak-coredumpctl
%{_datadir}/bash-completion
%{_datadir}/dbus-1/interfaces/org.freedesktop.portal.Flatpak.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Flatpak.Authenticator.xml
%{_datadir}/dbus-1/services/org.flatpak.Authenticator.Oci.service
%{_datadir}/dbus-1/services/org.freedesktop.portal.Flatpak.service
%{_datadir}/dbus-1/system-services/org.freedesktop.Flatpak.SystemHelper.service
%{_datadir}/fish/
%{_datadir}/%{name}
%{_datadir}/polkit-1/actions/org.freedesktop.Flatpak.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.Flatpak.rules
%{_datadir}/zsh/site-functions
%{_libexecdir}/flatpak-oci-authenticator
%{_libexecdir}/flatpak-portal
%{_libexecdir}/flatpak-system-helper
%{_libexecdir}/flatpak-validate-icon
%{_libexecdir}/revokefs-fuse
%dir %{_localstatedir}/lib/flatpak
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man5/%{name}-metadata.5*
%{_mandir}/man5/flatpak-flatpakref.5*
%{_mandir}/man5/flatpak-flatpakrepo.5*
%{_mandir}/man5/flatpak-installation.5*
%{_mandir}/man5/flatpak-remote.5*
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf
%dir %{_sysconfdir}/flatpak
%{_sysconfdir}/flatpak/remotes.d
%{_sysconfdir}/profile.d/flatpak.sh
%{_sysusersdir}/flatpak.conf
%{_unitdir}/flatpak-system-helper.service
%{_userunitdir}/flatpak-oci-authenticator.service
%{_userunitdir}/flatpak-portal.service
%{_systemd_user_env_generator_dir}/60-flatpak

%if 0%{?fedora}
%{_unitdir}/flatpak-add-fedora-repos.service
%endif

%files devel
%{_datadir}/gir-1.0/Flatpak-1.0.gir
%{_datadir}/gtk-doc/
%{_includedir}/%{name}/
%{_libdir}/libflatpak.so
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%license COPYING
%{_libdir}/girepository-1.0/Flatpak-1.0.typelib
%{_libdir}/libflatpak.so.*

%files selinux
%{_datadir}/selinux/packages/flatpak.pp.bz2
%{_datadir}/selinux/devel/include/contrib/flatpak.if

%files session-helper
%license COPYING
%{_datadir}/dbus-1/interfaces/org.freedesktop.Flatpak.xml
%{_datadir}/dbus-1/services/org.freedesktop.Flatpak.service
%{_libexecdir}/flatpak-session-helper
%{_userunitdir}/flatpak-session-helper.service

%files tests
%{_datadir}/installed-tests
%{_libexecdir}/installed-tests


%changelog
* Mon Jun 27 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.7-2
- Let flatpak own %%{_sysconfdir}/flatpak
Resolves: #2101456

* Thu Mar 17 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.7-1
- Update to 1.12.7
Resolves: #2058633

* Mon Mar 07 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.5-2
- Cope better with /var/lib/flatpak existing but being empty
Resolves: #2062806

* Sun Feb 20 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.5-1
- Update to 1.12.5
Resolves: #2054215

* Tue Feb 08 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.4-2
- Don't try to add Fedora's OCI Flatpak repository on RHEL
- Remove an obsolete Fedora-specific update path
Resolves: #2051697

* Mon Feb 07 2022 Neal Gompa <ngompa@centosproject.org> - 1.12.4-1
- Rebase to 1.12.4
Resolves: #2050302

* Thu Feb 03 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.10.7-2
- Use SHA256, not SHA1, to name the cache for a filtered remote
Resolves: #1935508

* Wed Feb 02 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.10.7-1
- Update to 1.10.7 (CVE-2021-43860)
Resolves: #2041973

* Tue Oct 26 2021 Debarshi Ray <rishi@fedoraproject.org> - 1.10.5-1
- Update to 1.10.5 (CVE-2021-41133)
Resolves: #2012862

* Wed Sep 22 2021 Debarshi Ray <rishi@fedoraproject.org> - 1.10.3-1
- Update to 1.10.3
Resolves: #2006554

* Sat Aug 28 2021 Debarshi Ray <rishi@fedoraproject.org> - 1.10.2-6
- Fix local deploys using system helper
Resolves: #1982304

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.10.2-5
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri May 07 2021 Kalev Lember <klember@redhat.com> - 1.10.2-4
- Disable system env generator to work around selinux denials (#1947214)

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 1.10.2-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Apr 05 2021 Kalev Lember <klember@redhat.com> - 1.10.2-2
- OCI: Switch to pax format for tar archives

* Wed Mar 10 2021 Kalev Lember <klember@redhat.com> - 1.10.2-1
- Update to 1.10.2

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.10.1-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Fri Feb 12 2021 Kalev Lember <klember@redhat.com> - 1.10.1-3
- Add G_BEGIN_DECLS/G_END_DECLS to public headers (#1927439)
- Drop unneeded ldconfig_scriptlets macro call

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Kalev Lember <klember@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Thu Jan 14 2021 Kalev Lember <klember@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Mon Jan 11 2021 Kalev Lember <klember@redhat.com> - 1.9.3-2
- Use "Fedora Flatpaks" as the visible repo name

* Tue Dec 22 2020 David King <amigadave@amigadave.com> - 1.9.3-1
- Update to 1.9.3 (#1910054)

* Fri Nov 20 2020 Kalev Lember <klember@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Thu Nov 19 2020 Kalev Lember <klember@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Wed Nov 18 2020 David King <amigadave@amigadave.com> - 1.8.3-2
- Drop obsolete Requires on system-release

* Tue Nov 17 2020 Kalev Lember <klember@redhat.com> - 1.8.3-1
- Update to 1.8.3

* Sat Oct 31 2020 Jeff Law <law@redhat.com> - 1.8.2-3
- Fix bogus volatiles caught by gcc-11

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 1.8.2-2
- Backport various OCI fixes from upstream

* Fri Aug 21 2020 Kalev Lember <klember@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 03 2020 David King <amigadave@amigadave.com> - 1.8.1-1
- Update to 1.8.1 (#1853667)

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 1.8.0-2
- Disable LTO

* Wed Jun 24 2020 David King <amigadave@amigadave.com> - 1.8.0-1
- Update to 1.8.0 (#1850676)

* Wed Jun 10 2020 David King <amigadave@amigadave.com> - 1.7.3-1
- Update to 1.7.3 (#1820762)

* Fri Apr 03 2020 Kalev Lember <klember@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Mon Mar 30 2020 David King <amigadave@amigadave.com> - 1.7.1-1
- Update to 1.7.1 (#1818882)

* Mon Mar 30 2020 Kalev Lember <klember@redhat.com> - 1.6.3-1
- Update to 1.6.3

* Thu Feb 13 2020 David King <amigadave@amigadave.com> - 1.6.2-1
- Update to 1.6.2 (#1802609)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 David King <amigadave@amigadave.com> - 1.6.1-1
- Update to 1.6.1

* Fri Jan 17 2020 David King <amigadave@amigadave.com> - 1.6.0-2
- Remove broken python3 sed hack

* Fri Dec 20 2019 David King <amigadave@amigadave.com> - 1.6.0-1
- Update to 1.6.0

* Mon Dec 16 2019 David King <amigadave@amigadave.com> - 1.5.2-1
- Update to 1.5.2

* Thu Nov 28 2019 David King <amigadave@amigadave.com> - 1.5.1-1
- Update to 1.5.1

* Fri Nov 01 2019 Orion Poplawski <orion@nwra.com> - 1.5.0-2
- Use %%{?selinux_requires} for proper install ordering

* Thu Oct 03 2019 David King <amigadave@amigadave.com> - 1.5.0-1
- Update to 1.5.0

* Thu Sep 19 2019 Kalev Lember <klember@redhat.com> - 1.4.3-1
- Update to 1.4.3

* Wed Sep 18 2019 Debarshi Ray <rishi@fedoraproject.org> - 1.4.2-6
- Trim unused shared library linkages from the session helper

* Wed Aug  7 2019 Owen Taylor <otaylor@redhat.com> - 1.4.2-5
- Add patch fixing problem with downloading icons for OCI remotes (#1683375)

* Thu Jul 25 2019 Tim Zabel <tjzabel21@gmail.com> - 1.4.2-4
- SELinux needs additional Requires (#1732132)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Kalev Lember <klember@redhat.com> - 1.4.2-2
- Backport a patch that fixes a fairly large memory leak in gnome-software

* Fri Jun 28 2019 David King <amigadave@amigadave.com> - 1.4.2-1
- Update to 1.4.2 (#1725071)

* Tue Jun 25 2019 David King <amigadave@amigadave.com> - 1.4.1-3
- Use Requires(post) for selinux-policy (#1723118)

* Tue Jun 25 2019 Debarshi Ray <rishi@fedoraproject.org> - 1.4.1-2
- Split the session helper into a separate sub-package

* Thu Jun 13 2019 Kalev Lember <klember@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Wed Jun 12 2019 Kalev Lember <klember@redhat.com> - 1.4.0-2
- Backport an upstream patch to fix gnome-software CI

* Tue May 28 2019 Kalev Lember <klember@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Fri May 10 2019 Kalev Lember <klember@redhat.com> - 1.3.4-1
- Update to 1.3.4

* Tue Apr 30 2019 David King <amigadave@amigadave.com> - 1.3.3-2
- Generate consistent anchor IDs

* Fri Apr 26 2019 David King <amigadave@amigadave.com> - 1.3.3-1
- Update to 1.3.3 (#1699338)

* Wed Apr 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.2-2
- Fixup selinux requires

* Fri Apr 12 2019 David King <amigadave@amigadave.com> - 1.3.2-1
- Update to 1.3.2 (#1699338)

* Wed Apr 03 2019 Kalev Lember <klember@redhat.com> - 1.3.1-2
- Add a oneshot systemd service to add Fedora flatpak repos
- Remove the post script to create system repo now that we have the service

* Wed Mar 27 2019 David King <amigadave@amigadave.com> - 1.3.1-1
- Update to 1.3.1 (#1693207)

* Tue Mar 12 2019 David King <amigadave@amigadave.com> - 1.3.0-1
- Update to 1.3.0

* Thu Feb 14 2019 David King <amigadave@amigadave.com> - 1.2.3-2
- Remove an obsolete Conflicts
- Use xdg-dbus-proxy

* Mon Feb 11 2019 David King <amigadave@amigadave.com> - 1.2.3-1
- Update to 1.2.3

* Wed Feb 06 2019 David King <amigadave@amigadave.com> - 1.2.2-1
- Update to 1.2.2

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Mon Feb  4 2019 fedora-toolbox <otaylor@redhat.com> - 1.2.0-4
- Add an upstream patch to add flatpak build-export --disable-sandbox

* Thu Jan 31 2019 Bastien Nocera <bnocera@redhat.com> - 1.2.0-3
- Require librsvg2 so SVG icons can be exported

* Tue Jan 29 2019 Kalev Lember <klember@redhat.com> - 1.2.0-2
- Enable libsystemd support

* Mon Jan 28 2019 David King <amigadave@amigadave.com> - 1.2.0-1
- Update to 1.2.0

* Tue Jan 15 2019 Kalev Lember <klember@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Fri Dec 21 2018 David King <amigadave@amigadave.com> - 1.1.2-1
- Update to 1.1.2

* Mon Dec 17 2018 David King <amigadave@amigadave.com> - 1.1.1-2
- Enable installed tests and add to tests subpackage

* Mon Dec 10 2018 Kalev Lember <klember@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Fri Nov 30 2018 fedora-toolbox <otaylor@redhat.com> - 1.0.6-3
- Add a patch to fix OCI system remotes
- Add patch fixing permissions on icons downloaded from an OCI registry

* Fri Nov 16 2018 Kalev Lember <klember@redhat.com> - 1.0.6-1
- Update to 1.0.6

* Mon Nov 12 2018 Kalev Lember <klember@redhat.com> - 1.0.5-2
- Recommend p11-kit-server instead of just p11-kit (#1649049)

* Mon Nov 12 2018 Kalev Lember <klember@redhat.com> - 1.0.5-1
- Update to 1.0.5

* Fri Oct 12 2018 Kalev Lember <klember@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Thu Oct 04 2018 Kalev Lember <klember@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Thu Sep 13 2018 Kalev Lember <klember@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Tue Aug 28 2018 David King <amigadave@amigadave.com> - 1.0.1-1
- Update to 1.0.1

* Mon Aug 20 2018 David King <amigadave@amigadave.com> - 1.0.0-2
- Fix double dash in XML documentation

* Mon Aug 20 2018 David King <amigadave@amigadave.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Kalev Lember <klember@redhat.com> - 0.99.3-1
- Update to 0.99.3

* Wed Jun 27 2018 Kalev Lember <klember@redhat.com> - 0.99.2-1
- Update to 0.99.2

* Thu Jun 21 2018 David King <amigadave@amigadave.com> - 0.99.1-1
- Update to 0.99.1

* Wed Jun 13 2018 David King <amigadave@amigadave.com> - 0.11.8.3-1
- Update to 0.11.8.3 (#1590808)

* Mon Jun 11 2018 David King <amigadave@amigadave.com> - 0.11.8.2-1
- Update to 0.11.8.2 (#1589810)

* Fri Jun 08 2018 David King <amigadave@amigadave.com> - 0.11.8.1-1
- Update to 0.11.8.1 (#1588868)

* Fri Jun 08 2018 David King <amigadave@amigadave.com> - 0.11.8-1
- Update to 0.11.8 (#1588868)

* Wed May 23 2018 Adam Jackson <ajax@redhat.com> - 0.11.7-2
- Remove Requires: kernel >= 4.0.4-202, which corresponds to rawhide
  somewhere before Fedora 22 which this spec file certainly no longer
  supports.

* Thu May 03 2018 Kalev Lember <klember@redhat.com> - 0.11.7-1
- Update to 0.11.7

* Wed May 02 2018 Kalev Lember <klember@redhat.com> - 0.11.6-1
- Update to 0.11.6

* Wed May 02 2018 Kalev Lember <klember@redhat.com> - 0.11.5-2
- Backport a fix for a gnome-software crash installing .flatpakref files

* Mon Apr 30 2018 David King <amigadave@amigadave.com> - 0.11.5-1
- Update to 0.11.5

* Thu Apr 26 2018 Kalev Lember <klember@redhat.com> - 0.11.4-1
- Update to 0.11.4

* Mon Feb 19 2018 David King <amigadave@amigadave.com> - 0.11.3-1
- Update to 0.11.3

* Mon Feb 19 2018 David King <amigadave@amigadave.com> - 0.11.2-1
- Update to 0.11.2

* Wed Feb 14 2018 David King <amigadave@amigadave.com> - 0.11.1-1
- Update to 0.11.1 (#1545224)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10.3-2
- Switch to %%ldconfig_scriptlets

* Tue Jan 30 2018 Kalev Lember <klember@redhat.com> - 0.10.3-1
- Update to 0.10.3

* Thu Dec 21 2017 David King <amigadave@amigadave.com> - 0.10.2.1-1
- Update to 0.10.2.1

* Fri Dec 15 2017 Kalev Lember <klember@redhat.com> - 0.10.2-1
- Update to 0.10.2

* Fri Nov 24 2017 David King <amigadave@amigadave.com> - 0.10.1-1
- Update to 0.10.1

* Thu Oct 26 2017 Kalev Lember <klember@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Mon Oct 09 2017 Kalev Lember <klember@redhat.com> - 0.9.99-1
- Update to 0.9.99

* Tue Sep 26 2017 Kalev Lember <klember@redhat.com> - 0.9.98.2-1
- Update to 0.9.98.2

* Tue Sep 26 2017 Kalev Lember <klember@redhat.com> - 0.9.98.1-1
- Update to 0.9.98.1

* Mon Sep 25 2017 Kalev Lember <klember@redhat.com> - 0.9.98-1
- Update to 0.9.98

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 0.9.12-1
- Update to 0.9.12

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 0.9.11-1
- Update to 0.9.11

* Mon Sep 04 2017 Kalev Lember <klember@redhat.com> - 0.9.10-1
- Update to 0.9.10
- Split out flatpak-builder to a separate source package

* Fri Aug 25 2017 Kalev Lember <klember@redhat.com> - 0.9.8-2
- Backport a patch to fix regression in --devel

* Mon Aug 21 2017 David King <amigadave@amigadave.com> - 0.9.8-1
- Update to 0.9.8

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 0.9.7-4
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Owen Taylor <otaylor@redhat.com> - 0.9.7-3
- Add a patch to fix OCI refname annotation

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 01 2017 David King <amigadave@amigadave.com> - 0.9.7-1
- Update to 0.9.7 (#1466970)

* Tue Jun 20 2017 David King <amigadave@amigadave.com> - 0.9.6-1
- Update to 0.9.6

* Sat Jun 10 2017 David King <amigadave@amigadave.com> - 0.9.5-1
- Update to 0.9.5 (#1460437)

* Tue May 23 2017 David King <amigadave@amigadave.com> - 0.9.4-1
- Update to 0.9.4 (#1454750)

* Mon Apr 24 2017 David King <amigadave@amigadave.com> - 0.9.3-1
- Update to 0.9.3

* Fri Apr 07 2017 David King <amigadave@amigadave.com> - 0.9.2-2
- Add eu-strip dependency for flatpak-builder

* Wed Apr 05 2017 Kalev Lember <klember@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Wed Mar 15 2017 Kalev Lember <klember@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Fri Mar 10 2017 Kalev Lember <klember@redhat.com> - 0.8.4-1
- Update to 0.8.4

* Sun Feb 19 2017 David King <amigadave@amigadave.com> - 0.8.3-3
- Make flatpak-builder require bzip2 (#1424857)

* Wed Feb 15 2017 Kalev Lember <klember@redhat.com> - 0.8.3-2
- Avoid pulling in all of ostree and only depend on ostree-libs subpackage

* Tue Feb 14 2017 Kalev Lember <klember@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Kalev Lember <klember@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Wed Jan 18 2017 David King <amigadave@amigadave.com> - 0.8.1-1
- Update to 0.8.1

* Tue Dec 20 2016 Kalev Lember <klember@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Tue Nov 29 2016 David King <amigadave@amigadave.com> - 0.6.14-2
- Add a patch to fix a GNOME Software crash
- Silence repository listing during post

* Tue Nov 29 2016 Kalev Lember <klember@redhat.com> - 0.6.14-1
- Update to 0.6.14

* Wed Oct 26 2016 David King <amigadave@amigadave.com> - 0.6.13-2
- Add empty /etc/flatpak/remotes.d

* Tue Oct 25 2016 David King <amigadave@amigadave.com> - 0.6.13-1
- Update to 0.6.13

* Thu Oct 06 2016 David King <amigadave@amigadave.com> - 0.6.12-1
- Update to 0.6.12

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com> - 0.6.11-1
- Update to 0.6.11
- Set minimum ostree and bubblewrap versions

* Mon Sep 12 2016 David King <amigadave@amigadave.com> - 0.6.10-1
- Update to 0.6.10

* Tue Sep 06 2016 David King <amigadave@amigadave.com> - 0.6.9-2
- Look for bwrap in PATH

* Thu Aug 25 2016 David King <amigadave@amigadave.com> - 0.6.9-1
- Update to 0.6.9

* Mon Aug 01 2016 David King <amigadave@amigadave.com> - 0.6.8-1
- Update to 0.6.8 (#1361823)

* Thu Jul 21 2016 David King <amigadave@amigadave.com> - 0.6.7-2
- Use system bubblewrap

* Fri Jul 01 2016 David King <amigadave@amigadave.com> - 0.6.7-1
- Update to 0.6.7

* Thu Jun 23 2016 David King <amigadave@amigadave.com> - 0.6.6-1
- Update to 0.6.6

* Fri Jun 10 2016 David King <amigadave@amigadave.com> - 0.6.5-1
- Update to 0.6.5

* Wed Jun 01 2016 David King <amigadave@amigadave.com> - 0.6.4-1
- Update to 0.6.4

* Tue May 31 2016 David King <amigadave@amigadave.com> - 0.6.3-1
- Update to 0.6.3
- Move bwrap to main package

* Tue May 24 2016 David King <amigadave@amigadave.com> - 0.6.2-1
- Rename from xdg-app to flatpak (#1337434)
