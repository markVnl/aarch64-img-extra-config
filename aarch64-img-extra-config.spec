%define debug_package %{nil}

Name:           aarch64-img-extra-config
Version:        0.0.2
Release:        1%{?dist}
Summary:        Helper scripts and configs for aarch64 image
Group:          System Environment/Base
License:        GPLv2

Source0:        rootfs-expand
Source10:       10-devicetree.add
Source11:       10-devicetree.remove
Source12:       10-devicetree.install
Source20:       gubby-kernel.conf


# Requires for rootfs-expand
Requires:       cloud-utils-growpart e2fsprogs
%if 0%{?rhel}
# Requires for devicetree add/remove/install
Requires:       grubby
%endif

%description
Helper scripts and configs for aarch64 image
- /bin/rootfs-expand ;
  script to extend rootfs partition to max available size
%if 0%{?rhel} == 7 
- /etc/kernel/postinst.d/10-devicetree.add ;
  script to create/update link to dtb-<kernel-version>
- /etc/kernel/prerm.d/10-devicetree.remove ;
  script to remove/update link to dtb-<kernel-version>
- /etc/sysconfig/kernel
  Default configuration for grubby, apparently not populated elsewhere on aarch64
%endif
%if 0%{?rhel} == 8
- /lib/kernel/install.d/10-devicetree.install
  systemd kernel-install script for device tree
%endif

%prep

%build
echo OK

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/

%if 0%{?rhel} == 7 
mkdir -p %{buildroot}%{_sysconfdir}/kernel/postinst.d
install -m 0755 %{SOURCE10} %{buildroot}%{_sysconfdir}/kernel/postinst.d/
mkdir -p %{buildroot}%{_sysconfdir}/kernel/prerm.d
install -m 0755 %{SOURCE11} %{buildroot}%{_sysconfdir}/kernel/prerm.d/

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE20} %{buildroot}%{_sysconfdir}/sysconfig/kernel
%endif

%if 0%{?rhel} == 8
mkdir -p %{buildroot}/lib/kernel/install.d/
install -p -m 0755 %{SOURCE12} %{buildroot}/lib/kernel/install.d/
%endif

%clean
rm -rf %{buildroot}

%posttrans


%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/rootfs-expand
%if 0%{?rhel} == 7 
%attr(0755,root,root) %{_sysconfdir}/kernel/postinst.d/10-devicetree.add
%attr(0755,root,root) %{_sysconfdir}/kernel/prerm.d/10-devicetree.remove
%attr(0644,root,root) %{_sysconfdir}/sysconfig/kernel
%endif
%if 0%{?rhel} == 8
%attr(0755,root,root) /lib/kernel/install.d/10-devicetree.install
%endif

%changelog
* Sat May 22 2021 Mark Verlinde <mark.verlinde@gmail.com> 0.0.2-1
- Include systemd kernel-install script for device tree in el8,
  (It is no longer present in upstream uboot-tools)

* Fri May 22 2020 Mark Verlinde <mark.verlinde@gmail.com> 0.0.1-1
- Version for el8

* Sat Dec 29 2018 Mark Verlinde <mark.verlinde@gmail.com>
- Initial build
