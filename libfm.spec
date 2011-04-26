Summary:	Helper library for pcmanfm
Summary(pl.UTF-8):	Biblioteka pomocnicza do pcmanfm
Name:		libfm
Version:	0.1.15
Release:	2.git3625952cea
License:	GPL v2+
Group:		Libraries
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/%{name}_%{version}+git-3625952cea.orig.tar.gz
# Source0-md5:	5a63ab70b24bb178b2cefb2ab49680cd
Patch0:		%{name}-link.patch
URL:		http://pcmanfm.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.27.0
BuildRequires:	gtk+2-devel
BuildRequires:	gtk-doc
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

%prep
%setup -qn %{name}
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
%attr(755,root,root) %{_libdir}/libfm-gtk.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libfm-gtk.so.0
%attr(755,root,root) %{_libdir}/libfm.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libfm.so.0
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
