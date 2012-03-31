#
# Conditional build:
%bcond_with	tests		# build with tests

%define snapshot d525a9bab875
%define snapdate 20110830
Summary:	PAM module for One-time passcode support using open standards
Name:		pam-pam_google-authenticator
Version:	0
Release:	0.3.%{snapdate}.hg%{snapshot}
License:	ASL 2.0
URL:		http://code.google.com/p/google-authenticator/
# hg archive -r ${snapshot} %{name}-0.%{snapdate}.hg%{snapshot}.tar.gz
#Source0:        %{name}-0.%{snapdate}.hg%{snapshot}.tar.gz
Group:		Libraries
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/google-authenticator/google-authenticator-0.20110830.hgd525a9bab875.tar.gz/82b01c66812d1a2ceef51c0e375c18f3/google-authenticator-0.20110830.hgd525a9bab875.tar.gz
# Source0-md5:	82b01c66812d1a2ceef51c0e375c18f3
Patch1:		0001-Add-no-drop-privs-option-to-manage-secret-files-as-r.patch
Patch2:		0002-Allow-expansion-of-PAM-environment-variables-in-secr.patch
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
%setup -q -n google-authenticator-%{version}.%{snapdate}.hg%{snapshot}
%patch1 -p1
%patch2 -p1

%build
%{__make} -C libpam \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="-ldl"

%if %{with tests}
cd libpam
./pam_google_authenticator_unittest
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib}/security,%{_bindir}}
cd libpam
install -p pam_google_authenticator.so $RPM_BUILD_ROOT/%{_lib}/security
install -p google-authenticator $RPM_BUILD_ROOT%{_bindir}/google-authenticator

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc libpam/FILEFORMAT libpam/README libpam/totp.html
%attr(755,root,root) /%{_lib}/security/pam_google_authenticator.so
%attr(755,root,root) %{_bindir}/google-authenticator
