Name:           cpuminer
Version:        2.3.3
Release:        1%{?dist}
Summary:        CPU miner for Litecoin and Bitcoin

License:        GPLv2
URL:            https://github.com/pooler/%{name}
Source0:        https://github.com/pooler/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.sysconfig

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires:  systemd
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libcurl-devel


%description
This is a multi-threaded CPU miner for Litecoin and Bitcoin,
which is a fork of Jeff Garzik's reference cpuminer.


%prep
%setup -q


%build
NOCONFIGURE=yes ./autogen.sh
%configure
make %{?_smp_mflags}


%install
%make_install
install -D -m644 -p %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m644 -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null ||
        useradd -r -g %{name} -s /sbin/nologin \
        -c "%{name} daemon (minerd)" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%doc AUTHORS ChangeLog COPYING LICENSE NEWS README
%{_bindir}/minerd
%{_unitdir}/%{name}.service
%{_mandir}/man1/minerd.1.gz
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}


%changelog
* Sun Mar 16 2014 Graham Forest <vitaminmoo@wza.us> 2.3.3-1
- Version bump
- Fix github url for spectool
- Add upstream manpage

* Sat Feb 22 2014 Graham Forest <vitaminmoo@wza.us> 2.3.2-3
- Move to systemd, misc spec cleanup

* Wed Feb  5 2014 Graham Forest <vitaminmoo@wza.us> 2.3.2-2
- Rename user-facing elements from minerd to cpuminer

* Sun Feb  2 2014 Graham Forest <vitaminmoo@wza.us> 2.3.2-1
- Initial release
