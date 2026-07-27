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
python3 -m PyInstaller \
    --onefile \
    --name autoclicker \
    --distpath "$APP_DIR/usr/bin" \
    --workpath "$BUILD_DIR/build" \
    --specpath "$BUILD_DIR" \
    app/main.py

cd "$BUILD_DIR"

fpm -s dir -t deb \
    --name autoclicker \
    --version "$VERSION" \
    --description "Automação de cliques de mouse para Linux" \
    --maintainer "VitaoDeveloper" \
    --license MIT \
    --category Utility \
    --after-install "$REPO_DIR/packaging/postinst.sh" \
    --deb-auto-config-files \
    -C "$APP_DIR" \
    -p "$BUILD_DIR/autoclicker_${VERSION}_all.deb" \
    usr/

fpm -s dir -t rpm \
    --name autoclicker \
    --version "$VERSION" \
    --description "Automação de cliques de mouse para Linux" \
    --maintainer "VitaoDeveloper" \
    --license MIT \
    --category Utility \
    --after-install "$REPO_DIR/packaging/postinst.sh" \
    -C "$APP_DIR" \
    -p "$BUILD_DIR/autoclicker-${VERSION}-1.noarch.rpm" \
    usr/

echo "Pacotes gerados em $BUILD_DIR:"
ls -lh "$BUILD_DIR"/*.deb "$BUILD_DIR"/*.rpm 2>/dev/null
