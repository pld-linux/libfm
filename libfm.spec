Summary:	Helper library for pcmanfm
Summary(pl.UTF-8):	Biblioteka pomocnicza do pcmanfm
Name:		libfm
Version:	0.1.14
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.gz
# Source0-md5:	d55e51dced6bb9ef46665243b079761f
Patch0:		%{name}-link.patch
URL:		http://pcmanfm.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	menu-cache-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
Requires(post,postun):	shared-mime-info
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

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%{_sysconfdir}/xdg/libfm
%attr(755,root,root) %{_bindir}/libfm-pref-apps
%attr(755,root,root) %{_libdir}/gio/modules/libgiofm.so
%attr(755,root,root) %{_libdir}/libfm-gtk.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libfm-gtk.so.0
%attr(755,root,root) %{_libdir}/libfm.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libfm.so.0
%dir %{_libdir}/libfm
%attr(755,root,root) %{_libdir}/libfm/gnome-terminal
%{_desktopdir}/libfm-pref-apps.desktop
%{_datadir}/libfm
%{_datadir}/mime/packages/libfm.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/libfm
%{_libdir}/libfm-gtk.la
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.la
%{_libdir}/libfm.so
%{_pkgconfigdir}/libfm-gtk.pc
%{_pkgconfigdir}/libfm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfm-gtk.a
%{_libdir}/libfm.a
