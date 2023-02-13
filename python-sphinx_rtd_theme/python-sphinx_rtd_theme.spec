%global srcname sphinx_rtd_theme

# Disables tests and docs
%bcond_with bootstrap

Name:           python-%{srcname}
Version:        0.5.1
Release:        2%{?dist}.eso.1
Summary:        Sphinx theme for readthedocs.org

License:        MIT
URL:            https://github.com/rtfd/%{srcname}
Source0:        https://github.com/rtfd/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz
# The koji builders do not have network access, and this file is not included
# in any Fedora package, so we retrieve it for offline use.
Source1:        https://docs.readthedocs.io/en/latest/objects.inv
# Remove all traces of html5shiv.  We have no interest in supporting ancient
# versions of Internet Explorer.
Patch0:         %{name}-html5shiv.patch

BuildArch:      noarch

BuildRequires:  font(fontawesome)
BuildRequires:  font(lato)
BuildRequires:  font(robotoslab)
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  %{py3_dist docutils}
BuildRequires:  %{py3_dist readthedocs-sphinx-ext}
BuildRequires:  %{py3_dist setuptools}
%if %{without bootstrap}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinxcontrib-httpdomain}
BuildRequires:  python-sphinx-doc
%endif

%description
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Sphinx theme for readthedocs.org
Requires:       font(fontawesome)
Requires:       font(lato)
Requires:       font(robotoslab)

%description -n python%{python3_pkgversion}-%{srcname}
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.

%if %{without bootstrap}
%package doc
Summary:        Documentation for the Sphinx theme for readthedocs.org
Requires:       font(fontawesome)
Requires:       font(lato)
Requires:       font(robotoslab)

%description doc
This package contains documentation for the Sphinx theme for
readthedocs.org.
%endif

%prep
%autosetup -p0 -n %{srcname}-%{version}

# Use local objects.inv for intersphinx
sed -e "s|\('https://docs\.readthedocs\.io/en/latest/', \)None|\1'%{SOURCE1}'|" \
    -e "s|\('http://www\.sphinx-doc\.org/en/stable/', \)None|\1'%{_docdir}/python-sphinx-doc/html/objects.inv'|" \
    -i docs/conf.py

# We cannot build the Javascript from source at this time, due to many missing
# dependencies.  Convince the build script to skip building the Javascript and
# go on to the python.
mkdir -p build/lib/%{srcname}/static/js
cp -p sphinx_rtd_theme/static/js/badge_only.js build/lib/%{srcname}/static/js
cp -p sphinx_rtd_theme/static/js/theme.js build/lib/%{srcname}/static/js
sed -i "/'build_py'/d" setup.py

%build
%py3_build

%if %{without bootstrap}
# Build the documentation
make -C docs html
%endif

rst2html --no-datestamp README.rst README.html

%install
%py3_install

%if %{without bootstrap}
rm docs/build/html/.buildinfo
%endif

