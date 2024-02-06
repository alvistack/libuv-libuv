# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: libuv
Epoch: 100
Version: 1.46.0
Release: 1%{?dist}
Summary: Asynchronous event notification library
License: MIT
URL: https://github.com/libuv/libuv/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?rhel} == 7
BuildRequires: devtoolset-11
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
BuildRequires: devtoolset-11-libatomic-devel
%endif
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: glibc-static
BuildRequires: libtool
BuildRequires: make

%description
libuv is a new platform layer for Node. Its purpose is to abstract IOCP on
Windows and libev on Unix systems. We intend to eventually contain all platform
differences in this library.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-11/enable
%endif
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.la' -exec rm -rf {} \;

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libuv1
Summary: Asynchronous event notification library

%description -n libuv1
libuv is a new platform layer for Node. Its purpose is to abstract IOCP on
Windows and libev on Unix systems. We intend to eventually contain all platform
differences in this library.

%package -n libuv-devel
Summary: Development libraries for libuv
Requires: libuv1 = %{epoch}:%{version}-%{release}

%description -n libuv-devel
Development libraries for libuv

%post -n libuv1 -p /sbin/ldconfig
%postun -n libuv1 -p /sbin/ldconfig

%files -n libuv1
%license LICENSE
%{_libdir}/*.so.*

%files -n libuv-devel
%{_includedir}/uv.h
%{_includedir}/uv/
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/libuv.pc
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n libuv-devel
Summary: Development libraries for libuv
Requires: libuv = %{epoch}:%{version}-%{release}

%description -n libuv-devel
Development libraries for libuv

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/*.so.*

%files -n libuv-devel
%{_includedir}/uv.h
%{_includedir}/uv/
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/libuv.pc
%endif

%changelog
