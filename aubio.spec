#
# Conditional build:
%bcond_without	python2  # python bindings
%bcond_without	python3  # python bindings
#
Summary:	aubio - library for audio labelling
Summary(pl.UTF-8):	aubio - biblioteka do oznaczania dźwięku
Name:		aubio
Version:	0.4.3
Release:	2
License:	GPL v3+
Group:		Libraries
Source0:	http://aubio.piem.org/pub/%{name}-%{version}.tar.bz2
# Source0-md5:	52a960cfc8a3e3125f3a258545d1c7e5
URL:		http://aubio.piem.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	doxygen
BuildRequires:	ffmpeg-devel
BuildRequires:	fftw3-single-devel >= 3.0.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.15.0
BuildRequires:	libsamplerate-devel >= 0.0.15
BuildRequires:	libsndfile-devel >= 1.0.4
BuildRequires:	pkgconfig
BuildRequires:	txt2man
%if %{with python2} || %{with python3}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-setuptools
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
  symbolicznych danych muzycznych ze źródła dźwięku i stworzenia danych
  typu MIDI.
- aubiocut - skrypt Pythona pobierający dźwięk wejściowy i tworzący
  nową próbkę dla każdego wykrytego początku lub taktu. Fragmenty
  tworzone przez aubiocut są przydatne do wykorzystania przez sekwencer,
  jak np. Hydrogen.
- aubiopitch - skrypt Pythona do wyciągania ścieżek wysokości z plików
  dźwiękowych.

%package -n python-aubio
Summary:	aubio Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki aubio
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-aubio
aubio Python bindings.

%description -n python-aubio -l pl.UTF-8
Wiązania Pythona do biblioteki aubio.

%package -n python3-aubio
Summary:	aubio Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki aubio
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-aubio
aubio Python bindings.

%description -n python3-aubio -l pl.UTF-8
Wiązania Pythona do biblioteki aubio.

%prep
%setup -q

%build
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
./waf configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--enable-fftw3f \
	--enable-jack \
	--enable-sndfile \
	--enable-avcodec \
	--enable-samplerate \
	--disable-atlas \
	--enable-docs

./waf build -v

%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

./waf install -v \
	--destdir=$RPM_BUILD_ROOT \
	--libdir=%{_libdir} \
	--prefix=%{_prefix} \
	--libexecdir=%{_libexecdir}

%if %{with python2}
%py_install
%endif

%if %{with python3}
%py3_install
%endif

rm -r $RPM_BUILD_ROOT%{_docdir}/libaubio-doc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) %{_libdir}/libaubio.so.5.*.*
%attr(755,root,root) %ghost %{_libdir}/libaubio.so.5

%files devel
%defattr(644,root,root,755)
%doc doc/web/html/*
%attr(755,root,root) %{_libdir}/libaubio.so
%{_includedir}/%{name}
%{_pkgconfigdir}/aubio.pc

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aubiomfcc
%attr(755,root,root) %{_bindir}/aubionotes
%attr(755,root,root) %{_bindir}/aubioonset
%attr(755,root,root) %{_bindir}/aubiopitch
%attr(755,root,root) %{_bindir}/aubioquiet
%attr(755,root,root) %{_bindir}/aubiotrack
%{_mandir}/man1/aubiomfcc.1*
%{_mandir}/man1/aubionotes.1*
%{_mandir}/man1/aubioonset.1*
%{_mandir}/man1/aubiopitch.1*
%{_mandir}/man1/aubioquiet.1*
%{_mandir}/man1/aubiotrack.1*

%if %{with python2}
%files -n python-aubio
%defattr(644,root,root,755)
%dir %{py_sitedir}/aubio
%{py_sitedir}/aubio/*.py*
%attr(755,root,root) %{py_sitedir}/aubio/_aubio.so
%{py_sitedir}/aubio*.egg-info
%if %{without python3}
%attr(755,root,root) %{_bindir}/aubiocut
%{_mandir}/man1/aubiocut.1*
%endif
%endif

%if %{with python3}
%files -n python3-aubio
%defattr(644,root,root,755)
%dir %{py3_sitedir}/aubio
%{py3_sitedir}/aubio/__pycache__
%{py3_sitedir}/aubio/*.py
%attr(755,root,root) %{py3_sitedir}/aubio/_aubio.*.so
%{py3_sitedir}/aubio*.egg-info
%attr(755,root,root) %{_bindir}/aubiocut
%{_mandir}/man1/aubiocut.1*
%endif
