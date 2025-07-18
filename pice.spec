#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
%define		_rel	1
Summary:	PrivateICE Linux system level symbolic source debugger
Summary(pl.UTF-8):	PrivateICE - odpluskwiacz działający w trybie jądra
Name:		pice
Version:	0.99.8
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Development/Debuggers
Source0:	http://pice.sourceforge.net/%{name}_0_99_build8_src.tar.gz
# Source0-md5:	f00cc77f1f8739e321e4eaf42af021fb
Patch0:		%{name}-generic.patch
Patch1:		%{name}-newline.patch
URL:		http://pice.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.118
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PrivateICE (pICE) is a powerful kernel mode debugger that supports
device driver and kernel as well as application debugging on a single
LINUX machine.

%description -l pl.UTF-8
PrivateICE (pICE) jest potężnym odpluskwiaczem działającym w trybie
jądra jak również odpluskwiacz aplikacji.

%package -n kernel-%{name}
Summary:	Kernel modules for PICE
Summary(pl.UTF-8):	Moduł jądra dla PICE
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod

%description -n kernel-%{name}
Kernel modules for PICE.

%description -n kernel-%{name} -l pl.UTF-8
Moduł jądra dla PICE.

%package -n kernel-smp-%{name}
Summary:	Kernel SMP modules for PICE
Summary(pl.UTF-8):	Moduł jądra SMP dla PICE
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-%{name}
Kernel SMP modules for PICE.

%description -n kernel-smp-%{name} -l pl.UTF-8
Moduł jądra SMP dla PICE.

%prep
%setup -q -c
%patch -P0 -p0
%patch -P1 -p1

%build
%{__make} -C loader \
	CFLAGS="%{rpmcflags} -I/usr/include/ncurses -Wall -fomit-frame-pointer -DLINUX"

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
%depmod %{_kernel_ver}

%postun -n kernel-%{name}
%depmod %{_kernel_ver}

%post	-n kernel-smp-%{name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-%{name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*

%files -n kernel-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/pice.o*

%files -n kernel-smp-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/pice.o*
