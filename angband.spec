Name:    angband
Version: 4.2.3
Release: 4%{?dist}
Summary: Popular roguelike role playing game

License: GPLv2
URL:     https://rephial.org/
Source0: angband-%{version}-norestricted.tar.gz
# angband contains assets and code that don't comply to Fedora's 
# licensing restrictions. Therefore we use this script to download 
# and remove the restricted files before shipping it.
# Invoke this script to download and generate a patched tarball:
# ./generate-tarball.sh
Source1: generate-tarball.sh
# The fix-restricted.patch file is used by generate-tarball.sh to fix
# the source to work without the restricted assets.
Source2: fix-restricted.patch
Source3: angband.desktop
Source4: angband.png

# Fixes regarding SDL2 events affecting the menu
# https://github.com/angband/angband/pull/5170
# https://github.com/angband/angband/pull/5169
Patch0:  angband-4.2.3-1-fix_events.patch
# Fix so that it can get installed without root privileges
# https://github.com/angband/angband/pull/5186
Patch1:  angband-4.2.3-1-chown_fix.patch
# Move gamedata from sysconfpath to libpath
# https://github.com/angband/angband/pull/5185
Patch2:  angband-4.2.3-1-gamedata_in_lib.patch

BuildRequires: autoconf automake make
BuildRequires: ncurses-devel desktop-file-utils gcc
BuildRequires: SDL2-devel SDL2_image-devel SDL2_ttf-devel
BuildRequires: SDL2_mixer-devel python3-docutils

Requires: hicolor-icon-theme
Requires: freetype >= 2.11.1
Requires: %{name}-data = %{version}-%{release}

%description
A roguelike game where you explore a very deep dungeon, kill monsters, try to
equip yourself with the best weapons and armor you can find, and finally face
Morgoth - "The Dark Enemy".


%package data
Summary: Angband data files
License: GPLv2 and CC-BY
BuildArch: noarch

%description data
Data files for the Angband game


%package doc
Summary: Angband doc files

%description doc
Documentation about the Angband game


%prep
%autosetup -p1
./autogen.sh

# file-not-utf8 fix
iconv -f iso8859-1 -t utf-8 \
    docs/version.rst > docs/version.rst.conv && \
    mv -f docs/version.rst.conv docs/version.rst


%build
%configure \
    --with-setgid=games \
    --with-gamedata-in-lib \
    --enable-sdl2 \
    --enable-sdl2-mixer \
    --disable-x11
%make_build


%install
%make_install
install -d $RPM_BUILD_ROOT/%{_var}/games/%{name}
install -d $RPM_BUILD_ROOT/%{_var}/games/%{name}/scores
install -d $RPM_BUILD_ROOT/%{_var}/games/%{name}/archive
install -d $RPM_BUILD_ROOT/%{_var}/games/%{name}/save

desktop-file-install \
    --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
    %{SOURCE3}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man6/
install -p -m 644 src/angband.man $RPM_BUILD_ROOT%{_mandir}/man6/angband.6


%files
%license docs/copying.rst
%attr(2755,root,games) %{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%dir %{_sysconfdir}/angband
%dir %{_sysconfdir}/angband/customize
%config(noreplace) %{_sysconfdir}/angband/customize/*
%dir %attr(0775,root,games) %{_var}/games/%{name}
%dir %attr(2775,root,games) %{_var}/games/%{name}/scores
%dir %attr(2775,root,games) %{_var}/games/%{name}/archive
%dir %attr(2775,root,games) %{_var}/games/%{name}/save
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_mandir}/man6/angband.*


%files data
%license docs/copying.rst
%{_datadir}/angband


%files doc
%license docs/copying.rst
%doc docs/*.rst


%changelog
* Mon Jan 10 2022 Diego Herrera <dherrera@redhat.com> 4.2.3-4
- Added make as an expicit BuildRequires
- Removed Requires that can be autodetected
- Fixed licensing description
- Use macros when needed
- Separated doc files into a separate package
- Added license to subpackages
- Added some missing folders in the installation process

* Mon Dec 13 2021 Diego Herrera <dherrera@redhat.com> 4.2.3-3
- Move customize folder to sysconfdir
- Add patch to keep the gamedata folder to datadir
- Add references to upstream patches

* Sun Dec 12 2021 Diego Herrera <dherrera@redhat.com> 4.2.3-2
- Restored Adam Bolt's tileset
- Fix typos and descriptions

* Sat Dec 11 2021 Diego Herrera <dherrera@redhat.com> 4.2.3-1
- Update to 4.2.3
- Use setgid mode with games group
- Change default renderer to SDL2
- Apply upstream fixes to SDL2 implementation
- Remove more restricted assets
- Move game data to datadir

* Sun Aug 25 2019 Wart <wart at kobold dot org> 4.2.0-1
- Update to 4.2.0
- Fix group creation
- Fix desktop file
- Update license naming
- Add man page
- Remove restricted tileset

* Tue Aug 13 2019 Wart <wart at kobold dot org> 4.1.3-4
- Use recommended dynamic allocation for the group

* Sat Aug 10 2019 Wart <wart at kobold dot org> 4.1.3-3
- Minor spec file cleanup

* Wed Jul 24 2019 Wart <wart at kobold dot org> 4.1.3-2
- Enable shared scoreboard file

* Sun Jul 21 2019 Wart <wart at kobold dot org> 4.1.3-1
- Update to 4.1.3

* Sun Jul 21 2019 Wart <wart at kobold dot org> 3.0.6-5
- Updates to build for Fedora 30

* Wed Apr 4 2007 Wart <wart at kobold dot org> 3.0.6-4
- Add BR: to allow X11 support

* Tue Apr 3 2007 Wart <wart at kobold dot org> 3.0.6-3
- Add icon name to .desktop files
- Fix License tag
- Move game data to /var/games/angband
- Remove non-working -graphics desktop file

* Mon Apr 2 2007 Wart <wart at kobold dot org> 3.0.6-2
- Use custom group for setgid as added protection
- Install extra graphics files
- Add vendor to .desktop file installation

* Thu Mar 29 2007 Wart <wart at kobold dot org> 3.0.6-1
- Update to 3.0.6
- Updated spec to Fedora Extras standards (again)

* Sat Feb 25 2006 Wart <wart at kobold dot org> 3.0.3-5
- Update. spec to Fedora Extras standards
