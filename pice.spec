#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
Summary:	PrivateICE Linux system level symbolic source debugger
Summary(pl):	PrivateICE - odpluskwiacz dzia³aj±cy w trybie j±dra
Name:		pice
Version:	0.99.8
%define		_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Development/Debuggers
Source0:	http://pice.sourceforge.net/%{name}_0_99_build8_src.tar.gz
Patch0:		%{name}-generic.patch
Patch1:		%{name}-newline.patch
URL:		http://pice.sf.net/
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	ncurses-devel
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PrivateICE (pICE) is a powerful kernel mode debugger that supports
device driver and kernel as well as application debugging on a single
LINUX machine.

%description -l pl
PrivateICE (pICE) jest potê¿nym odpluskwiaczem dzia³aj±cym w trybie
j±dra jak równie¿ odpluskwiacz aplikacji.

%package -n kernel-%{name}
Summary:	Kernel modules for PICE
Summary(pl):	Modu³ j±dra dla PICE
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod

%description -n kernel-%{name}
Kernel modules for PICE.

%description -n kernel-%{name} -l pl
Modu³ j±dra dla PICE.

%package -n kernel-smp-%{name}
Summary:	Kernel SMP modules for PICE
Summary(pl):	Modu³ j±dra SMP dla PICE
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-%{name}
Kernel SMP modules for PICE.

%description -n kernel-smp-%{name} -l pl
Modu³ j±dra SMP dla PICE.

%prep
%setup -q -c
%patch0 -p0
%patch1 -p1

%build
%{__make} -C loader \
	CFLAGS="%{rpmcflags} -I%{_includedir}/ncurses -Wall -fomit-frame-pointer -DLINUX"

cd module
%{__make} \
	MODCFLAGS="-Wall -c -fomit-frame-pointer -O2 -DMODULE -D__KERNEL__ -DLINUX -DEXPORT_SYMTAB -D__SMP__ -D__KERNEL_SMP=1"
mv pice.o pice-smp.o

%{__make} clean
%{__make} MODCFLAGS="-Wall -c -fomit-frame-pointer -O2 -DMODULE -D__KERNEL__ -DLINUX -DEXPORT_SYMTAB"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

install loader/loader	$RPM_BUILD_ROOT%{_sbindir}/pice-loader
install module/pice-smp.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/pice.o
install module/pice.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-%{name}
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver} %{_kernel_ver}

%postun -n kernel-%{name}
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver} %{_kernel_ver}

%post	-n kernel-smp-%{name}
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver}smp %{_kernel_ver}smp

%postun -n kernel-smp-%{name}
/sbin/depmod -a -F /boot/System.map-%{_kernel_ver}smp %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*

%files -n kernel-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/pice.o*

%files -n kernel-smp-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/pice.o*
