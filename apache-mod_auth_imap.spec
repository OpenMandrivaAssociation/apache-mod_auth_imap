#Module-Specific definitions
%define mod_name mod_auth_imap
%define mod_conf A42_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Provides authentication against an IMAP mail server
Name:		apache-%{mod_name}
Version:	2.2.0
Release:	%mkrel 2
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}/var/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG GPL.txt README examples/htaccess-example examples/httpd.conf-append-example
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*


