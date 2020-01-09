Name: docbook-utils
Version: 0.6.14
Release: 24%{?dist}
Group: Applications/Text

Summary: Shell scripts for managing DocBook documents
URL: http://sources.redhat.com/docbook-tools/

License: GPLv2+

Requires: docbook-style-dsssl >= 1.72
Requires: docbook-dtds
Requires: perl-SGMLSpm >= 1.03ii
Requires: which grep gawk
Requires: text-www-browser

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl-SGMLSpm, openjade, docbook-style-dsssl

BuildArch: noarch
Source0: ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES/%{name}-%{version}.tar.gz
Source1: db2html
Source2: gdp-both.dsl
#We will ship newer version of docbook2man-spec.pl for better handling of docbook2man conversion
#You could check it at http://sourceforge.net/projects/docbook2x/
Source3: docbook2man-spec.pl

Obsoletes: stylesheets < %{version}-%{release}
Provides: stylesheets = %{version}-%{release}

Patch0: docbook-utils-spaces.patch
Patch1: docbook-utils-2ndspaces.patch
Patch2: docbook-utils-w3mtxtconvert.patch
Patch3: docbook-utils-grepnocolors.patch
Patch4: docbook-utils-sgmlinclude.patch
Patch5: docbook-utils-rtfmanpage.patch
Patch6: docbook-utils-papersize.patch
Patch7: docbook-utils-nofinalecho.patch

%description
This package contains scripts are for easy conversion from DocBook
files to other formats (for example, HTML, RTF, and PostScript), and
for comparing SGML files.

%package pdf
Requires: jadetex >= 2.5
Requires: docbook-utils = %{version}
Requires: tex(dvips)
License: GPL+
Group: Applications/Text
Obsoletes: stylesheets-db2pdf <= %{version}-%{release}
Provides: stylesheets-db2pdf = %{version}-%{release}
Summary: A script for converting DocBook documents to PDF format
URL: http://sources.redhat.com/docbook-tools/

%description pdf
This package contains a script for converting DocBook documents to
PDF format.

%prep
%setup -q
%patch0 -p1 -b .spaces
%patch1 -p1 -b .2ndspaces
%patch2 -p1 -b .w3mtxtconvert
%patch3 -p1 -b .grepnocolors
%patch4 -p1 -b .sgmlinclude
%patch5 -p1 -b .rtfman
%patch6 -p1 -b .papersize
%patch7 -p1 -b .finalecho

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir} --libdir=%{_libdir}
make %{?_smp_mflags}

%install
export DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install prefix=%{_prefix} mandir=%{_mandir} docdir=/tmp
for util in dvi html pdf ps rtf
do
	ln -s docbook2$util $RPM_BUILD_ROOT%{_bindir}/db2$util
	ln -s jw.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/db2$util.1
done
ln -s jw.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/docbook2txt.1
# db2html is not just a symlink, as it has to create the output directory
rm -f $RPM_BUILD_ROOT%{_bindir}/db2html
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/db2html
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/utils-%{version}/docbook-utils.dsl
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/utils-%{version}/helpers/docbook2man-spec.pl

