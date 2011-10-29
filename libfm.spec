#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	Helper library for pcmanfm
Summary(pl.UTF-8):	Biblioteka pomocnicza do pcmanfm
Name:		libfm
Version:	0.1.17
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.gz
# Source0-md5:	a97e03d973e6ac727f28d0934d6c9ad5
Patch0:		%{name}-link.patch
URL:		http://pcmanfm.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.27.0
BuildRequires:	gtk+2-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	menu-cache-devel
BuildRequires:	pkgconfig
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
%patch0 -p1

# docs dir missing in tarball, but configure.ac references it
install -d docs/reference/libfm
touch docs/Makefile.in
touch docs/reference/Makefile.in
touch docs/reference/libfm/Makefile.in

%build
%configure \
	%{!?with_apidocs:--enable-gtk-doc=no} \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_DATA="install -p -m 644" \
	DESTDIR=$RPM_BUILD_ROOT

# pkg-config present, so drop .la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfm.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfm-gtk.la

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/tt_RU

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
%attr(755,root,root) %ghost %{_libdir}/libfm.so.1
%{_datadir}/libfm
%{_datadir}/mime/packages/libfm.xml

# -gtk
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/libfm/pref-apps.conf
%attr(755,root,root) %{_bindir}/libfm-pref-apps
%attr(755,root,root) %{_libdir}/libfm-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm-gtk.so.1
%{_desktopdir}/libfm-pref-apps.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/libfm
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.so
%{_pkgconfigdir}/libfm-gtk.pc
%{_pkgconfigdir}/libfm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfm-gtk.a
%{_libdir}/libfm.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfm
%endif
