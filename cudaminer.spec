Name:           cudaminer
Version:        2014.02.28
Release:        1%{?dist}
Summary:        CUDA accelerated mining application for AltCoins

%define dashver %(echo %{version} | tr . -)

License:        GPLv3
URL:            https://github.com/cbuchner1/CudaMiner
Source0:        https://github.com/cbuchner1/CudaMiner/archive/%{dashver}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.sysconfig
ExclusiveArch:  x86_64

# The space-cadets at nVidia have libcudart.so dynamically loading
# libcuda.so (unversioned) in a way that is not normal dynamic linking.
# As Fedora's xorg-x11-drv-nvidia only contains libcuda.so.1, we
# have to hard-depend on xorg-x11-drv-nvidia-devel for the unversioned
# libcuda.so file to exist at runtime
Requires:       xorg-x11-drv-nvidia-devel
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires:  systemd
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  cuda-core-5-5
BuildRequires:  cuda-headers-5-5
BuildRequires:  cuda-core-libs-5-5

%description
CudaMiner is a CUDA accelerating mining application for AltCoin
mining with nVidia cards.

%prep
%setup -q -n CudaMiner-%(echo %{version} | tr . -)


%build
# nvcc doesn't support pipe, which gets aggressively injected everywhere
# substitute our own lame cflags
RPM_OPT_FLAGS=${RPM_OPT_FLAGS/-pipe}
export RPM_OPT_FLAGS
export CFLAGS=-O3
export CXXFLAGS=-O3

# the included configure script is jacked in various ways, regenerate it
./autogen.sh

%configure --with-cuda=/usr/local/cuda-5.5
make %{?_smp_mflags} LIBS=-Wl,-rpath,/usr/local/cuda-5.5/lib64


%install
%make_install
install -D -m644 -p %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m644 -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null ||
        useradd -r -g %{name} -s /sbin/nologin \
        -c "%{name} daemon" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%doc README.txt LICENSE.txt ChangeLog
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}


%changelog
* Sun Mar 16 2014 Graham Forest <vitaminmoo@wza.us> 2014.02.28-1
- Version bump
- Fix source URL for spectool
- ExclusiveArch x86_64, as there's no cuda repo for i386

* Sat Feb 22 2014 Graham Forest <vitaminmoo@wza.us> 2014.02.18-1
- Initial package
