#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?Uso: $0 <versão>}"

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$REPO_DIR/dist/standalone"
STAGE_DIR="$BUILD_DIR/autoclicker"

rm -rf "$BUILD_DIR"
mkdir -p "$STAGE_DIR"

cd "$REPO_DIR"
.venv/bin/python -m PyInstaller \
    --onefile \
    --name autoclicker \
    --distpath "$STAGE_DIR" \
    --workpath "$BUILD_DIR/build" \
    --specpath "$BUILD_DIR" \
    app/main.py

cp "$REPO_DIR/packaging/standalone/autoclicker.desktop" "$STAGE_DIR/"
cp "$REPO_DIR/packaging/standalone/install.sh" "$STAGE_DIR/"
cp "$REPO_DIR/packaging/standalone/README.txt" "$STAGE_DIR/"
chmod +x "$STAGE_DIR/install.sh"

if [ -f "$REPO_DIR/packaging/icons/autoclicker.png" ]; then
    cp "$REPO_DIR/packaging/icons/autoclicker.png" "$STAGE_DIR/icon.png"
fi

cd "$BUILD_DIR"
tar -czf "$REPO_DIR/dist/autoclicker-linux-${VERSION}-standalone.tar.gz" \
    autoclicker

echo "Arquivo standalone gerado:"
ls -lh "$REPO_DIR/dist/autoclicker-linux-${VERSION}-standalone.tar.gz"
