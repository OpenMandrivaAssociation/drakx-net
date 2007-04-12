%define name drakx-net
%define version 0.12
%define release %mkrel 1

%define libname lib%{name}

Summary: Mandriva network tools
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: System/Configuration/Networking
Url: http://wiki.mandriva.com/en/Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: drakxtools >= 10.4.99-3mdv
Requires: %{name}-text
Requires: %{libname}
Requires: netprofile
Requires: perl-Gtk2-NotificationBubble
Conflicts: drakxtools <= 10.4.83

%description
This package contains the Mandriva network tools.

net_applet: applet to check network connection

net_monitor: connection monitoring

%package text
Summary: Mandriva network text tools
Group: System/Configuration/Networking
Requires: drakxtools-curses
Conflicts: drakxtools-curses <= 10.4.83

%description text
This package contains the Mandriva network tools that can be used in
text mode.

drakconnect: LAN/Internet connection configuration. It handles
ethernet, ISDN, DSL, cable, modem.

drakfirewall: simple firewall configurator

drakgw: internet connection sharing

drakproxy: proxies configuration

drakvpn: VPN configuration (openvpn, vpnc)


%package -n %{libname}
Summary: Mandriva network tools library
Group: System/Configuration/Networking
Requires: drakxtools-backend
Conflicts: drakxtools-backend <= 10.4.83

%description -n	%{libname}
This package contains the Mandriva network tools library.

%prep
%setup -q

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS
%{_bindir}/net_applet
%{_bindir}/drakroam
%{_sbindir}/drakhosts
%{_sbindir}/drakids
%{_sbindir}/draknetprofile
%{_sbindir}/draknfs
%{_sbindir}/drakroam
%{_sbindir}/draksambashare
%{_sbindir}/net_monitor
%{_prefix}/lib/libDrakX/network/ifw.pm
%{_prefix}/lib/libDrakX/network/monitor.pm
%config(noreplace) %{_sysconfdir}/pam.d/drakroam
%config(noreplace) %{_sysconfdir}/security/console.apps/drakroam
%{_sysconfdir}/X11/xinit.d/??net_applet
%{_datadir}/applications/net_applet.desktop
%{_datadir}/autostart/net_applet.desktop
%{_datadir}/gnome/autostart/net_applet.desktop
%{_prefix}/lib/libDrakX/icons/*.png
%{_datadir}/libDrakX/pixmaps/*.png

%files text
%{_sbindir}/drakconnect
%{_sbindir}/drakfirewall
%{_sbindir}/drakgw
%{_sbindir}/drakinvictus
%{_sbindir}/drakproxy
%{_sbindir}/drakvpn

%files -n %{libname} -f %{name}.lang
%defattr(-,root,root)
%exclude %{_prefix}/lib/libDrakX/network/ifw.pm
%exclude %{_prefix}/lib/libDrakX/network/monitor.pm
%{_prefix}/lib/libDrakX/network/*


