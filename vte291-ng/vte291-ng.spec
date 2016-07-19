%global apiver 2.91

Name:           vte291-ng
Version:        0.44.2
Release:        2%{?dist}
Summary:        Terminal emulator library

License:        LGPLv2+
URL:            http://www.gnome.org/
Source0:        http://download.gnome.org/sources/vte/0.44/vte-%{version}.tar.xz

# https://bugzilla.gnome.org/show_bug.cgi?id=711059
Patch100:       vte291-command-notify.patch

# Since version 0.39.90 in Fedora 22, ABI was unintentionally broken
# in vte291-command-notify.patch. It was fixed in version 0.44.2 in Fedora 24,
# but not in older Fedora releases, which still have gnome-terminal relying
# on broken ABI.
# This patch reverts the fix, thus breaking ABI back for Fedora 22 and 23.
%if 0%{?fedora} > 21 && 0%{?fedora} < 24
Patch110:       break-abi-again.patch
%endif

# https://bugzilla.gnome.org/show_bug.cgi?id=679658
# Patch generated from https://github.com/thestinger/vte-ng
Patch200:       expose_select_text.patch

BuildRequires:  gettext
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  gobject-introspection-devel
BuildRequires:  gperf
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  intltool
BuildRequires:  vala-tools

# initscripts creates the utmp group
Requires:       initscripts
Requires:       %{name}-profile

Conflicts:      vte291
Provides:       vte291 = %{version}-%{release}

# This Conflicts directive is only necessary on Fedora 24,
# please see comment for Patch110.
%if 0%{?fedora} >= 24
Conflicts:      gnome-terminal < 3.20.1-2
%endif

%description
VTE is a library implementing a terminal emulator widget for GTK+. VTE
is mainly used in gnome-terminal, but can also be used to embed a
console/terminal in games, editors, IDEs, etc.

This is a patched version from https://github.com/thestinger/vte-ng

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

# vte-profile is deliberately not noarch to avoid having to obsolete a noarch
# subpackage in the future when we get rid of the vte3 / vte291 split. Yum is
# notoriously bad when handling noarch obsoletes and insists on installing both
# of the multilib packages (i686 + x86_64) as the replacement.
%package -n     %{name}-profile
Summary:        Profile script for VTE terminal emulator library
License:        GPLv3+
# vte.sh was previously part of the vte3 package
Conflicts:      vte3 < 0.36.1-3
Conflicts:      vte-profile
Provides:       vte-profile = %{version}-%{release}

%description -n %{name}-profile
The %{name}-profile package contains a profile.d script for the VTE terminal
emulator library.

%prep
%setup -q -n vte-%{version}
%patch100 -p1 -b .command-notify
%patch110 -p1 -b .break-abi-again
%patch200 -p1 -b .expose_select_text

%build
CFLAGS="%optflags -fPIE -DPIE -Wno-nonnull" \
CXXFLAGS="$CFLAGS" \
LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now -pie" \
%configure \
        --disable-static \
        --libexecdir=%{_libdir}/vte-%{apiver} \
        --disable-gtk-doc \
        --enable-introspection
make %{?_smp_mflags} V=1

%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang vte-%{apiver}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f vte-%{apiver}.lang
%license COPYING
%doc NEWS README
%{_libdir}/libvte-%{apiver}.so.0*
%{_libdir}/girepository-1.0/

%files devel
%{_bindir}/vte-%{apiver}
%{_includedir}/vte-%{apiver}/
%{_libdir}/libvte-%{apiver}.so
%{_libdir}/pkgconfig/vte-%{apiver}.pc
%{_datadir}/gir-1.0/
%doc %{_datadir}/gtk-doc/
%{_datadir}/vala/

%files -n %{name}-profile
%{_sysconfdir}/profile.d/vte.sh

%changelog
* Wed Jul 20 2016 selurvedu <selurvedu@yandex.com> - 0.44.2+ng-2
- Add compatibility patch for broken ABI in Fedora 22 and 23

* Sat Jul 16 2016 selurvedu <selurvedu@yandex.com> - 0.44.2+ng-1
- Update expose_select_text.patch to be compatible with vte 0.44.2
  Source: vte-ng 0.44.1b (df5bb2ca5edca23f7a8508f5de63331d85e83907)

* Tue May 10 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.2-1
- Update to 0.44.2
- Rebase downstream patches and undo unintentional ABI break

* Mon Apr 11 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.44.1-1
- Update to 0.44.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 0.44.0-1
- Update to 0.44.0

* Tue Mar 15 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.92-1
- Update to 0.43.92

* Tue Mar 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.91-1
- Update to 0.43.91
- Remove BuildRequires on pkgconfig(libpcre2-8)

* Tue Mar 01 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.90-1
- Update to 0.43.90

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.2-1
- Update to 0.43.2

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.1-1
- Update to 0.43.1
- Drop upstreamed patch

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.43.0-1
- Update to 0.43.0
- Add BuildRequires on pkgconfig(libpcre2-8)
- Disable -Wnonnull

* Thu Jan 28 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.42.3-1
- Update to 0.42.3
- Backport upstream patch to fix disappearing lines (GNOME #761097)

* Tue Jan 19 2016 selurvedu <selurvedu@yandex.com> - 0.42.1+ng-1
- Rename vte291 to vte291-ng
- Add expose_select_text.patch
  Source: vte-ng 0.42.1 (ff40e5dafa83a4bb394ee755e1a48922d32a3ca3)
- Add 'Conflicts' and 'Provides' for vte291

* Wed Oct 14 2015 Kalev Lember <klember@redhat.com> - 0.42.1-1
- Update to 0.42.1

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 0.42.0-1
- Update to 0.42.0
- Use license macro for COPYING

* Mon Sep 14 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.41.90-1
- Update to 0.41.90
- Rebased downstream patches after the migration to C++
- gnome-pty-helper has been removed

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.40.2-1
- Update to 0.40.2

* Tue Mar 24 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.40.0-1
- Update to 0.40.0

* Thu Mar 19 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.39.92-1
- Update to 0.39.92

* Tue Feb 17 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.39.90-1
- Update to 0.39.90
- Add command-notify patches

* Fri Dec 19 2014 Richard Hughes <rhughes@redhat.com> - 0.39.1-1
- Update to 0.39.1

* Mon Dec 01 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.39.0-2
- Backport upstream patch to fix zombie shells (GNOME #740929)

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 0.39.0-1
- Update to 0.39.0

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.2-1
- Update to 0.38.2

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.1-1
- Update to 0.38.1

* Sun Sep 14 2014 Kalev Lember <kalevlember@gmail.com> - 0.38.0-1
- Update to 0.38.0

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.90-1
- Update to 0.37.90

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.2-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 0.37.2-1
- Update to 0.37.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.1-1
- Update to 0.37.1

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-2
- Split out a vte-profile subpackage that can be used with both vte291 / vte3

* Tue May 06 2014 Kalev Lember <kalevlember@gmail.com> - 0.37.0-1
- Initial Fedora package, based on previous vte3 0.36 packaging
