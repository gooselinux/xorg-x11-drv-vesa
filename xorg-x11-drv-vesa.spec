%define tarball xf86-video-vesa
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 vesa video driver
Name:      xorg-x11-drv-vesa
Version:   2.3.0
Release:   1%{?dist}
URL:       http://www.x.org
Source0:   http://xorg.freedesktop.org/releases/individual/driver/%{tarball}-%{version}.tar.bz2
License: MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-sdk >= 1.4.99.1-0.15
#BuildRequires: autoconf automake libtool

Requires:  xorg-x11-server-Xorg >= 1.4.99.1

Patch0: vesa-refuse-kms.patch
Patch1: vesa-avoid-24bpp.patch

%description 
X.Org X11 vesa video driver.

%prep
%setup -q -n %{tarball}-%{version}

%patch0 -p1 -b .nokms
%patch1 -p1 -b .24bpp

%build
#autoreconf -v --install || exit 1
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/vesa_drv.so
%{_mandir}/man4/vesa.4*

%changelog
* Tue Jun 01 2010 Adam Jackson <ajax@redhat.com> 2.3.0-1
- vesa 2.3.0
- vesa-avoid-24bpp.patch: Avoid 24bpp if 16bpp is available, ugly workaround
  for an xserver crash with virt (#555221)

* Thu May 13 2010 Ben Skeggs <bskeggs@redhat.com> 2.2.1-2
- refuse to load if KMS driver is active

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.2.1-1.1
- Rebuilt for RHEL 6

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 2.2.1-1
- vesa 2.2.1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 2.2.0-3.1
- ABI bump

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Adam Jackson <ajax@redhat.com> 2.2.0-2
- Check VBE PanelID if DDC fails.

* Tue Feb 17 2009 Adam Jackson <ajax@redhat.com> 2.2.0-1
- vesa 2.2.0

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.1.0-1
- Update to new upstream release

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.0.0-2
- bump for new server API

* Tue Jul 01 2008 Adam Jackson <ajax@redhat.com> 2.0.0-1
- vesa 2.0.0

* Tue Apr 29 2008 Adam Jackson <ajax@redhat.com> 1.3.0-15.20080404
- vesa-1.9-32bpp-dammit.patch: Prefer 24+32 instead of 24+24. (#427383)

* Fri Apr 04 2008 Adam Jackson <ajax@redhat.com> 1.3.0-14.20080404
- Today's git snapshot for FTBFS and other.  (#440720)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.0-13.20071113
- Autorebuild for GCC 4.3

* Tue Jan 08 2008 Adam Jackson <ajax@redhat.com> 1.3.0-12.20071113
- Rebuild for new ABI.

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 1.3.0-11.20071113
- Update to git snapshot for pciaccess goodness.
- Rip out legacy framebuffer support.

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1.3.0-10
- Rebuild for ppc toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.3.0-9
- Update Requires and BuildRequires.

* Thu May 31 2007 Adam Jackson <ajax@redhat.com> 1.3.0-8
- vesa-1.3.0-mode-heuristics.patch: Fix a typo that would crash on
  some cards. (#241491)

* Wed May 09 2007 Adam Jackson <ajax@redhat.com> 1.3.0-6
- Re-add the sync range hack. (#235066)

* Tue Mar 20 2007 Adam Jackson <ajax@redhat.com> 1.3.0-5
- vesa-1.3.0-mode-heuristics.patch: If strict intersection of VBE and EDID
  modes leaves no modes remaining after validation, try again with just
  range and VBE checks.  Replaces earlier range-hack and validmode patches.

* Tue Feb 27 2007 Adam Jackson <ajax@redhat.com> 1.3.0-4
- vesa-1.3.0-range-hack.patch: Work around broken ATI video BIOSes.
- Disown the module dir
- Fix the License

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.3.0-3
- ExclusiveArch -> ExcludeArch

* Wed Jan 24 2007 Adam Jackson <ajax@redhat.com> 1.3.0-2
- vesa-1.2.1-validmode.patch: Strictly limit runtime modes to the intersection
  of the BIOS and DDC lists, if a DDC list exists; fixes cases where we'd
  choose 1600x1200 on 1680x1050 panel.  Conversely, be more forgiving when
  validating the resulting set against the sync ranges; fixes 640x480 syndrome
  when the monitor has broken DDC.  Don't be deceived though, vesa still sucks.

* Mon Dec 4 2006 Adam Jackson <ajax@redhat.com> 1.3.0-1
- Update to 1.3.0
- vesa-1.2.1-validmode.patch: Implement a ValidMode driver hook, which rejects
  modes not present in the BIOS or outside the capability of the monitor.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.2.1-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-3
- vesa-1.2.1-fix-shadowfb.patch: Fix massive performance regression relative
  to FC5.

* Fri Jul 28 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-2
- vesa-1.2.1-randr-crash.patch: Fix a RANDR crash.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.2.1-1.1
- rebuild

* Sat Jun 17 2006 Mike A. Harris <mharris@redhat.com> 1.2.1-1
- Updated to version 1.2.1 for X11R7.1 server.

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-2
- Build on ppc64

* Tue May 30 2006 Adam Jackson <ajackson@redhat.com> 1.2.0-1
- Update to 1.2.0 from 7.1.

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1.3-1
- Updated xorg-x11-drv-vesa to version 1.0.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.1.2-1
- Updated xorg-x11-drv-vesa to version 1.0.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated xorg-x11-drv-vesa to version 1.0.1 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-vesa to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Tue Oct 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64 ia64 ppc alpha sparc sparc64

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for vesa video driver generated automatically
  by my xorg-driverspecgen script.
