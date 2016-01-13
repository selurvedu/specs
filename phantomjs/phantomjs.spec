Name:           phantomjs
Version:        2.0.0
Release:        2%{?dist}
Summary:        A headless WebKit with JavaScript API
Group:          Utilities/Misc
License:        BSD
URL:            http://phantomjs.org/
Source:         https://bitbucket.org/ariya/phantomjs/downloads/%{name}-%{version}-source.zip

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gperf
BuildRequires:  libicu-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  ruby
BuildRequires:  sqlite-devel

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and
native support for various web standards: DOM handling, CSS selector,
JSON, Canvas, and SVG. PhantomJS is created by Ariya Hidayat.

%prep
%setup -q

%build
./build.sh --confirm

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp bin/%{name} %{buildroot}%{_bindir}/%{name}
cp examples/* %{buildroot}%{_datadir}/%{name}/examples/
cp CONTRIBUTING.md %{buildroot}%{_datadir}/%{name}/
cp ChangeLog %{buildroot}%{_datadir}/%{name}/
cp LICENSE.BSD %{buildroot}%{_datadir}/%{name}/
cp README.md %{buildroot}%{_datadir}/%{name}/

%files
%defattr(0444,root,root)
%attr(0555,root,root)%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Wed Jan 13 2016 selurvedu <selurvedu@yandex.com> 2.0.0-2
- Reformat and reorder spec header and description,
  add "URL", remove "Packager"

* Sat May 9 2015 Frankie Dintino <fdintino@gmail.com>
- updated to version 2.0, added BuildRequires directives

* Fri Apr 18 2014 Eric Heydenberk <heydenberk@gmail.com>
- add missing filenames for examples to files section

* Tue Apr 30 2013 Eric Heydenberk <heydenberk@gmail.com>
- add missing filenames for examples to files section

* Wed Apr 24 2013 Robin Helgelin <lobbin@gmail.com>
- updated to version 1.9

* Thu Jan 24 2013 Matthew Barr <mbarr@snap-interactive.com>
- updated to version 1.8

* Thu Nov 15 2012 Jan Schaumann <jschauma@etsy.com>
- first rpm version
