%define	major 1
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define staticdevelname %mklibname -d %{name} -s

Summary:	An API for audio analysis and feature extraction plugins
Name:		vamp-plugin-sdk
Version:	1.1b
Release:	%mkrel 5
License:	BSD
Group:		System/Libraries
URL:		http://www.vamp-plugins.org/
Source0:	http://downloads.sourceforge.net/vamp/vamp-plugin-sdk-%{version}.tar.gz
Patch0:		%{name}-1.1b-Makefile.patch
Patch1:		%{name}-1.1b-gcc43.patch
BuildRequires:	libsndfile-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Vamp is an API for C and C++ plugins that process sampled audio data to produce
descriptive output (measurements or semantic observations).

%package -n	%{libname}
Summary:	An API for audio analysis and feature extraction plugins library
Group:          System/Libraries

%description -n	%{libname}
Vamp is an API for C and C++ plugins that process sampled audio data to produce
descriptive output (measurements or semantic observations).

%package -n	%{develname}
Summary:	Development files (headers) for SLV2
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Requires:       pkgconfig

%description -n	%{develname}
Vamp is an API for C and C++ plugins that process sampled audio data to produce
descriptive output (measurements or semantic observations).

The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package -n	%{staticdevelname}
Summary:	Development files (headers) for SLV2
Group:		Development/C
Requires:	%{develname} = %{version}
Provides:	%{name}-static-devel = %{version}

%description -n	%{staticdevelname}
Vamp is an API for C and C++ plugins that process sampled audio data to produce
descriptive output (measurements or semantic observations).

The %{name}-static package contains library files for developing static
applications that use %{name}.

%prep

%setup -q -n %{name}-v%{version}
%patch0 -p1 -b .mk
%patch1 -p1 -b .gcc43

%build
export CXXFLAGS=$RPM_OPT_FLAGS

%make

%install
rm -rf %{buildroot}

# fix libdir
find . -name '*.pc.in' -exec sed -i 's|/lib|/%{_lib}|' {} ';'
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir}

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# create Makefile for examples
cd examples
echo CXXFLAGS=$RPM_OPT_FLAGS -fpic >> Makefile
echo bundle: `ls *.o` >> Makefile
echo -e "\t"g++ \$\(CXXFLAGS\) -shared -Wl,-Bsymbolic \
     -o vamp-example-plugins.so \
     *.o \$\(pkg-config --libs vamp-sdk\) >> Makefile
echo `ls *.cpp`: >> Makefile
echo -e "\t"g++ \$\(CXXFLAGS\) -c $*.cpp >> Makefile
echo clean: >> Makefile
echo -e "\t"-rm *.o *.so >> Makefile
# clean directory up so we can package the sources
make clean

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root,-)
%doc examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{staticdevelname}
%defattr(-,root,root,-)
%{_libdir}/*.a

