#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x
%bcond_with	extra_only	# build only libfm-extra
%bcond_with	bootstrap	# synonym for extra_only (to break libfm<>menu-cache loop)

%if %{with bootstrap}
%define	with_extra_only	1
%endif
Summary:	Helper library for pcmanfm
Summary(pl.UTF-8):	Biblioteka pomocnicza do pcmanfm
Name:		libfm
Version:	1.2.5
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.xz
# Source0-md5:	a1ba9ae5e920f38b647dd511edd6c807
Patch0:		%{name}-doc.patch
URL:		http://pcmanfm.sourceforge.net/
BuildRequires:	cairo-devel >= 1.8.0
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.27.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.14}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libexif-devel
%{!?with_extra_only:BuildRequires:	menu-cache-devel >= 0.3.2}
BuildRequires:	pango-devel >= 1:1.16.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 0.13.0
BuildRequires:	xz
Obsoletes:	lxshortcut
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	shared-mime-info
Requires:	%{name}-extra = %{version}-%{release}
Requires:	glib2 >= 1:2.27.0
%{!?with_extra_only:Requires:	menu-cache >= 0.3.2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Helper library for pcmanfm.

%description -l pl.UTF-8
Biblioteka pomocnicza dla pcmanfm

%package devel
Summary:	Header files and libraries for libfm development
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do libfm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-extra-devel = %{version}-%{release}
Requires:	glib2-devel >= 1:2.27.0

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
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains the header files and libraries needed to develop
programs that use these libfm.

%description static -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe potrzebne do rozwoju oprogramowania
korzystającego z libfm.

%package gtk
Summary:	libfm-gtk library
Summary(pl.UTF-8):	Biblioteka libfm-gtk
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.18.0}
# in case someone want to split this package into smaller ones
Provides:	lxshortcut

%description gtk
libfm-gtk library.

%description gtk -l pl.UTF-8
Biblioteka libfm-gtk.

%package gtk-devel
Summary:	Header files for libfm-gtk library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libfm-gtk
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk = %{version}-%{release}
%{!?with_gtk3:Requires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk3:Requires:	gtk+3-devel >= 3.0}

%description gtk-devel
Header files for libfm-gtk library.

%description gtk-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libfm-gtk.

%package gtk-static
Summary:	Static libfm-gtk library
Summary(pl.UTF-8):	Statyczna biblioteka libfm-gtk
Group:		Development/Libraries
Requires:	%{name}-gtk-devel = %{version}-%{release}

%description gtk-static
Static libfm-gtk library.

%description gtk-static -l pl.UTF-8
Statyczna biblioteka libfm-gtk.

%package apidocs
Summary:	LIBFM API documentation
Summary(pl.UTF-8):	Dokumentacja API LIBFM
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
LIBFM API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API LIBFM.

%package extra
Summary:	libfm-extra library
Summary(pl.UTF-8):	Biblioteka libfm-extra
Group:		Libraries
Requires:	glib2 >= 1:2.27.0
Conflicts:	libfm < 1.2.5

%description extra
libfm-extra library.

%description extra -l pl.UTF-8
Biblioteka libfm-extra.

%package extra-devel
Summary:	Header files for libfm-extra library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libfm-extra
Group:		Development/Libraries
Requires:	%{name}-extra = %{version}-%{release}
Requires:	glib2-devel >= 1:2.27.0
Conflicts:	libfm-devel < 1.2.5

%description extra-devel
Header files for libfm-extra library.

%description extra-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libfm-extra.

%package extra-static
Summary:	Static libfm-extra library
Summary(pl.UTF-8):	Statyczna biblioteka libfm-extra
Group:		Development/Libraries
Requires:	%{name}-extra-devel = %{version}-%{release}
Conflicts:	libfm-static < 1.2.5

%description extra-static
Static libfm-extra library.

%description extra-static -l pl.UTF-8
Statyczna biblioteka libfm-extra.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	--enable-exif \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--enable-udisks \
	%{?with_extra_only:--with-extra-only} \
	--with-gtk=%{?with_gtk3:3}%{!?with_gtk3:2} \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}}

%{?with_apidocs:export LC_ALL=C.UTF-8}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -j1 \
	INSTALL_DATA="install -p -m 644" \
	DESTDIR=$RPM_BUILD_ROOT

# pkg-config present, so drop .la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfm*.la

%if %{without extra_only}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{tt_RU,tt}
# copy of ur (both empty anyway)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ur_PK

