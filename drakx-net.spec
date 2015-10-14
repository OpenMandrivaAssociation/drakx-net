%define drakxtools_ver 16.00

%define libname lib%{name}

%define gtk_files (connection_manager/gtk|signal_strength|drakroam|ifw|netcenter|drakconnect/edit|drakconnect/global).pm

Summary:	Mandriva network tools
Name:		drakx-net
Version:	2.23
Release:	1
Source0:	%{name}-%{version}.tar.xz
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		https://abf.io/omv_software/drakx-net
BuildArch:	noarch
BuildRequires:	intltool
Requires:	drakxtools >= %{drakxtools_ver}
Requires:	%{name}-text = %{version}
Requires:	%{libname} = %{version}
Requires:	netprofile >= 0.20
Requires:	perl-Gtk3
Conflicts:	drakxtools <= 10.4.83
Suggests:	net_monitor
Suggests:	networkmanager

%description
This package contains the OpenMandriva network tools.

%package text
Summary:	OpenMandriva network text tools
Group:		System/Configuration/Networking
Requires:	drakxtools-curses >= %{drakxtools_ver}
Requires:	%{libname} = %{version}
Conflicts:	drakxtools-curses <= 10.4.83
Conflicts:	mdkonline < 2.37

%description text
This package contains the Mandriva network tools that can be used in
text mode.

drakconnect: LAN/Internet connection configuration. It handles
ethernet, ISDN, DSL, cable, modem.

drakfirewall: simple firewall configurator

drakgw: internet connection sharing

drakproxy: proxies configuration

drakvpn: VPN configuration (openvpn, vpnc)

%package applet
Summary:	OpenMandriva network applet
Group:		System/Configuration/Networking
Requires:	%{name} = %{version}-%{release}

%description applet
This package contains the Mandriva network applet.

%package -n %{libname}
Summary:	OpenMandriva network tools library
Group:		System/Configuration/Networking
Requires:	drakxtools-backend >= %{drakxtools_ver}
# require perl-Net-Telnet for OpenVPN connections (#36126):
Requires:	perl-Net-Telnet
# Require crda, iw and wireless-regdb for CRDA domain settings (#47324)
Requires:	crda
Requires:	iw
Requires:	wireless-regdb
Conflicts:	drakxtools-backend <= 10.4.83

%description -n	%{libname}
This package contains the Mandriva network tools library.

%prep
%setup -q

%build
%make

%install
%makeinstall_std

(cd %{buildroot}; find usr/lib/libDrakX/network/ -type f -name '*.pm') | perl -ne 'm!/%{gtk_files}$! ? print STDERR "/$_" : print "/$_"' > %{name}-nogtk.list 2> %{name}-gtk.list

%find_lang %{name} %{name}.lang
cat %{name}-nogtk.list %{name}.lang > %{name}.list

%check
while read f; do
      grep Gtk3 %{buildroot}$f && exit 1
done < %{name}-nogtk.list
exit 0

%files -f %{name}-gtk.list
%doc NEWS
%{_bindir}/draknetcenter
%{_bindir}/draknetprofile
%{_bindir}/drakhosts
%{_bindir}/drakids
%{_bindir}/draknfs
%{_bindir}/drakroam
%{_bindir}/draksambashare
%{_datadir}/applications/draknetcenter.desktop
%{_prefix}/lib/libDrakX/icons/*.png
%{_datadir}/libDrakX/pixmaps/*.png
%{_libexecdir}/draknetcenter
%{_libexecdir}/draknetprofile
%{_libexecdir}/drakhosts
%{_libexecdir}/drakids
%{_libexecdir}/draknfs
%{_libexecdir}/drakroam
%{_libexecdir}/draksambashare
%{_datadir}/polkit-1/actions/org.openmandriva.draknetcenter.policy
%{_datadir}/polkit-1/actions/org.openmandriva.draknetprofile.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakhosts.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakids.policy
%{_datadir}/polkit-1/actions/org.openmandriva.draknfs.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakroam.policy
%{_datadir}/polkit-1/actions/org.openmandriva.draksambashare.policy
%{_datadir}/polkit-1/actions/com.redhat.initscripts.ifdown.policy
%{_datadir}/polkit-1/actions/com.redhat.initscripts.ifup.policy
%{_datadir}/polkit-1/actions/com.redhat.initscripts.vpn-start.policy
%{_datadir}/polkit-1/actions/com.redhat.initscripts.vpn-stop.policy
%{_datadir}/polkit-1/actions/org.openmandriva-x.set-netprofile.policy

%files text
%{_bindir}/drakconnect
%{_bindir}/drakgw
%{_bindir}/drakvpn
%{_bindir}/drakproxy
%{_bindir}/drakfirewall
%{_bindir}/drakinvictus
%{_libexecdir}/drakconnect
%{_libexecdir}/drakgw
%{_libexecdir}/drakvpn
%{_libexecdir}/drakproxy
%{_libexecdir}/drakfirewall
%{_libexecdir}/drakinvictus
%{_datadir}/polkit-1/actions/org.openmandriva.drakconnect.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakgw.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakvpn.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakproxy.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakfirewall.policy
%{_datadir}/polkit-1/actions/org.openmandriva.drakinvictus.policy

%files -n %{libname} -f %{name}.list
%dir %{_prefix}/lib/libDrakX/network/
%dir %{_prefix}/lib/libDrakX/network/connection
%dir %{_prefix}/lib/libDrakX/network/connection/isdn
%dir %{_prefix}/lib/libDrakX/network/connection/providers
%dir %{_prefix}/lib/libDrakX/network/drakconnect
%dir %{_prefix}/lib/libDrakX/network/vpn

%files applet
%{_bindir}/net_applet
%{_datadir}/applications/net_applet.desktop
%{_sysconfdir}/xdg/autostart/net_applet.desktop
