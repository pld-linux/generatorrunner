#
# Conditional build:
%bcond_with	apidocs		# API documentation

Summary:	Generator Runner - calling binding generator front-ends
Summary(pl.UTF-8):	Generator Runner - wywoływanie frontendów generatorów wiązań
Name:		generatorrunner
Version:	0.6.16
Release:	2
License:	GPL v2
Group:		Development/Tools
Source0:	https://github.com/PySide/Generatorrunner/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	34e60a01f574e5976279510fa9c9069a
URL:		https://github.com/PySide/Generatorrunner
BuildRequires:	QtCore-devel >= 4.5.0
BuildRequires:	apiextractor-devel >= 0.10.10
BuildRequires:	cmake >= 2.6
%{?with_apidocs:BuildRequires:	sphinx-pdg}
Requires:	apiextractor >= 0.10.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Generator Runner loads and calls binding generator front-ends.

%description -l pl.UTF-8
Generator Runner wczytuje i wywołuje frontendy generatorów wiązań.

%package devel
Summary:	Header files for Generator Runner library and plugins
Summary(pl.UTF-8):	Pliki nagłówkowe dla biblioteki oraz wtyczek Generator Runnera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Generator Runner library and plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla biblioteki oraz wtyczek Generator Runnera.

%package apidocs
Summary:	Generator Runner API documentation
Summary(pl.UTF-8):	Dokumentacja API Generator Runnera
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Generator Runner API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Generator Runnera.

%prep
%setup -q -n Generatorrunner-%{version}

%build
install -d build
cd build
%cmake ..
%{__make}
%{?with_apidocs:%{__make} doc}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/docgenerator
%attr(755,root,root) %{_bindir}/generatorrunner
%attr(755,root,root) %{_libdir}/libgenrunner.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgenrunner.so.0.6
%dir %{_libdir}/generatorrunner
%attr(755,root,root) %{_libdir}/generatorrunner/qtdoc_generator.so
%{_mandir}/man1/docgenerator.1*
%{_mandir}/man1/generatorrunner.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgenrunner.so
%{_includedir}/generatorrunner
%{_pkgconfigdir}/generatorrunner.pc
%{_libdir}/cmake/GeneratorRunner-%{version}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/{_images,_sources,_static,*.{html,js}}
%endif
