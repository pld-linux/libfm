#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	Helper library for pcmanfm
Summary(pl.UTF-8):	Biblioteka pomocnicza do pcmanfm
Name:		libfm
Version:	1.2.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.xz
# Source0-md5:	07d1361bc008db46b0fd4c775f5696de
Patch1:		mate-desktop.patch
URL:		http://pcmanfm.sourceforge.net/
BuildRequires:	cairo-devel >= 1.8.0
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.27.0
BuildRequires:	gtk+2-devel >= 2.18.0
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libexif-devel
BuildRequires:	menu-cache-devel
BuildRequires:	pango-devel >= 1.16.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 0.13.0
BuildRequires:	xz
Obsoletes:	lxshortcut
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	shared-mime-info
Requires:	glib2 >= 1:2.27.0
# in case someone want to split this package into smaller ones
Provides:	libfm-gtk
Provides:	lxshortcut
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Helper library for pcmanfm.

%description -l pl.UTF-8
Biblioteka pomocnicza dla pcmanfm

%package devel
Summary:	Header files and libraries for libfm development
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do libfm
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	libfm-gtk-devel

%description devel
This package contains the header files needed to develop programs that
use these libfm.

%description devel -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe potrzebne do rozwoju oprogramowania
korzystającego z libfm.

%package static
Summary:	Static library for libfm development
Summary(pl.UTF-8):	Biblioteka statyczna do libfm
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
This package contains the header files and libraries needed to develop
programs that use these libfm.

%description static -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe potrzebne do rozwoju oprogramowania
korzystającego z libfm.

%package apidocs
Summary:	LIBFM API documentation
Summary(pl.UTF-8):	Dokumentacja API LIBFM
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
LIBFM API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API LIBFM.

%prep
%setup -q
%patch1 -p1

%build
%configure \
	--enable-gtk-doc=%{!?with_apidocs:no}%{?with_apidocs:yes} \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}} \
	--enable-exif \
	--enable-udisks \
	--with-gtk=2
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -j1 \
	INSTALL_DATA="install -p -m 644" \
	DESTDIR=$RPM_BUILD_ROOT

# pkg-config present, so drop .la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfm.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfm-gtk.la

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/tt_RU

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_mime_database

%postun
/sbin/ldconfig
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS TODO
%attr(755,root,root) %{_bindir}/lxshortcut
%dir /etc/xdg/libfm
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/libfm/libfm.conf
%attr(755,root,root) %{_libdir}/libfm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm.so.4
%attr(755,root,root) %{_libdir}/libfm-extra.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm-extra.so.4
%{_datadir}/libfm
%{_datadir}/mime/packages/libfm.xml
%attr(755,root,root) %{_libdir}/libfm

# -gtk
#%config(noreplace) %verify(not md5 mtime size) /etc/xdg/libfm/pref-apps.conf
%attr(755,root,root) %{_bindir}/libfm-pref-apps
%attr(755,root,root) %{_libdir}/libfm-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm-gtk.so.4
%{_desktopdir}/libfm-pref-apps.desktop
%{_desktopdir}/lxshortcut.desktop
%{_mandir}/man1/libfm-pref-apps.1*
%{_mandir}/man1/lxshortcut.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libfm
%{_libdir}/libfm-extra.so
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.so
%{_pkgconfigdir}/libfm-gtk.pc
%{_pkgconfigdir}/libfm-gtk3.pc
%{_pkgconfigdir}/libfm.pc
%{_includedir}/libfm-1.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libfm-extra.a
%{_libdir}/libfm-gtk.a
%{_libdir}/libfm.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfm
%endif
