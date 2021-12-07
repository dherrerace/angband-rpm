Name:    angband
Version: 4.2.0
Release: 1%{?dist}
Summary: Popular roguelike role playing game

License: GPLv2 and BSD and CC-BY
URL:     https://rephial.org/
#Source0: http://rephial.org/downloads/4.2/angband-4.2.0.tar.gz
Source0: angband-4.2.0-noshockbolt.tar.gz
# angband contains graphics tiles that have extra restrictions that prohibit
# us from shipping it.
# Download the upstream tarball and invoke this script while in the
# tarball's directory:
# ./generate-tarball.sh 4.2.0
Source1: generate-tarball.sh
Source2: angband.desktop
Source3: angband.png
Patch0:  angband-4.1.3-savedir.patch

BuildRequires: autoconf automake
BuildRequires: ncurses-devel desktop-file-utils gcc
BuildRequires: libX11-devel libXmu-devel libXt-devel libXaw-devel
Requires: xorg-x11-fonts-misc
Requires: %{name}-data = %{version}-%{release}
Requires(pre): shadow-utils

%description
A roguelike game where you explore a very deep dungeon, kill monsters, try to
equip yourself with the best weapons and armor you can find, and finally face
Morgoth - "The Dark Enemy".

%package data
Summary:        Angband data files
%description data
Data files for the Angband game

%prep
%setup -q
%patch0
# Remove windows sources, which include copies of third-party headers (eg png.h)
rm -rf src/win
./autogen.sh


%build
%configure --without-private-dirs --enable-sdl
make %{?_smp_mflags}


%install
%make_install
install -d $RPM_BUILD_ROOT/%{_var}/games/%{name}
install -d $RPM_BUILD_ROOT/%{_var}/games/%{name}/scores

desktop-file-install \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        %{SOURCE2}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man6/
install -p -m 644 src/angband.man $RPM_BUILD_ROOT%{_mandir}/man6/angband.6

# Remove the bundled fonts.
rm -rf $RPM_BUILD_ROOT%{_datarootdir}/angband/fonts


%pre
getent group angband >/dev/null || groupadd -r angband
exit 0

%files
%license docs/copying.rst
%doc docs/*.rst
%attr(2755,root,angband) %{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%dir %{_sysconfdir}/angband
%dir %{_sysconfdir}/angband/gamedata
%dir %{_sysconfdir}/angband/customize
%config(noreplace) %{_sysconfdir}/angband/gamedata/*
%config(noreplace) %{_sysconfdir}/angband/customize/*
%dir %attr(0775,root,angband) %{_var}/games/%{name}
%dir %attr(2775,root,angband) %{_var}/games/%{name}/scores
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_mandir}/man6/angband.*

%files data
%{_datarootdir}/angband



%changelog
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
