%global debug_package %{nil}

Name: dooble
Version: 2025.06.10
Release: 1
Source0: https://github.com/textbrowser/dooble/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Summary: Simple lightweight web browser
URL: https://textbrowser.github.io/dooble
License: MIT
Group: Networking/WWW
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6WebEngineCore)
BuildRequires: cmake(Qt6WebEngineWidgets)
BuildRequires: cmake(Qt6Charts)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6WebChannel)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Positioning)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Sql)
BuildRequires: cmake(Qt6Xml)
BuildRequires: cmake(Qt6PrintSupport)
BuildRequires: qmake-qt6
BuildRequires: qt6-cmake
BuildRequires: make
# Just for scaling/converting icons
BuildRequires: imagemagick
# For storing settings
Requires:	qt6-qtbase-sql-sqlite

%description
Simple lightweight web browser

%prep
%autosetup -p1
export QTDIR=%{_qtdir}
sed -i -e 's,-Werror,,g' dooble.pro
%{_qtdir}/bin/qmake dooble.pro

%build
%make_build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 Dooble %{buildroot}%{_bindir}/
cat >%{buildroot}%{_bindir}/dooble <<EOF
#!/bin/sh
export QT_PLUGIN_PATH=%{_qtdir}/plugins
exec %{_bindir}/Dooble "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/dooble
#mkdir -p %{buildroot}%{_qtdir}/translations/qtwebengine_locales
#mv qtwebengine_dictionaries/* %{buildroot}%{_qtdir}/translations/qtwebengine_locales
mkdir -p %{buildroot}%{_datadir}/applications
mv Distributions/dooble.desktop %{buildroot}%{_datadir}/applications/
for scale in 16 20 22 24 32 36 40 44 48 64 72 80 96 128 150 160 192 256 512 ; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${scale}x${scale}/apps
	convert Icons/dooble.ico -scale ${scale}x${scale} %{buildroot}%{_datadir}/icons/hicolor/${scale}x${scale}/apps/dooble.png
done

%files
%{_bindir}/dooble
%{_bindir}/Dooble
#%{_qtdir}/translations/qtwebengine_locales
%{_datadir}/applications/dooble.desktop
%{_datadir}/icons/*/*/*/*
