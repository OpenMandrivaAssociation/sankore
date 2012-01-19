%define	int_ver v1.26.b.00-83-g
%define	pname Sankore-Sankore
%define	gitversion 0d12a17


%define	destdir %{_datadir}/%{name}

Name:		sankore
Version:	3.1
Release:	1
Summary:	The open-source software suite for digital teachers
License:	GPLv3+ or LGPLv3+
Group:		Education
URL:		https://github.com/Sankore/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		sankore_3.1.pro.patch

BuildRequires:	qt4-devel
BuildRequires:	zlib-devel
BuildRequires:	xpdf-devel
BuildRequires:	quazip-devel
BuildRequires:	phonon-devel
BuildRequires:	qtsingleapplication-devel
BuildRequires:	libgomp-devel
BuildRequires:	freetype2-devel
BuildRequires:	desktop-file-utils

%description
The Sankore project (formerly known as Uniboard) has for 
goal to propose a free and open source Interactive Whiteboard 
Software, an editor of interactive content and a tutorial
for the creation of teaching content

%prep

%setup -q
%patch0 -p1 -b .fix_deps

%build
%{qmake_qt4} PREFIX=%{destdir} DESTDIR=%{destdir}
%make

%install
%make INSTALL="install -p" release-install

mkdir -p %{buildroot}%{_datadir}/icons/
install -D -m 0644 resources/images/uniboard.png %{buildroot}%{_datadir}/icons/%{name}.png

cat > %{name}.desktop <<EOF
[Desktop Entry]
Name=Sankore
Comment=The open-source software suite for digital teachers
Exec=%{destdir}/sankore
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Education
EOF

desktop-file-install --mode=0644 --dir=%{buildroot}%{_datadir}/applications %{name}.desktop
mkdir -p %{buildroot}/%_bindir/
cat > %{buildroot}/%_bindir/%{name} <<EOF
#!/bin/sh
%{destdir}/sankore
EOF
chmod 755 %{buildroot}/%_bindir/%{name}
mkdir -p %{buildroot}/%{destdir}
cp -R resources/linux/qtlinux/* %{buildroot}/%{destdir}
cp -rv build/linux/release/product/* %{buildroot}/%{destdir}
mv %{buildroot}/%{destdir}/Sankore\ %{version} %{buildroot}/%{destdir}/sankore

%files
%defattr(-,root,root,-)
%doc *gpl.txt README.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.png
%{destdir}
