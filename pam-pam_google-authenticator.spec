# TODO
# - re-check validity of patches (drop/update/upstreamify)
#
# Conditional build:
%bcond_without	tests		# build with tests

Summary:	PAM module for One-time passcode support using open standards
Name:		pam-pam_google-authenticator
Version:	1.09
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/google/google-authenticator-libpam/archive/%{version}/google-authenticator-libpam-%{version}.tar.gz
# Source0-md5:	c0a5624f53d64f851775fe7e94732651
URL:		https://github.com/google/google-authenticator-libpam
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	qrencode-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Google Authenticator package contains a pluggable authentication
module (PAM) which allows login using one-time passcodes conforming to
the open standards developed by the Initiative for Open Authentication
(OATH) (which is unrelated to OAuth).

Passcode generators are available (separately) for several mobile
platforms.

These implementations support the HMAC-Based One-time Password (HOTP)
algorithm specified in RFC 4226 and the Time-based One-time Password
(TOTP) algorithm currently in draft.

%prep
%setup -q -n google-authenticator-libpam-%{version}

%build
%{__aclocal} -I build
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--libdir=/%{_lib}
%{__make} %{?with_tests:check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_google_authenticator.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/google-authenticator

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc FILEFORMAT README.md totp.html
%attr(755,root,root) /%{_lib}/security/pam_google_authenticator.so
%attr(755,root,root) %{_bindir}/google-authenticator
%{_mandir}/man1/google-authenticator.1*
%{_mandir}/man8/pam_google_authenticator.8*
