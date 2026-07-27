#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?Uso: $0 <versão>}"

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$REPO_DIR/dist"
APP_DIR="$BUILD_DIR/autoclicker"

rm -rf "$BUILD_DIR"
mkdir -p "$APP_DIR/usr/bin" \
         "$APP_DIR/usr/share/applications" \
         "$APP_DIR/usr/share/icons/hicolor/256x256/apps"

cp "$REPO_DIR/packaging/autoclicker.desktop" \
   "$APP_DIR/usr/share/applications/autoclicker.desktop"

if [ -f "$REPO_DIR/packaging/icons/autoclicker.png" ]; then
    cp "$REPO_DIR/packaging/icons/autoclicker.png" \
       "$APP_DIR/usr/share/icons/hicolor/256x256/apps/autoclicker.png"
fi

cd "$REPO_DIR"
.venv/bin/python -m PyInstaller \
    --onefile \
    --name autoclicker \
    --distpath "$APP_DIR/usr/bin" \
    --workpath "$BUILD_DIR/build" \
    --specpath "$BUILD_DIR" \
    app/main.py

chmod 755 "$APP_DIR/usr/bin/autoclicker"

# --- .deb via dpkg-deb ---
DEB_ROOT="$BUILD_DIR/deb/autoclicker_${VERSION}_amd64"
mkdir -p "$DEB_ROOT/DEBIAN"
cp -a "$APP_DIR"/* "$DEB_ROOT/"

cat > "$DEB_ROOT/DEBIAN/control" << EOF
Package: autoclicker
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: amd64
Depends: ydotool
Maintainer: VitaoDeveloper
Description: Automação de cliques de mouse para Linux
 AutoClicker para Linux com suporte a X11 e Wayland.
 Interface gráfica em GTK4 com atalho global de teclado.
EOF

cp "$REPO_DIR/packaging/postinst.sh" "$DEB_ROOT/DEBIAN/postinst"
chmod 755 "$DEB_ROOT/DEBIAN/postinst"

dpkg-deb --build --root-owner-group "$DEB_ROOT" \
    "$BUILD_DIR/autoclicker_${VERSION}_amd64.deb"

# --- .rpm via rpmbuild ---
RPMBUILD="$BUILD_DIR/rpmbuild"
mkdir -p "$RPMBUILD"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

RPM_SRC="/tmp/autoclicker-rpm-src/autoclicker-${VERSION}"
mkdir -p "$RPM_SRC"
cp -a "$APP_DIR/usr" "$RPM_SRC/"
tar -czf "$RPMBUILD/SOURCES/autoclicker-${VERSION}.tar.gz" \
    -C /tmp/autoclicker-rpm-src "autoclicker-${VERSION}"
rm -rf /tmp/autoclicker-rpm-src

cat > "$RPMBUILD/SPECS/autoclicker.spec" << EOF
%define _enable_debug_packages 0
%define debug_package %{nil}

Name:           autoclicker
Version:        ${VERSION}
Release:        1%{?dist}
Summary:        Automação de cliques de mouse para Linux
License:        MIT
URL:            https://github.com/JotinhaGamer22/AutoClicker-Linux
Source0:        autoclicker-%{version}.tar.gz
Requires:       ydotool

%description
AutoClicker para Linux com suporte a X11 e Wayland.

%prep
%setup -q

%install
cp -a usr %{buildroot}

%post
update-desktop-database -q /usr/share/applications || true
gtk-update-icon-cache /usr/share/icons/hicolor || true

%files
/usr/bin/autoclicker
/usr/share/applications/autoclicker.desktop
EOF

rpmbuild -bb "$RPMBUILD/SPECS/autoclicker.spec" \
    --define "_topdir $RPMBUILD" \
    --define "_sourcedir $RPMBUILD/SOURCES" 2>/dev/null

cp "$RPMBUILD"/RPMS/*/*.rpm "$BUILD_DIR/" 2>/dev/null || true

echo "Pacotes gerados em $BUILD_DIR:"
ls -lh "$BUILD_DIR"/*.deb "$BUILD_DIR"/*.rpm 2>/dev/null
