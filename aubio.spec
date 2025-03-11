#
# Conditional build:
%bcond_without	python2	# CPython 2.x bindings
%bcond_without	python3	# CPython 3.x bindings
%bcond_with	tests	# (python) tests (some inexact failures, missing test data)
%bcond_without	apidocs	# API (Sphinx and doxygen) documentation
#
%if %{without python3}
%undefine	with_apidocs
%endif
Summary:	aubio - library for audio labelling
Summary(pl.UTF-8):	aubio - biblioteka do oznaczania dźwięku
Name:		aubio
Version:	0.4.9
Release:	6
License:	GPL v3+
Group:		Libraries
Source0:	https://aubio.org/pub/%{name}-%{version}.tar.bz2
# Source0-md5:	50c9c63b15a2692378af5d602892f16a
Patch0:		ffmpeg6.patch
URL:		https://aubio.org/
# libavcodec >= 54.35.0, libavformat >= 52.3.0, libavutil >= 52.3.0, libswresample >= 1.2.0 || libavresample >= 1.0.1
BuildRequires:	ffmpeg-devel >= 1.1
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
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	sed >= 4.0
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	sphinx-pdg-3
%endif
Requires:	ffmpeg-libs >= 1.1
Requires:	libsamplerate >= 0.0.15
Requires:	libsndfile >= 1.0.4
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

%package apidocs
Summary:	API documentation for aubio library
Summary(pl.UTF-8):	Dokumentacja API biblioteki aubio
Group:		Documentation

%description apidocs
API documentation for aubio library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki aubio.

%package progs
Summary:	Example applications using aubio library
Summary(pl.UTF-8):	Przykładowe programy korzystajace z biblioteki aubio
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}
Requires:	jack-audio-connection-kit-libs >= 0.15.0

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
Summary:	aubio Python 2 bindings
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki aubio
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-aubio
aubio Python 2 bindings.

%description -n python-aubio -l pl.UTF-8
Wiązania Pythona 2 do biblioteki aubio.

%package -n python3-aubio
Summary:	aubio Python 3 bindings
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki aubio
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-aubio
aubio Python 3 bindings.

%description -n python3-aubio -l pl.UTF-8
Wiązania Pythona 3 do biblioteki aubio.

%prep
%setup -q
%patch -P 0 -p1

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
	--disable-atlas \
	--enable-avcodec \
	%{?with_apidocs:--enable-docs} \
	--enable-fftw3f \
	--enable-jack \
	--enable-samplerate \
	--enable-sndfile

./waf build -v

%if %{with python2}
%py_build

%if %{with tests}
LD_LIBRARY_PATH=$(pwd)/build/src \
PYTHONPATH=$(readlink -f build-2/lib.*) \
%{__python} -m unittest discover -s python/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
LD_LIBRARY_PATH=$(pwd)/build/src \
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} -m unittest discover -s python/tests
%endif
%endif

%if %{with apidocs}
LD_LIBRARY_PATH=$(pwd)/build/src \
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
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

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libaubio-doc

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
%attr(755,root,root) %{_libdir}/libaubio.so
%{_includedir}/aubio
%{_pkgconfigdir}/aubio.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libaubio.a

%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_downloads,_static,*.html,*.js} build/api

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aubio
%attr(755,root,root) %{_bindir}/aubiomfcc
%attr(755,root,root) %{_bindir}/aubionotes
%attr(755,root,root) %{_bindir}/aubioonset
%attr(755,root,root) %{_bindir}/aubiopitch
%attr(755,root,root) %{_bindir}/aubioquiet
%attr(755,root,root) %{_bindir}/aubiotrack
%{_mandir}/man1/aubio.1*
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
%{py_sitedir}/aubio-%{version}-py*.egg-info
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
%{py3_sitedir}/aubio-%{version}-py*.egg-info
%attr(755,root,root) %{_bindir}/aubiocut
%{_mandir}/man1/aubiocut.1*
%endif
