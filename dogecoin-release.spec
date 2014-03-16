Name:           dogecoin-release       
Version:        1
Release:        1
Summary:        Dogecoin repository configuration

Group:          System Environment/Base 
License:        MIT

URL:            http://obsoleet.org/resources/dogecoin
Source0:        http://obsoleet.org/resources/dogecoin/RPM-GPG-KEY-dogecoin
Source1:        dogecoin.repo

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:      fedora-release >= 19

%description
This package contains the Dogecoin repository GPG key as well as configuration
for yum.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-dogecoin

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/dogecoin.repo

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Sun Jan 26 2014 Graham Forest <dogecoin@obsoleet.org> - 1-1
- Reset release
- Replace key
- s/bitcoin/dogecoin/g
- Only support fc19+

* Mon Dec 9 2013 Michael Hampton <bitcoin@ringingliberty.com> - 1-5
- New signature on GPG key

* Wed Aug 22 2012 Michael Hampton <bitcoin@ringingliberty.com> - 1-4
- Fedora specific build with unique filenames

* Fri Jul 27 2012 Michael Hampton <bitcoin@ringingliberty.com> - 1-1
- Initial Package
