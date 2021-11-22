# TODO: init scripts/service files for zephyrd and zhm
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	hesiod		# Hesiod support
%bcond_without	kerberos5	# Kerberos 5 support
%bcond_without	static_libs	# static library
#
Summary:	Project Athena's notification service
Summary(pl.UTF-8):	Usługa powiadomień z Projektu Athena
Name:		zephyr
Version:	3.1.2
Release:	3
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/zephyr-im/zephyr/releases
Source0:	https://github.com/zephyr-im/zephyr/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f41be8ee4383d100d4eeb7ed7de0e018
Patch0:		%{name}-heimdal.patch
URL:		https://github.com/zephyr-im/zephyr
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	c-ares-devel
BuildRequires:	flex
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_hesiod:BuildRequires:	hesiod-devel}
BuildRequires:	libcom_err-devel
BuildRequires:	libss-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	xorg-lib-libX11-devel
# if using noarch subpackages:
#BuildRequires:	rpm-build >= 4.6
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zephyr allows users to send messages to other users or to groups of
users. Users can view incoming Zephyr messages as windowgrams
(transient X windows) or as text on a terminal. Zephyr can optionally
make use of the Kerberos security library or the Hesiod service name
resolution library.

This package contains Zephyr clients.

%description -l pl.UTF-8
Zephyr pozwala użytkownikom wysyłać wiadomości do innych użytkowników
lub grup użytkowników. Użytkownicy mogą zobaczyć przychodzące
wiadomości Zephyra jako oknogramy (przemijające okienka X) albo jako
tekst na terminalu. Zephyr opcjonalnie może wykorzystywać bibliotekę
bezpieczeństwa Kerberos lub bibliotekę rozwiązywania nazw usług
Hesiod.

Ten pakiet zawiera programy klienckie Zephyra.

%package server
Summary:	Zephyr server
Summary(pl.UTF-8):	Serwer usługi Zephyr
Group:		Networking/Daemons
Requires:	%{name}-libs = %{version}-%{release}

%description server
zephyrd is the central server for the Zephyr Notification System. It
maintains a location database of all currently logged-in users, and a
subscription database for each user's Zephyr clients.

%description server -l pl.UTF-8
zephyrd to centralny serwer systemu powiadomień Zephyr. Utrzymuje bazę
danych lokalizacji wszystkich aktualnie zalogowanych użytkowników oraz
bazę danych subskrypcji klientów Zephyra dla każdego użytkownika.

%package libs
Summary:	Zephyr service shared library
Summary(pl.UTF-8):	Biblioteka współdzielona usługi Zephyr
Group:		Libraries

%description libs
Zephyr service shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona usługi Zephyr.

%package devel
Summary:	Header files for Zephyr library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Zephyr
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_kerberos5:Requires:	heimdal-devel}
%{?with_hesiod:Requires:	hesiod-devel}

%description devel
Header files for Zephyr library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Zephyr.

%package static
Summary:	Static Zephyr library
Summary(pl.UTF-8):	Statyczna biblioteka Zephyr
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Zephyr library.

%description static -l pl.UTF-8
Statyczna biblioteka Zephyr.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's/__DEV__/%{version}/' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{?with_hesiod:--with-hesiod} \
	%{?with_kerberos5:--with-krb5}
%{__make} -j 1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzephyr.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zaway
%attr(755,root,root) %{_bindir}/zctl
%attr(755,root,root) %{_bindir}/zleave
%attr(755,root,root) %{_bindir}/zlocate
%attr(755,root,root) %{_bindir}/znol
%attr(755,root,root) %{_bindir}/zstat
%attr(755,root,root) %{_bindir}/zwgc
%attr(755,root,root) %{_bindir}/zwrite
%attr(755,root,root) %{_sbindir}/zhm
%attr(755,root,root) %{_sbindir}/zshutdown_notify
%{_datadir}/zephyr
%{_mandir}/man1/zaway.1*
%{_mandir}/man1/zctl.1*
%{_mandir}/man1/zephyr.1*
%{_mandir}/man1/zleave.1*
%{_mandir}/man1/zlocate.1*
%{_mandir}/man1/znol.1*
%{_mandir}/man1/zwgc.1*
%{_mandir}/man1/zwrite.1*
%{_mandir}/man8/zhm.8*
%{_mandir}/man8/zshutdown_notify.8*
%{_mandir}/man8/zstat.8*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zephyrd
%dir %{_sysconfdir}/zephyr
%dir %{_sysconfdir}/zephyr/acl
%config(noreplace) %verify(not md5,mtime,size) %{_sysconfdir}/zephyr/default.subscriptions
%{_mandir}/man8/zephyrd.8*

%files libs
%defattr(644,root,root,755)
%doc NOTES OPERATING README.in USING h/zephyr/mit-copyright.h
%attr(755,root,root) %{_libdir}/libzephyr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzephyr.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzephyr.so
%{_includedir}/zephyr
%{_pkgconfigdir}/zephyr.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzephyr.a
%endif
