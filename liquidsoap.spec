#
# spec file for liquidsoap
#
%ifarch x86_64
%define _host %{nil}
%define _build %{nil}
%endif

Name: liquidsoap
Version: 1.0.1
Release: 2%{?dist}
License: GPLv2
Group: Applications/Multimedia
Summary: Used for generating the stream of net radios written by the Savonet project
Source: http://downloads.sourceforge.net/project/savonet/${name}/${version}/%{name}-%{version}-full.tar.bz2
Source1: http://downloads.sourceforge.net/project/ocaml-magic/ocaml-magic/0.7/ocaml-magic-0.7.3.tar.gz 
Source2: liquidsoap.init-dist
URL: http://savonet.sourceforge.net/
Distribution: Fedora Core
Vendor: Savonet Team
Buildroot: %{_tmppath}/%{name}-%{version}-root
Patch0: liquidsoap-fedora-fixes.patch
Patch1: liquidsoap-fedora-fixes-nonfree.patch
Patch2: ogg_decoder.patch 
Patch3: generator.ml.patch
Patch4: generator.mli.patch
Requires(pre): shadow-utils
BuildRequires: automake
BuildRequires: file-devel
BuildRequires: ocaml
BuildRequires: libshout
BuildRequires: libshout-devel
BuildRequires: ocaml-findlib
BuildRequires: libao-devel
BuildRequires: portaudio-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: libsamplerate-devel
BuildRequires: ladspa-devel
BuildRequires: gavl-devel
BuildRequires: ocaml-xml-light-devel
BuildRequires: ocaml-pcre-devel
BuildRequires: ocaml-ocamlnet
BuildRequires: perl-XML-DOM
BuildRequires: python-devel
BuildRequires: soundtouch-devel
BuildRequires: xmltoman
BuildRequires: libX11-devel
BuildRequires: schroedinger-devel
BuildRequires: flac-devel
BuildRequires: liblo-devel
BuildRequires: ocaml-camomile-data
BuildRequires: ocaml-camomile-devel
BuildRequires: ocaml-camlidl
BuildRequires: dssi-devel
BuildRequires: gstreamer-devel
BuildRequires: ffmpeg-devel
BuildRequires: gstreamer-plugins-base-devel
#BuildRequires: ocaml-camlidl-devel

# Uncomment these if you wish to rebuild against Non-free libs
# See liquidsoap source: PACKAGES for which modules to build
# which is maintained in liquidsoap-fedora-fixes.patch
BuildRequires: lame-devel
BuildRequires: libmad-devel
BuildRequires: faac-devel
BuildRequires: faad2-devel
BuildRequires: taglib-devel
BuildRequires: libaacs-devel
BuildRequires: libaacplus-devel
Requires: libshout libogg libtheora libvorbis speex libao jack-audio-connection-kit portaudio alsa-lib pulseaudio-lib libsamplerate taglib ladspa gavl libmad libmp3lame0 faac faad2 liblo ocaml-camomile-data libaacplus

%description
Liquidsoap has tons of features, it's free and 
it's open-source! Liquidsoap lets you to describe 
your streams in a powerful and flexible way. 
Allowing arbitrarily deep-nested composition of streams,
it gives you more power than you need for creating
an original net radio. But liquidsoap is still very 
light and easy to use, in the Unix tradition of simple
strong components working together. 

%prep
%setup -q -n %{name}-%{version}-full
%setup -q -D -T -a 1 -c -n %{name}-%{version}-full/
# This is the 'free' patch, Comment this out for nonfree
#%patch0 -p1
# This is the 'nonfree' patch.  Uncomment this for nonfree
%patch1 -p1
echo $PATH
echo `env`

%patch2 -p1 
%patch3 -p1
%patch4 -p1

%build
echo `pwd`
PKG_CONFIG_PATH=%_libdir/pkgconfig/
export PKG_CONFIG_PATH
./bootstrap
%configure #--with-user=$(id -un) --with-group=$(id -gn)
make

%pre
getent group  liquidsoap >/dev/null || groupadd -r liquidsoap
getent passwd liquidsoap >/dev/null || \
    useradd -r -g liquidsoap -d /var/lib/liquidsoap -s /sbin/nologin \
    -c "User account for running the liquidsoap daemon" liquidsoap
exit 0

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT%{_initddir}
cp %SOURCE2 $RPM_BUILD_ROOT%{_initddir}/%{name}
mkdir -p $RPM_BUILD_ROOT%_localstatedir/{log,run}/%{name}

%post
if [ "$1" = 1 ]; then
chkconfig --add liquidsoap

fi
exit 0

%preun
if [ "$1" = 0 ]; then
service liquidsoap stop > /dev/null 2>&1
chkconfig --del liquidsoap
   if [ -n $(id -un liquidsoap 2>/dev/null) ]; then
      #delete user liquidsoap if it exists
      userdel liquidsoap
   fi
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
   service liquidsoap condrestart > /dev/null 2>&1
fi
exit 0 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root)
%attr(755,root,root) %{_initddir}/liquidsoap
%defattr(-,root,root) 
%{_bindir}/%{name}
%config /etc/%{name}/radio.liq.example
%config(noreplace) /etc/logrotate.d/%{name}
%{_libdir}/%{name}
%doc /usr/share/doc/%{name}-%{version}
%doc /usr/share/man/man1/%{name}.1.gz

#/usr/share/man/man1/liguidsoap.1.gz
%defattr(-,liquidsoap,liquidsoap)
%dir /var/log/%{name}
%dir /var/run/%{name}

%changelog
* Mon Feb 18 2013 Andrey Zarochentsev <andrey.zar@gmail.com> 1.0.1-2
- Rebuild  for version 1.0.1
- Add patch for ogg_decoder.ml from Samuel Mimram

* Wed Aug 1 2012 Chris Everest <chris@vinylproject.com> - 1.0.1-1
- Rebuild  for version 1.0.1
- Add support for systemd

* Mon Oct 17 2011 Chris Everest <chris@vinylproject.com> - 1.0.0-4
- Rebuild  for version 1.0.0

* Thu Sep 29 2011 Chris Everest <chris@vinylproject.com> - 1.0.0-3
- Build again for beta3
- Fix the init script to be SysV and Systemd friendly

* Mon Sep 26 2011 Chris Everest <chris@vinylproject.com> - 1.0.0-2
- Upgrade to 1.0.0-beta3
- Build for Fedora 15

* Thu Mar 17 2011 Chris Everest <chris@vinylproject.com> - 1.0.0-1
- Upgrade to 1.0.0-beta1

* Tue Feb 22 2011 Chris Everest <chris@vinylproject.com> - 0.9.3-1
- Upgrade to 0.9.3

* Tue Jul 28 2009 Chris Everest <chris@vinylproject.com> - 0.9.1-1
- Downloaded version 0.9.1, applied patches to remove soundtouch
- Added service init script
 
