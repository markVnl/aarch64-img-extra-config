%define debug_package %{nil}

Name:           aarch64-img-extra-config
Version:        0.0.1
Release:        1%{?dist}
Summary:        Helper scripts and configs for aarch64 image
Group:          System Environment/Base
License:        GPLv2

Source0:        rootfs-expand
Source10:       10-devicetree.add
Source11:       10-devicetree.remove
Source20:       gubby-kernel.conf

# Requires for rootfs-expand
Requires:       cloud-utils-growpart e2fsprogs
%if 0%{?rhel} == 7
# Requires for devicetree add/remove
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

%changelog
* Fri May 22 2020 Mark Verlinde <mark.verlinde@gmail.com>
- Version for el8
* Sat Dec 29 2018 Mark Verlinde <mark.verlinde@gmail.com>
- Initial build
