%global debug_package %{nil}

# If target system is RHEL/CentOS 6
%if 0%{?rhel} && 0%{?rhel} == 6
# Then disable systemd-related features
%global systemd no
%else
# Enable for other configurations
%global systemd yes
%endif

Name:		udevil
Version:	0.4.4
Release:	2%{dist}
Summary:	Mount and unmount without password
Group:		System Environment/Daemons
License:	GPLv3+
URL:		http://ignorantguru.github.com/udevil/
Source0:	https://github.com/IgnorantGuru/%{name}/archive/%{version}.tar.gz
BuildRequires:	intltool, gettext
BuildRequires:	glib2-devel
%if %{systemd} == yes
BuildRequires:	systemd-devel
%else
BuildRequires:	libudev-devel
%endif

%description
udevil is a command line Linux program which mounts and unmounts
removable devices without a password, shows device info, and monitors
device changes. It can also mount ISO files, nfs://, smb://, ftp://,
ssh:// and WebDAV URLs, and tmpfs/ramfs filesystems

%prep
%setup -q
sed -i 's/-o root -g root -m 4755//g' src/Makefile.in

%build
%configure --enable-systemd=%{systemd}
make %{?_smp_mflags}

%install
%make_install
%find_lang %{name}

%if %{systemd} == yes
%post
%systemd_post devmon@.service

%preun
%systemd_preun devmon@.service

%postun
%systemd_postun devmon@.service
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README
%attr(4755,-,-) %{_bindir}/%{name}
%{_bindir}/devmon
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%if %{systemd} == yes
%config(noreplace) %{_sysconfdir}/conf.d/devmon
%{_unitdir}/devmon@.service
%endif

%changelog
* Fri Dec 18 2015 selurvedu <selurvedu@yandex.com> 0.4.4-2
- Support RHEL/CentOS 6 (the oldest version with libudev)
- Don't make a usual unit (devmon.service)
  from instantiated unit (devmon@.service)
- Several changes and improvements suggested by rpmlint
  and specfile guidelines
* Wed May 06 2015 Huaren Zhong <huaren.zhong@gmail.com> 0.4.4
- Rebuild for Fedora
* Wed Jan 08 2014 Simone Sclavi <darkhado@gmail.com> 0.4.3-1
- Initial build