rm -rf $RPM_BUILD_ROOT/tmp

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-,root,root,-)
%doc README COPYING TODO
%{_bindir}/jw
%{_bindir}/docbook2html
%{_bindir}/docbook2man
%{_bindir}/docbook2rtf
%{_bindir}/docbook2tex
%{_bindir}/docbook2texi
%{_bindir}/docbook2txt
%attr(0755,root,root) %{_bindir}/db2html
%{_bindir}/db2rtf
%{_bindir}/sgmldiff
%{_datadir}/sgml/docbook/utils-%{version}
%{_mandir}/*/db2dvi.*
%{_mandir}/*/db2html.*
%{_mandir}/*/db2ps.*
%{_mandir}/*/db2rtf.*
%{_mandir}/*/docbook2html.*
%{_mandir}/*/docbook2rtf.*
%{_mandir}/*/docbook2man.*
%{_mandir}/*/docbook2tex.*
%{_mandir}/*/docbook2texi.*
%{_mandir}/*/docbook2txt.*
%{_mandir}/*/jw.*
%{_mandir}/*/sgmldiff.*
%{_mandir}/*/*-spec.*

%files pdf
%defattr (-,root,root,-)
%{_bindir}/docbook2pdf
%{_bindir}/docbook2dvi
%{_bindir}/docbook2ps
%{_bindir}/db2dvi
%{_bindir}/db2pdf
%{_bindir}/db2ps
%{_mandir}/*/db2pdf.*
%{_mandir}/*/docbook2pdf.*
%{_mandir}/*/docbook2dvi.*
%{_mandir}/*/docbook2ps.*

%changelog
* Mon May 31 2010 Ondrej Vasik <ovasik@redhat.com> 0.6-14-24
- do not produce final echo, it causes some manpage noise
  with new perl(#587012)

* Tue Oct 27 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.14-23
- do not obsolete self

* Mon Oct 12 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.14-22
- fix url in pdf subpackage

* Wed Oct 07 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.14-21
- fix locale-based papersize selection (#527395)

* Thu Aug 27 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.14-20
- provide symlink manpage for docbook2txt

* Thu Aug 13 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.14-19
- add note about openjade limitation in rtf section of jw
  manpage(#516942)

* Fri Jul 24 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.14-18
- another quoted variable fixes for spaces in filenames
- use SGML_INCLUDE in man backend(upstream)
- change upstream URL to something useful
- escape dots and single quotes in column 1 in docbook2man-spec.pl

* Mon Jun 29 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.14-17
- fix pdf subpackage requires(to match TeXLive2008 provides)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 28 2008 Ondrej Vasik <ovasik@redhat.com> 0.6.14-15
- require grep,gawk, fix jw script to find SGML_BASE_DIR even
  with grep with colors(#473278), finish funcsynopsis patch
  drop

* Mon Sep 08 2008 Ondrej Vasik <ovasik@redhat.com> 0.6-14-14
- ship new version of docbook2man-spec.pl to avoid issues
  with the old one
- dropped funcsynopsis patch - docbook2man-spec.pl from
  tarball used no longer

* Thu Nov 22 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.14-13
- fix of w3m params while converting to txt

* Tue Nov 05 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.14-12
- Merge Review(#225705)
- corrected some other packaging guidelines issues

* Thu Nov 01 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.14-11
- rpmlint check
- fixed: dist tag, summary ended with dot, license tag,
  versioned provides/obsoletes + some cosmetic changes

* Fri Oct 12 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.14-10
- generalized text browser requirement(#174566)

* Tue Sep 18 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.14-9
- fixed typo in Source URL

* Mon May 21 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.14-8
- Added more fixes for handling spaces in directory name
- SGML_FILE variable is factored out of SGML_ARGUMENTS
- (changes taken from upstream)

* Tue Apr 24 2007 Petr Mejzlik <pmejzlik@redhat.com> 0.6.14-7
- add missing dist tag, bump release

* Tue Apr 24 2007 Petr Mejzlik <pmejzlik@redhat.com> 0.6.14-6
- Fixed a minor bug in processing of <funcsynopsisinfo> (bug #217649)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.14-5.1
- rebuild

* Thu Mar 09 2006 Florian La Roche <laroche@redhat.com>
- use 755 instead of 775 for /usr/bin/db2html

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com> 0.6.14-5
- Move dvi and ps tools into pdf sub-package (bug #174897).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Aug 19 2004 Tim Waugh <twaugh@redhat.com> 0.6.14-4
- Apply CVS patch to protect spaces in jw (bug #130329).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 11 2004 Tim Waugh <twaugh@redhat.com> 0.6.14-1
- 0.6.14.
- All patches integrated.

* Thu Nov 27 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-9
- Requires jadetex (bug #110755).

* Thu Nov 27 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-8
- Build requires docbook-style-dsssl (bug #110754).

* Tue Jun 10 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-7
- Fix manpage output: escape dots in column 1 (bug #97087).

* Tue May 27 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-6
- Rebuild.

* Fri May 23 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-5
- Build requires openjade.

* Thu May 22 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-4
- Require elinks (bug #91472).

* Thu May  1 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-3
- Move docbook2pdf man pages to pdf subpackage (bug #90041).

* Wed Apr 30 2003 Elliot Lee <sopwith@redhat.com> 0.6.13-2
- Add s/head -1/head -n 1/ patch to make ppc64 happy (among other things)

* Mon Mar 17 2003 Tim Waugh <twaugh@redhat.com> 0.6.13-1
- 0.6.13, fixing bug #86152.

* Fri Feb 14 2003 Elliot Lee <sopwith@redhat.com> 0.6.12-6
- tetex-dvips requirement should go on main package (not just pdf 
  subpackage) because docbook2ps requires dvips too.

* Wed Feb  5 2003 Tim Waugh <twaugh@redhat.com> 0.6.12-5
- Build requires perl-SGMLSpm (bug #83474).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.6.12-4
- rebuilt

* Mon Jan 13 2003 Tim Waugh <twaugh@redhat.com> 0.6.12-3
- Fixes from CVS.

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 0.6.12-2
- No longer need separate stylesheet for A4.
- Don't install files not packaged.

* Wed Oct 16 2002 Tim Waugh <twaugh@redhat.com> 0.6.12-1
- 0.6.12.

* Thu Jun 27 2002 Tim Waugh <twaugh@redhat.com> 0.6.11-2
- 0.6.11.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.6.10-5
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 0.6.10-4
- automated rebuild

* Mon May 20 2002 Tim Waugh <twaugh@redhat.com> 0.6.10-3
- Improvements for man page output.

* Fri May  3 2002 Tim Waugh <twaugh@redhat.com> 0.6.10-2
- Don't define graphic-default-extension in the stylesheet---it messes
  up PS+PDF output from the same source.

* Wed May  1 2002 Tim Waugh <twaugh@redhat.com> 0.6.10-1
- 0.6.10.
- No longer need automake files.
- No longer need '.', jw-custom, '@', pdf, nochunks, txt, '-o', manpage,
  sdata, help, ol, '-V', sgml_xml, excl, link, pagesize, or texinputs
  patches.

* Fri Apr 12 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-25
- Turned off use-id-as-filename in gdp-both.dsl.

* Fri Mar 22 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-24
- Pick up images from the right place (bug #61652).

* Wed Mar  6 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-23
- Add URL tags, and provide: stylesheets and stylesheets-pdf (bug #60226).

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-22
- Rebuild in new environment.

* Tue Feb  5 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-21
- Edited the wrong file when making the patch.. fix breakage introduced
  by trying to fix bug #58375.

* Tue Feb  5 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-20
- Fix docbook frontend (bug #51478).
- Make the old db2html script understand the .xml filename extension
  (bug #59194).
- Determine page size to use automatically from LC_PAPER (bug #58375).

* Fri Jan 25 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-19
- Require the DocBook DTDs.

* Tue Jan 22 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-18
- Fix bug #46913 again, since the last change broke it.

* Sun Jan 20 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-16
- Several more fixes that will be in the next upstream version.

* Sat Jan 19 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-15
- Support -V (bug #31518).

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.6.9-14
- automated rebuild

* Wed Jan  9 2002 Tim Waugh <twaugh@redhat.com> 0.6.9-13
- Fix generated man output for orderedlists.

* Mon Dec  3 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-12
- Fix generated man output for funcprototypes with more than one
  paramdef.

* Wed Nov 28 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-11
- Rebuild to fix man pages (bug #56449).

* Thu Nov 22 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-10
- Fix jw behaviour when executed with no parameter.
- Fix 'jw --help'.

* Wed Nov 14 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-9
- Actually apply the patch that makes man backend understand &minus;.
- Also don't redefine <comment> and <remark> for HTML output either.

* Tue Nov 13 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-8
- Default stylesheet: <comment> and <remark> as rationale markers
  probably isn't really appropriate for general use.
- Default stylesheet: larger top margin to make some RTF readers
  happy (bug #56011).
- Make man backend understand &minus;.
- Specfile cleanups (%%{_bindir}, %%{_docdir}).

* Mon Nov 12 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-7
- The fix for bug #53546 broke '--dsl none'.  Fix it.

* Fri Nov  2 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-6
- Explicit synopsis for each docbook2[xxx] command in the jw man page.
- Clean up all temporary files in pdf backend.

* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-5
- Fix ADDRESS element output (bug #50605).

* Fri Sep 28 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-4
- Adjust stylesheet so that it works with docbook-dsssl 1.72.
- Fix jw so that -o and -d can be used together (bug #53546).

* Thu Sep  6 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-3
- Fix txt backend so that it works.
- Fix jw so that it uses the HTML stylesheet for text backends.
- Use links if lynx isn't available, in txt backend.

* Mon Aug 13 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-2
- Larger bottom margin in gdp-both.dsl to fix RTF output (bug #49677).

* Tue Jul  3 2001 Tim Waugh <twaugh@redhat.com> 0.6.9-1
- 0.6.9.
- With --nochunks, send output to a file instead of stdout (bug #46913).

* Mon Jun  4 2001 Tim Waugh <twaugh@redhat.com> 0.6.8-2
- Make sure COPYING isn't installed as a symlink.

* Mon May 21 2001 Tim Waugh <twaugh@redhat.com> 0.6.8-1
- 0.6.8.

* Mon May 21 2001 Tim Waugh <twaugh@redhat.com> 0.6-14
- db2html: copy admon graphics to output directory (bug #40143).
- Require docbook-style-dsssl 1.64-2 for symbolic link used by db2html.
- db2html: handle arguments with spaces better.

* Sat Mar 24 2001 Tim Waugh <twaugh@redhat.com> 0.6-13
- Fix man pages (bug #32820).

* Mon Mar 12 2001 Tim Waugh <twaugh@redhat.com>
- Fix argument parsing in docbook2xxx (bug #31518).
- Fix argument passing in db2html (bug #31520).
- Fix pdf generation (bug #31524).

* Fri Feb 23 2001 Tim Waugh <twaugh@redhat.com>
- Allow the use of custom backends and frontends (bug #29067).

* Fri Feb 16 2001 Tim Waugh <twaugh@redhat.com>
- Use gdp-both.dsl as the default stylesheet.

* Mon Feb 12 2001 Tim Waugh <twaugh@redhat.com>
- REALLY only create output directory for db2html (duh).
- Handle filenames with dots in properly.

* Sun Feb 11 2001 Tim Waugh <twaugh@redhat.com>
- Only create output directory for db2html (bug #27092). (docbook2html
  does not create an output directory in the upstream version, but
  the compatibility script has been made to do so.)

* Mon Jan 22 2001 Tim Waugh <twaugh@redhat.com>
- Move the jadetex requirement to the -pdf subpackage.

* Tue Jan 16 2001 Tim Waugh <twaugh@redhat.com>
- Put output files in new directory instead of current directory.

* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- Don't play so many macro games.
- Be sure to own utils directory.

* Fri Jan 12 2001 Tim Waugh <twaugh@redhat.com>
- Split off docbook2pdf into subpackage for dependency reasons.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Change group.
- Use %%{_mandir} and %%{_prefix}.
- db2* symlinks.
- Obsolete stylesheets (and -db2pdf).
- Change Copyright: to License:.
- Remove Packager: line.
- Reword description.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Based on Eric Bischoff's new-trials packages.
