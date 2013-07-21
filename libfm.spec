#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	Helper library for pcmanfm
Summary(pl.UTF-8):	Biblioteka pomocnicza do pcmanfm
Name:		libfm
Version:	1.1.0
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.gz
# Source0-md5:	a5bc8b8291cf810c659bfb3af378b5de
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
BuildRequires:	vala >= 0.13.0
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	shared-mime-info
Requires:	glib2 >= 1:2.27.0
# in case someone want to split this package into smaller ones
Provides:	libfm-gtk
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
%{__make}

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
%dir /etc/xdg/libfm
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/libfm/libfm.conf
%attr(755,root,root) %{_libdir}/libfm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm.so.3
%{_datadir}/libfm
%{_datadir}/mime/packages/libfm.xml

# -gtk
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/libfm/pref-apps.conf
%attr(755,root,root) %{_bindir}/libfm-pref-apps
%attr(755,root,root) %{_libdir}/libfm-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm-gtk.so.3
%{_desktopdir}/libfm-pref-apps.desktop
%{_mandir}/man1/libfm-pref-apps.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libfm
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.so
%{_pkgconfigdir}/libfm-gtk.pc
%{_pkgconfigdir}/libfm-gtk3.pc
%{_pkgconfigdir}/libfm.pc
%{_includedir}/libfm-1.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libfm-gtk.a
%{_libdir}/libfm.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfm
%endif
