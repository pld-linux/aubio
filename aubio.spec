# TODO:
#	- unpackaged /usr/share/sounds/aubio/woodblock.aiff
#	- package python stuff
#	- create lash.spec (http://www.nongnu.org/lash) and
#	  --enable-lash
#
Summary:	aubio is a library for audio labelling
Name:		aubio
Version:	0.3.2
Release:	0.1
License:	GPL v2+
Group:		Libraries
Source0:	http://aubio.piem.org/pub/%{name}-%{version}.tar.gz
# Source0-md5:	ffc3e5e4880fec67064f043252263a44
URL:		http://aubio.piem.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	fftw3-single-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
aubio is a library for audio labelling

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

%package progs
Summary:	Example applications using aubio library
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description progs
A few examples of applications using aubio library:
- aubioonset: outputs the onset detected
- aubionotes: uses both onset and pitch to extract symbolic music data
    from an audio source and emit MIDI like data.
- aubiocut: a python script that takes an input sound and creates one
    new sample at each detected onset or beat. The slices produced by
    aubiocut are useful for use with a sequencer such as Hydrogen.
- aubiopitch: a python script to extract pitch tracks from sound files

%prep
%setup -q

%build
%configure \
	--enable-alsa \
	--enable-jack

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/%{py_sitedir}
rm -rf $RPM_BUILD_ROOT/%{py_libdir}
rm -rf $RPM_BUILD_ROOT/%{py_scriptdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
