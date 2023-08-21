%define vendor_name Microsemi
%define vendor_label microsemi
%define driver_name smartpqi

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 2.1.24_046
Release: 1%{?dist}
License: GPL

# Extracted from latest XS driver disk
Source0: microsemi-smartpqi-2.1.24_046.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{vendor_label}-%{driver_name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules EXTRA_CFLAGS+=-DKCLASS4C

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko


%changelog
* Mon Aug 21 2023 Gael Duperrey <gduperrey@vates.fr> - 2.1.24_046-1.1
- Update to version 2.1.24_046-1
- Synced from XS driver SRPM microsemi-smartpqi-2.1.24_046-1.xs8~2_1.src.rpm

* Wed May 10 2023 Gael Duperrey <gduperrey@vates.fr> - 2.1.22_040-1
- initial package, version 2.1.22_040-1