%if %{without bootstrap}
%check
pytest
%endif

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.html
%license LICENSE OFL-License.txt
%{python3_sitelib}/%{srcname}-*.egg-info/
%dir %{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}/__pycache__/
%{python3_sitelib}/%{srcname}/static/
%{python3_sitelib}/%{srcname}/*.html
%{python3_sitelib}/%{srcname}/*.py
%{python3_sitelib}/%{srcname}/theme.conf
%dir %{python3_sitelib}/%{srcname}/locale/
%{python3_sitelib}/%{srcname}/locale/sphinx.pot
%lang(de) %{python3_sitelib}/%{srcname}/locale/de/
%lang(en) %{python3_sitelib}/%{srcname}/locale/en/
%lang(es) %{python3_sitelib}/%{srcname}/locale/es/
%lang(et) %{python3_sitelib}/%{srcname}/locale/et/
%lang(fr) %{python3_sitelib}/%{srcname}/locale/fr/
%lang(nl) %{python3_sitelib}/%{srcname}/locale/nl/
%lang(pt) %{python3_sitelib}/%{srcname}/locale/pt_BR/
%lang(ru) %{python3_sitelib}/%{srcname}/locale/ru/
%lang(sv) %{python3_sitelib}/%{srcname}/locale/sv/
%lang(tr) %{python3_sitelib}/%{srcname}/locale/tr/
%lang(zh) %{python3_sitelib}/%{srcname}/locale/zh_CN/

%if %{without bootstrap}
%files doc
%doc docs/build/html
%license LICENSE OFL-License.txt
%endif

%changelog
* Mon Feb 13 2023 Piotr Szubiakowski <pszubiak@eso.org> - 0.5.1-2.fc34.eso.1
- Bundle fonts again

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan  4 2021 Jerry James <loganjerry@gmail.com> - 0.5.1-1
- Version 0.5.1
- Do not list language files twice

* Thu Dec 10 2020 Jerry James <loganjerry@gmail.com> - 0.5.0-1
- Version 0.5.0
- Drop upstreamed -script patch
- Do not even link to fonts; modify the CSS to point to system fonts
- Remove all traces of html5shiv

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-13
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-12
- Bootstrap for Python 3.9

* Wed Mar 18 2020 Jerry James <loganjerry@gmail.com> - 0.4.3-11
- Fix symlinks to the Roboto fonts

* Tue Feb  4 2020 Jerry James <loganjerry@gmail.com> - 0.4.3-10
- BR readthedocs-sphinx-ext so the tests can be run

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Jerry James <loganjerry@gmail.com> - 0.4.3-8
- Add -doc subpackage

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-6
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-5
- Bootstrap for Python 3.8

* Tue Aug  6 2019 Jerry James <loganjerry@gmail.com> - 0.4.3-4
- Add -script patch to silence deprecation warnings

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-2
- Subpackage python2-sphinx_rtd_theme has been removed
  See https://fedoraproject.org/wiki/Changes/Sphinx2

* Tue Feb 12 2019 Jerry James <loganjerry@gmail.com> - 0.4.3-1
- New upstream version
- Use the github tarball, which has docs, instead of the pypi tarball
- Add %%check script

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 22 2018 Jerry James <loganjerry@gmail.com> - 0.4.2-1
- New upstream version

* Tue Jul 31 2018 Jerry James <loganjerry@gmail.com> - 0.4.1-1
- New upstream version

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  2 2018 Jerry James <loganjerry@gmail.com> - 0.4.0-1
- New upstream version

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-2
- Rebuilt for Python 3.7

* Wed May  2 2018 Jerry James <loganjerry@gmail.com> - 0.3.1-1
- New upstream version

* Sat Apr  7 2018 Jerry James <loganjerry@gmail.com> - 0.3.0-1
- New upstream version

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar  6 2017 Jerry James <loganjerry@gmail.com> - 0.2.4-1
- New upstream version

* Sat Mar  4 2017 Jerry James <loganjerry@gmail.com> - 0.2.2-1
- New upstream version

* Fri Mar  3 2017 Jerry James <loganjerry@gmail.com> - 0.2.0-1
- New upstream version
- Unbundle the roboto fonts

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.1.9-3
- Rebuild for Python 3.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb  1 2016 Jerry James <loganjerry@gmail.com> - 0.1.9-1
- Comply with latest python packaging guidelines

* Tue Nov 24 2015 Jerry James <loganjerry@gmail.com> - 0.1.9-1
- New upstream version

* Mon Nov 16 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.1.8-4
- Add Requires: fontawesome-web (rhbz#1282297)

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 0.1.8-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Jerry James <loganjerry@gmail.com> - 0.1.8-1
- New upstream version
- Unbundle the Lato fonts

* Wed Mar 11 2015 Jerry James <loganjerry@gmail.com> - 0.1.7-1
- New upstream version

* Sat Feb 21 2015 Jerry James <loganjerry@gmail.com> - 0.1.6-2
- Use license macro

* Thu Jul  3 2014 Jerry James <loganjerry@gmail.com> - 0.1.6-1
- Initial RPM