%find_lang %{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_mime_database

%postun
/sbin/ldconfig
%update_mime_database

%post	gtk -p /sbin/ldconfig
%postun	gtk -p /sbin/ldconfig

%post	extra -p /sbin/ldconfig
%postun	extra -p /sbin/ldconfig

%if %{without extra_only}
%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS TODO
%dir /etc/xdg/libfm
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/libfm/libfm.conf
%attr(755,root,root) %{_libdir}/libfm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm.so.4
%dir %{_libdir}/libfm
%dir %{_libdir}/libfm/modules
%attr(755,root,root) %{_libdir}/libfm/modules/vfs-*.so
%{_datadir}/libfm
%{_datadir}/mime/packages/libfm.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfm.so
%{_includedir}/libfm-1.0/fm.h
%{_includedir}/libfm-1.0/fm-actions.h
%{_includedir}/libfm-1.0/fm-app-info.h
%{_includedir}/libfm-1.0/fm-archiver.h
%{_includedir}/libfm-1.0/fm-bookmarks.h
%{_includedir}/libfm-1.0/fm-config.h
%{_includedir}/libfm-1.0/fm-deep-count-job.h
%{_includedir}/libfm-1.0/fm-dir-list-job.h
%{_includedir}/libfm-1.0/fm-dummy-monitor.h
%{_includedir}/libfm-1.0/fm-file.h
%{_includedir}/libfm-1.0/fm-file-info-job.h
%{_includedir}/libfm-1.0/fm-file-info.h
%{_includedir}/libfm-1.0/fm-file-launcher.h
%{_includedir}/libfm-1.0/fm-file-ops-job-change-attr.h
%{_includedir}/libfm-1.0/fm-file-ops-job-delete.h
%{_includedir}/libfm-1.0/fm-file-ops-job-xfer.h
%{_includedir}/libfm-1.0/fm-file-ops-job.h
%{_includedir}/libfm-1.0/fm-folder.h
%{_includedir}/libfm-1.0/fm-folder-config.h
%{_includedir}/libfm-1.0/fm-icon.h
%{_includedir}/libfm-1.0/fm-job.h
%{_includedir}/libfm-1.0/fm-list.h
%{_includedir}/libfm-1.0/fm-marshal.h
%{_includedir}/libfm-1.0/fm-mime-type.h
%{_includedir}/libfm-1.0/fm-module.h
%{_includedir}/libfm-1.0/fm-monitor.h
%{_includedir}/libfm-1.0/fm-nav-history.h
%{_includedir}/libfm-1.0/fm-path.h
%{_includedir}/libfm-1.0/fm-seal.h
%{_includedir}/libfm-1.0/fm-simple-job.h
%{_includedir}/libfm-1.0/fm-sortable.h
%{_includedir}/libfm-1.0/fm-templates.h
%{_includedir}/libfm-1.0/fm-terminal.h
%{_includedir}/libfm-1.0/fm-thumbnail-loader.h
%{_includedir}/libfm-1.0/fm-thumbnailer.h
%{_includedir}/libfm-1.0/fm-utils.h
%{_pkgconfigdir}/libfm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfm.a

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libfm-pref-apps
%attr(755,root,root) %{_bindir}/lxshortcut
%if %{with gtk3}
%attr(755,root,root) %{_libdir}/libfm-gtk3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm-gtk3.so.4
%else
%attr(755,root,root) %{_libdir}/libfm-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm-gtk.so.4
%endif
%attr(755,root,root) %{_libdir}/libfm/modules/gtk-*.so
#%config(noreplace) %verify(not md5 mtime size) /etc/xdg/libfm/pref-apps.conf
%{_desktopdir}/libfm-pref-apps.desktop
%{_desktopdir}/lxshortcut.desktop
%{_mandir}/man1/libfm-pref-apps.1*
%{_mandir}/man1/lxshortcut.1*

%files gtk-devel
%defattr(644,root,root,755)
%if %{with gtk3}
%attr(755,root,root) %{_libdir}/libfm-gtk3.so
%else
%attr(755,root,root) %{_libdir}/libfm-gtk.so
%endif
%{_includedir}/libfm-1.0/fm-app-chooser-combo-box.h
%{_includedir}/libfm-1.0/fm-app-chooser-dlg.h
%{_includedir}/libfm-1.0/fm-app-menu-view.h
%{_includedir}/libfm-1.0/fm-cell-renderer-pixbuf.h
%{_includedir}/libfm-1.0/fm-cell-renderer-text.h
%{_includedir}/libfm-1.0/fm-clipboard.h
%{_includedir}/libfm-1.0/fm-dir-tree-model.h
%{_includedir}/libfm-1.0/fm-dir-tree-view.h
%{_includedir}/libfm-1.0/fm-dnd-auto-scroll.h
%{_includedir}/libfm-1.0/fm-dnd-dest.h
%{_includedir}/libfm-1.0/fm-dnd-src.h
%{_includedir}/libfm-1.0/fm-file-menu.h
%{_includedir}/libfm-1.0/fm-file-properties.h
%{_includedir}/libfm-1.0/fm-folder-model.h
%{_includedir}/libfm-1.0/fm-folder-view.h
%{_includedir}/libfm-1.0/fm-gtk.h
%{_includedir}/libfm-1.0/fm-gtk-file-launcher.h
%{_includedir}/libfm-1.0/fm-gtk-marshal.h
%{_includedir}/libfm-1.0/fm-gtk-utils.h
%{_includedir}/libfm-1.0/fm-icon-pixbuf.h
%{_includedir}/libfm-1.0/fm-menu-tool-item.h
%{_includedir}/libfm-1.0/fm-path-bar.h
%{_includedir}/libfm-1.0/fm-path-entry.h
%{_includedir}/libfm-1.0/fm-places-model.h
%{_includedir}/libfm-1.0/fm-places-view.h
%{_includedir}/libfm-1.0/fm-progress-dlg.h
%{_includedir}/libfm-1.0/fm-side-pane.h
%{_includedir}/libfm-1.0/fm-standard-view.h
%{_includedir}/libfm-1.0/fm-tab-label.h
%{_includedir}/libfm-1.0/fm-thumbnail.h
%if %{with gtk3}
%{_pkgconfigdir}/libfm-gtk3.pc
%else
%{_pkgconfigdir}/libfm-gtk.pc
%endif

%files gtk-static
%defattr(644,root,root,755)
%if %{with gtk3}
%{_libdir}/libfm-gtk3.a
%else
%{_libdir}/libfm-gtk.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfm
%endif
%endif

%files extra
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfm-extra.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfm-extra.so.4

%files extra-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfm-extra.so
%dir %{_includedir}/libfm-1.0
%{_includedir}/libfm-1.0/fm-extra.h
%{_includedir}/libfm-1.0/fm-version.h
%{_includedir}/libfm-1.0/fm-xml-file.h
# symlink
%{_includedir}/libfm
%{_pkgconfigdir}/libfm-extra.pc

%files extra-static
%defattr(644,root,root,755)
%{_libdir}/libfm-extra.a
