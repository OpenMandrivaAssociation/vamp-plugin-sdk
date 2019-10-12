%define	major 2
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%define staticdevelname %mklibname -d %{name} -s

Summary:	An API for audio analysis and feature extraction plugins
Name:		vamp-plugin-sdk
Version:	2.8
Release:	1
License:	BSD
Group:		System/Libraries
URL:		http://www.vamp-plugins.org/
Source0:	%{name}-{version}-vamp-plugin-sdk-%{version}.tar.gz
#mirror:	https://github.com/c4dm/vamp-plugin-sdk/releases
#Patch0:         %{name}-2.4-libdir.patch
BuildRequires:	pkgconfig(sndfile)

%description
Vamp is an API for C and C++ plugins that process sampled audio data to produce
descriptive output (measurements or semantic observations).

%package -n	%{libname}
Summary:	An API for audio analysis and feature extraction plugins library
Group:		System/Libraries

%description -n	%{libname}
Vamp is an API for C and C++ plugins that process sampled audio data to produce
descriptive output (measurements or semantic observations).

%package -n	%{develname}
Summary:	Development files (headers) for SLV2
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Requires:	pkgconfig

%description -n	%{develname}
Vamp is an API for C and C++ plugins that process sampled audio data to produce
descriptive output (measurements or semantic observations).

The %{name}-devel package contains libraries
and header files for developing
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

%setup -q -n %{name}-%{name}-v%{version}
#patch0 -p1 -b .libdir
sed -i 's|/lib/vamp|/%{_lib}/vamp|g' src/vamp-hostsdk/PluginHostAdapter.cpp
sed -i 's|/lib/|/%{_lib}/|g' src/vamp-hostsdk/PluginLoader.cpp

%build
./configure --prefix=/usr \
	    --libdir=%{_libdir} \
	    --bindir=%{_bindir} \
	    --sbindir=%{_sbindir} \
	    --includedir=%{_includedir}
#make
%make

%install
# fix libdir
find . -name '*.pc.in' -exec sed -i 's|/lib|/%{_lib}|' {} ';'
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir}

find %{buildroot} -name '*.la' -exec rm -f {} ';'

# create Makefile for examples
cd examples
echo CXXFLAGS=%{optflags} -fpic >> Makefile
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

%files -n %{libname}
%doc COPYING README
%{_libdir}/*.so.*

%files -n %{develname}
%doc examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/vamp/*
%{_bindir}/vamp-rdf-template-generator
%{_bindir}/vamp-simple-host
%{_libdir}/pkgconfig/*.pc

%files -n %{staticdevelname}
%{_libdir}/*.a
