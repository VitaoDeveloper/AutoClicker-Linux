#!/usr/bin/env bash
set -e

INSTALL_DIR="${1:-$HOME/.local/opt/autoclicker}"

mkdir -p "$INSTALL_DIR"
cp autoclicker icon.png "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/autoclicker"

mkdir -p "$HOME/.local/share/applications"
sed "s|/opt/autoclicker|$INSTALL_DIR|g" autoclicker.desktop > "$HOME/.local/share/applications/autoclicker.desktop"
chmod +x "$HOME/.local/share/applications/autoclicker.desktop"

update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
echo "Instalado em $INSTALL_DIR"
