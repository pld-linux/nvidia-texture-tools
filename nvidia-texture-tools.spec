#
# Conditional build:
%bcond_with	cuda	# CUDA (GPU-accelerated compression) support (req. NVIDIA proprietary libs)
#
Summary:	NVIDIA Texture Tools
Summary(pl.UTF-8):	NVIDIA Texture Tools - narzędzia NVidii do tekstur
Name:		nvidia-texture-tools
Version:	2.0.8
Release:	2
License:	MIT
Group:		Libraries
#Source0Download: http://code.google.com/p/nvidia-texture-tools/downloads/list
Source0:	http://nvidia-texture-tools.googlecode.com/files/%{name}-%{version}-1.tar.gz
# Source0-md5:	7449c95ca1583b512561c83c5a5f401c
Patch0:		%{name}-posh_types.patch
URL:		http://code.google.com/p/nvidia-texture-tools/
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
%{?with_cuda:BuildRequires:	cg-devel}
BuildRequires:	cmake >= 2.6.0
%{?with_cuda:BuildRequires:	cudatoolkit-devel}
BuildRequires:	glew-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
#BuildRequires:	maya-devel ?
BuildRequires:	qt4-build
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The NVIDIA Texture Tools is a collection of image processing and
texture manipulation tools, designed to be integrated in game tools
and asset conditioning pipelines.

The primary features of the library are mipmap and normal map
generation, format conversion and DXT compression.

DXT compression is based on Simon Brown's squish library.
%if %{with cuda}
This library also contains an alternative GPU-accelerated compressor
that uses CUDA and is one order of magnitude faster.
%endif

%description -l pl.UTF-8
NVIDIA Texture Tools to zestaw narzędzi do przetwarzania obrazu i
obróbki tekstur, przeznaczonych do integrowania w narzędziach do
tworzenia gier oraz optymalizacji (w szczególności technice asset
conditioning).

Główne możliwości biblioteki to generowanie danych mipmap i normal
map, konwersja formatów oraz kompresja DXT.

Kompresja DXT jest oparta na bibliotece squish Simona Browna.
%if %{with cuda}
Ta biblioteka dodatkowo zawiera alternatywny kompresor akcelerowany
przez GPU, wykorzystujący CUDA w celu przyspieszenia o rząd wielkości.
%endif

%package devel
Summary:	Header file for NVIDIA Texture Tools library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki NVIDIA Texture Tools
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header file for NVIDIA Texture Tools library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki NVIDIA Texture Tools.

%prep
%setup -q -n %{name}
%patch -P0 -p1

# use arch dependent libdir
%{__sed} -i 's,DESTINATION lib,DESTINATION %{_lib},' src/nv*/CMakeLists.txt

%build
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_C_FLAGS_RELEASE="-DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELEASE="-DNDEBUG" \
	-DCMAKE_VERBOSE_MAKEFILE=1 \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DNVTT_SHARED=1

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NVIDIA_Texture_Tools_{LICENSE,README}.txt
%attr(755,root,root) %{_bindir}/nvassemble
%attr(755,root,root) %{_bindir}/nvcompress
%attr(755,root,root) %{_bindir}/nvdecompress
%attr(755,root,root) %{_bindir}/nvddsinfo
%attr(755,root,root) %{_bindir}/nvimgdiff
%attr(755,root,root) %{_bindir}/nvzoom
%attr(755,root,root) %{_libdir}/libnvcore.so
%attr(755,root,root) %{_libdir}/libnvmath.so
%attr(755,root,root) %{_libdir}/libnvimage.so
%attr(755,root,root) %{_libdir}/libnvtt.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/nvtt
