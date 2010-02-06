# TODO:
#	- package doc and create audacity-plugin
#
# Conditional build:
%bcond_without	python  # python bindings
#
Summary:	aubio - library for audio labelling
Summary(pl.UTF-8):	aubio - biblioteka do oznaczania dźwięku
Name:		aubio
Version:	0.3.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://aubio.piem.org/pub/%{name}-%{version}.tar.gz
# Source0-md5:	ffc3e5e4880fec67064f043252263a44
Patch0:		%{name}-python.patch
URL:		http://aubio.piem.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	docbook-to-man
BuildRequires:	fftw3-single-devel >= 3.0.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.15.0
BuildRequires:	lash-devel >= 0.5.0
BuildRequires:	libsamplerate-devel >= 0.0.15
BuildRequires:	libsndfile-devel >= 1.0.4
BuildRequires:	libtool
BuildRequires:	pkgconfig
#BuildRequires:	puredata-devel (m_pd.h)
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig-python
%endif
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
aubio is a library for audio labelling.

%description -l pl.UTF-8
aubio to biblioteka do oznaczania dźwięku.

%package devel
Summary:	Header files for aubio library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki aubio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	fftw3-single-devel >= 3.0.0
Requires:	libsamplerate-devel >= 0.0.15
# for libaubioext:
# alsa-lib-devel >= 0.9.0
# jack-audio-connection-kit-devel >= 0.15.0
# libsndfile-devel >= 1.0.4

%description devel
Header files for aubio library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki aubio.

%package static
Summary:	Static aubio library
Summary(pl.UTF-8):	Statyczna biblioteka aubio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static aubio library.

%description static -l pl.UTF-8
Statyczna biblioteka aubio.

%package progs
Summary:	Example applications using aubio library
Summary(pl.UTF-8):	Przykładowe programy korzystajace z biblioteki aubio
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description progs
A few examples of applications using aubio library:
- aubioonset: outputs the onset detected.
- aubionotes: uses both onset and pitch to extract symbolic music data
    from an audio source and emit MIDI like data.
- aubiocut: a Python script that takes an input sound and creates one
    new sample at each detected onset or beat. The slices produced by
    aubiocut are useful for use with a sequencer such as Hydrogen.
- aubiopitch: a Python script to extract pitch tracks from sound
  files.

%description progs -l pl.UTF-8
Kilka przykładowych aplikacji korzystających z biblioteki dubio:
- aubioonset - wypisuje wykryty początek.
- aubionotes - wykorzystuje początek i wysokość do wyciągnięcia
  symbolicznych danych muzycznych ze źródła dźwięku i stworzenia
  danych typu MIDI.
- aubiocut - skrypt Pythona pobierający dźwięk wejściowy i tworzący
  nową próbkę dla każdego wykrytego początku lub taktu. Fragmenty
  tworzone przez aubiocut są przydatne do wykorzystania przez
  sekwencer, jak np. Hydrogen.
- aubiopitch - skrypt Pythona do wyciągania ścieżek wysokości z
  plików dźwiękowych.

%package -n python-aubio
Summary:	aubio Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki aubio
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-aubio
aubio Python bindings.

%description -n python-aubio -l pl.UTF-8
Wiązania Pythona do biblioteki aubio.

%prep
%setup -q
%patch0 -p1
sed 's/\([A-Z_]\+\)+="\(.*\)"/\1="$\1 \2"/' -i configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-alsa \
	--enable-lash \
	--enable-jack

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean
rm -f $RPM_BUILD_ROOT%{py_sitedir}/aubio/_aubiowrapper.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libaubio.so.*.*.*
%attr(755,root,root) %{_libdir}/libaubioext.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaubio.so.2
%attr(755,root,root) %ghost %{_libdir}/libaubioext.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaubio.so
%attr(755,root,root) %{_libdir}/libaubioext.so
%{_libdir}/libaubio.la
%{_libdir}/libaubioext.la
%{_includedir}/%{name}
%{_pkgconfigdir}/aubio.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libaubio.a
%{_libdir}/libaubioext.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aubionotes
%attr(755,root,root) %{_bindir}/aubioonset
%attr(755,root,root) %{_bindir}/aubiotrack
%{_mandir}/man1/aubionotes.1*
%{_mandir}/man1/aubioonset.1*
%{_mandir}/man1/aubiotrack.1*
%{_datadir}/sounds/aubio

%if %{with python}
%files -n python-aubio
%defattr(644,root,root,755)
%dir %{py_sitedir}/aubio
%attr(755,root,root) %{py_sitedir}/aubio/_aubiowrapper.so
%{py_sitescriptdir}/aubio
# examples
%attr(755,root,root) %{_bindir}/aubiocut
%attr(755,root,root) %{_bindir}/aubiopitch
%{_mandir}/man1/aubiocut.1*
%{_mandir}/man1/aubiopitch.1*
%endif
