%define name drakx-net
%define version 0.14
%define release %mkrel 2

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

# consolehelper config

ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/draknetcenter

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps/

cat > %{buildroot}%{_sysconfdir}/pam.d/draknetcenter <<EOF
#%PAM-1.0
auth       sufficient   pam_rootok.so
auth       required     pam_console.so
auth       sufficient   pam_timestamp.so
auth       include      system-auth
account    required     pam_permit.so
session    required     pam_permit.so
session    optional     pam_xauth.so
session    optional     pam_timestamp.so
EOF

cat > %{buildroot}%{_sysconfdir}/security/console.apps/draknetcenter <<EOF
USER=<user>
PROGRAM=/usr/sbin/draknetcenter
FALLBACK=false
SESSION=true
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS
%{_bindir}/net_applet
%{_bindir}/drakroam
%{_bindir}/draknetcenter
%{_sbindir}/drakhosts
%{_sbindir}/drakids
%{_sbindir}/draknetcenter
%{_sbindir}/draknetprofile
%{_sbindir}/draknfs
%{_sbindir}/drakroam
%{_sbindir}/draksambashare
%{_sbindir}/net_monitor
%{_prefix}/lib/libDrakX/network/ifw.pm
%{_prefix}/lib/libDrakX/network/monitor.pm
%config(noreplace) %{_sysconfdir}/pam.d/drakroam
%config(noreplace) %{_sysconfdir}/pam.d/draknetcenter
%config(noreplace) %{_sysconfdir}/security/console.apps/drakroam
%config(noreplace) %{_sysconfdir}/security/console.apps/draknetcenter
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


