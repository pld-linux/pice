%define         _kernel_ver     %(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define         _kernel_ver_str %(echo %{_kernel_ver} | sed s/-/_/g)
%define         smpstr          %{?_with_smp:-smp}
%define         smp             %{?_with_smp:1}%{!?_with_smp:0}

Summary:	PrivateICE Linux system level symbolic source debugger
Summary(pl):	PrivateICE - odpluskwiacz dzia³aj±cy w trybie j±dra
Name:		pice
Version:	0.99.8
Release:	1@%{_kernel_ver_str}
License:	GPL
Group:		Development/Debuggers
Source0:	http://pice.sourceforge.net/%{name}_0_99_build8_src.tar.gz
Patch0:		%{name}-generic.patch
URL:		http://pice.sf.net/
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	%{kgcc_package}
BuildRequires:	ncurses-devel
%{?_with_smp:Obsoletes: kernel-net-%{_orig_name}}
Prereq:         /sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_%{?_with_smp:smp}%{!?_with_smp:up}}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PrivateICE (pICE) is a powerful kernel mode debugger that supports
device driver and kernel as well as application debugging on a single
LINUX machine.

%description -l pl
PrivateICE (pICE) jest potê¿nym odpluskwiaczem dzia³aj±cym w trybie
j±dra jak równie¿ odpluskwiacz aplikacji.

%prep
%setup -q -c
%patch0 -p0

%build
%{__make} -C loader \
	CFLAGS="%{rpmcflags} -I%{_includedir}/ncurses -Wall -fomit-frame-pointer -DLINUX" \
	CC="%{__cc}"

%{__make} -C module \
	CC="%{kgcc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

install loader/loader	$RPM_BUILD_ROOT%{_sbindir}/pice-loader
install module/pice.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
/lib/modules/*/misc/*.o
