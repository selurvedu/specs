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
Requires:       urw-fonts

# Upstream issue #12713
# https://github.com/ariya/phantomjs/issues/12713
Patch0:         phantomjs-python3-udis86-itab.patch
# Upstream issues #13265 #13518
# https://github.com/ariya/phantomjs/issues/13265
# https://github.com/ariya/phantomjs/issues/13518
Patch1:         phantomjs-gcc5-compile-fix.patch

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and
native support for various web standards: DOM handling, CSS selector,
JSON, Canvas, and SVG. PhantomJS is created by Ariya Hidayat.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./build.sh --confirm %(smp=%{?_smp_mflags}; echo ${smp/-j/--jobs })

%install
install -Dm 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}

%files
%defattr(-,root,root)
%license LICENSE.BSD
%doc ChangeLog README.md examples/
%{_bindir}/%{name}

%changelog
* Wed Jan 13 2016 selurvedu <selurvedu@yandex.com> 2.0.0-2
- Reformat and reorder spec header and description,
  add "URL", remove "Packager"
- Use "--jobs" in "build" section
- Add patches for GCC 5 and Python 3
- Add "urw-fonts" dependency to fix rendering
  of non-Latin symbols
- Update "install" and "files" sections (thanks, Alexei)
- Don't bundle CONTRIBUTING.md

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
