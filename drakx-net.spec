%define name drakx-net
%define version 0.53
%define release %mkrel 1
%define drakxtools_ver 10.15

%define libname lib%{name}

%define gtk_files (connection_manager|drakroam|ifw|monitor|netcenter|drakconnect/edit|drakconnect/global).pm

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
Requires: drakxtools >= %{drakxtools_ver}
Requires: %{name}-text = %{version}
Requires: %{libname} = %{version}
Requires: netprofile
Requires: perl-Gtk2 >= 1.154
Requires: usermode-consoleonly >= 1.92-4mdv2008.0
Conflicts: drakxtools <= 10.4.83

%description
This package contains the Mandriva network tools.

net_applet: applet to check network connection

net_monitor: connection monitoring

%package text
Summary: Mandriva network text tools
Group: System/Configuration/Networking
Requires: drakxtools-curses >= %{drakxtools_ver}
Requires: %{libname} = %{version}
Conflicts: drakxtools-curses <= 10.4.83
Conflicts: mdkonline < 2.37

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
Requires: drakxtools-backend >= %{drakxtools_ver}
# require perl-Net-Telnet for OpenVPN connections (#36126):
Requires: perl-Net-Telnet
Conflicts: drakxtools-backend <= 10.4.83

%description -n	%{libname}
This package contains the Mandriva network tools library.

%prep
%setup -q

%build
%make

%install
rm -rf %{buildroot}
%makeinstall_std

(cd %{buildroot}; find usr/lib/libDrakX/network/ -type f -name '*.pm') | perl -ne 'm!/%{gtk_files}$! ? print STDERR "/$_" : print "/$_"' > %{name}-nogtk.list 2> %{name}-gtk.list

%find_lang %{name}
cat %{name}-nogtk.list %{name}.lang > %{name}.list

# consolehelper config
# ask for user password
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/draknetcenter

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps/

ln -sf %{_sysconfdir}/pam.d/mandriva-console-auth %{buildroot}%{_sysconfdir}/pam.d/draknetcenter

cat > %{buildroot}%{_sysconfdir}/security/console.apps/draknetcenter <<EOF
USER=<user>
PROGRAM=/usr/sbin/draknetcenter
FALLBACK=false
SESSION=true
EOF

# consolehelper config
# ask for root password
for pak in drakconnect drakgw drakproxy drakvpn drakhosts; do
        ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/$pak
        ln -sf %{_sysconfdir}/pam.d/mandriva-simple-auth %{buildroot}%{_sysconfdir}/pam.d/$pak
        cat > %{buildroot}%{_sysconfdir}/security/console.apps/$pak <<EOF
USER=root
PROGRAM=/usr/sbin/$pak
FALLBACK=false
SESSION=true
EOF
done

%check
while read f; do
      grep Gtk2 %{buildroot}$f && exit 1
done < %{name}-nogtk.list
exit 0

%clean
rm -rf %{buildroot}

%files -f %{name}-gtk.list
%defattr(-,root,root)
%doc NEWS
%{_bindir}/net_applet
%{_bindir}/drakroam
%{_bindir}/draknetcenter
%{_bindir}/drakhosts
%{_sbindir}/drakhosts
%{_sbindir}/drakids
%{_sbindir}/draknetcenter
%{_sbindir}/draknetprofile
%{_sbindir}/draknfs
%{_sbindir}/drakroam
%{_sbindir}/draksambashare
%{_sbindir}/net_monitor
%config(noreplace) %{_sysconfdir}/pam.d/drakroam
%config(noreplace) %{_sysconfdir}/pam.d/draknetcenter
%config(noreplace) %{_sysconfdir}/pam.d/drakhosts
%config(noreplace) %{_sysconfdir}/security/console.apps/drakroam
%config(noreplace) %{_sysconfdir}/security/console.apps/draknetcenter
%config(noreplace) %{_sysconfdir}/security/console.apps/drakhosts
%{_sysconfdir}/X11/xinit.d/??net_applet
%{_datadir}/applications/net_applet.desktop
%{_datadir}/autostart/net_applet.desktop
%{_datadir}/gnome/autostart/net_applet.desktop
%{_prefix}/lib/libDrakX/icons/*.png
%{_datadir}/libDrakX/pixmaps/*.png

%files text
%config(noreplace) %{_sysconfdir}/pam.d/drakconnect
%config(noreplace) %{_sysconfdir}/pam.d/drakgw
%config(noreplace) %{_sysconfdir}/pam.d/drakproxy
%config(noreplace) %{_sysconfdir}/pam.d/drakvpn
%config(noreplace) %{_sysconfdir}/security/console.apps/drakconnect
%config(noreplace) %{_sysconfdir}/security/console.apps/drakgw
%config(noreplace) %{_sysconfdir}/security/console.apps/drakproxy
%config(noreplace) %{_sysconfdir}/security/console.apps/drakvpn
%{_bindir}/drakconnect
%{_bindir}/drakgw
%{_bindir}/drakvpn
%{_bindir}/drakproxy
%{_sbindir}/drakconnect
%{_sbindir}/drakfirewall
%{_sbindir}/drakgw
%{_sbindir}/drakinvictus
%{_sbindir}/drakproxy
%{_sbindir}/drakvpn

%files -n %{libname} -f %{name}.list
%defattr(-,root,root)
%dir %{_prefix}/lib/libDrakX/network/
%dir %{_prefix}/lib/libDrakX/network/connection
%dir %{_prefix}/lib/libDrakX/network/drakconnect/
%dir %{_prefix}/lib/libDrakX/network/vpn
