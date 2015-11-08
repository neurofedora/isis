%global commit c76e32f08eb1fbe44ec1ea5c306c1f7d2c2a2900
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           isis
Version:        0.7.9
Release:        1%{?dist}
Summary:        Framework to access a large variety of image processing libraries

License:        GPLv3+
URL:            https://github.com/isis-group/isis
Source0:        https://github.com/isis-group/isis/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# https://github.com/isis-group/isis/pull/72
Patch0:         0001-cmake-add-multiarch-support.patch
Patch1:         0002-cmake-install-ISISConfig.cmake-into-lib-dependent-lo.patch
BuildRequires:  git-core
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  fftw-devel
BuildRequires:  libtiff-devel
# ISIS_ITK adapter
BuildRequires:  InsightToolkit-devel
# ISIS_QT4 adapter
BuildRequires:  qt4-devel
# IOPLUGIN_PNG plugin
BuildRequires:  libpng12-devel
# ISIS_IOPLUGIN_COMP plugin
BuildRequires:  bzip2-devel zlib-devel
# ISIS_IOPLUGIN_COMP_LZMA plugin
BuildRequires:  xz-devel
# ISIS_APPS_CALC tool
BuildRequires:  muParser-devel
Recommends:     %{name}-tools
Suggests:       %{name}-applications

%description
The ISIS project aims to provide a framework to access a large variety
of image processing libraries written in different programming
languages and environments.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}
Requires:       cmake%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tools
Summary:        Tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Tools for %{name}. This package includes:

* isisdump - Dumps the meta data informations from an image file as seen
             by the ISIS internal data representation.
* isisdiff - Shows the  difference between the meta information
             given by two image files A and B.
* isisconv - The ISIS data converter. It converts image data between all
             different formats provided by the imageIO plugins.
* isisflip - Flips the image orientation and voxel data along a given axis.
* isisraw  - Reads or writes raw data files from/to isis images.

%package        applications
Summary:        Applications for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    applications
Applications for %{name}. This package includes:

* isiscalc - Does math on image voxels.

%package        adapter-qt4
Summary:        Qt 4 adapter for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Enhances:       %{name}

%description    adapter-qt4
Qt 4 adapter for %{name}.

%package        adapter-qt4-devel
Summary:        Development files for Qt 4 adapter for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       qt4-devel%{?_isa}
Enhances:       %{name}-devel

%description    adapter-qt4-devel
Development files for Qt 4 adapter for %{name}.

%package        adapter-itk-devel
Summary:        Development files for ITK adapter for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       InsightToolkit-devel%{?_isa}
Enhances:       %{name}-devel

%description    adapter-itk-devel
Development files for ITK adapter for %{name}.

%prep
%autosetup -n %{name}-%{commit} -S git
# otherwise git commit will appear somewhere
rm -rf .git

rm -rf build/
mkdir -p build/

%build
pushd build/
  %cmake ../ \
    -DISIS_BUILD_TESTS=ON                              \
    -DISIS_BUILD_TOOLS=ON                              \
    -DISIS_BUILD_FILTER=ON -DISIS_FILTER_ENABLE_OMP=ON \
    -DISIS_ITK=ON                                      \
    -DISIS_QT4=ON                                      \
    -DISIS_IOPLUGIN_NULL=ON                            \
    -DISIS_IOPLUGIN_PNG=ON                             \
    -DISIS_IOPLUGIN_COMP_LZMA=ON                       \
    -DISIS_APPS_CALC=ON                                \
    -DISIS_DEBUG_LOG=OFF
  %make_build
popd

%install
pushd build/
  %make_install
popd

%check
# not all tests pass (see https://github.com/isis-group/isis/issues/71)
pushd build/
  ctest -VV || :
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING.txt
%{_libdir}/%{name}/
%{_libdir}/lib%{name}_core.so.*

%files devel
%dir %{_includedir}/%{name}/
%dir %{_includedir}/%{name}/Adapter/
%{_includedir}/%{name}/CoreUtils/
%{_includedir}/%{name}/DataStorage/
%{_includedir}/%{name}/Filter/
%{_includedir}/%{name}/config.hpp
%{_libdir}/cmake/ISIS/
%{_libdir}/lib%{name}_core.so

%files tools
%{_bindir}/%{name}dump
%{_bindir}/%{name}diff
%{_bindir}/%{name}conv
%{_bindir}/%{name}flip
%{_bindir}/%{name}raw

%files applications
%{_bindir}/%{name}calc

%files adapter-qt4
%{_libdir}/lib%{name}Adapter_qt4.so.*

%files adapter-qt4-devel
%{_includedir}/%{name}/Adapter/q*.hpp
%{_libdir}/lib%{name}Adapter_qt4.so

%files adapter-itk-devel
%{_includedir}/%{name}/Adapter/itk*.hpp

%changelog
* Sun Nov 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.9-1
- Initial package
