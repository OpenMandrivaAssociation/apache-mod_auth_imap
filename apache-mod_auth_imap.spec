#Module-Specific definitions
%define mod_name mod_auth_imap
%define mod_conf A42_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Provides authentication against an IMAP mail server
Name:		apache-%{mod_name}
Version:	2.2.0
Release:	14
Group:		System/Servers
License:	GPL
URL:		http://ben.brillat.net/projects/mod_auth_imap/
Source0:	http://ben.brillat.net/files/projects/mod_auth_imap2/mod_auth_imap2-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= 2.2.0
Requires(pre):  apache >= 2.2.0
Requires:       apache-conf >= 2.2.0
Requires:       apache >= 2.2.0
BuildRequires:  apache-devel >= 2.2.0
BuildRequires:	file

%description
mod_auth_imap is an Apache module to provide authentication
against an IMAP mail server. The httpd.conf or .htaccess file can
specify server name and port of the desired IMAP server. It is
also compatible with stunnel for IMAP over SSL.

%prep

%setup -q -n mod_auth_imap2-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc CHANGELOG GPL.txt README examples/htaccess-example examples/httpd.conf-append-example
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-13mdv2012.0
+ Revision: 772558
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-12
+ Revision: 678259
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-11mdv2011.0
+ Revision: 587917
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-10mdv2010.1
+ Revision: 516043
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-9mdv2010.0
+ Revision: 406530
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-8mdv2009.1
+ Revision: 325540
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-7mdv2009.0
+ Revision: 234631
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-6mdv2009.0
+ Revision: 215529
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-5mdv2008.1
+ Revision: 181666
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-4mdv2008.0
+ Revision: 82516
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-3mdv2008.0
+ Revision: 65619
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-2mdv2007.1
+ Revision: 140607
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-1mdv2007.1
+ Revision: 79318
- Import apache-mod_auth_imap

* Mon Jul 03 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2.0-1mdv2007.0
- 2.2.0
- drop upstream patches; P0

* Wed Dec 21 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-1mdk
- initial Mandriva package

