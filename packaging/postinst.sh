#!/bin/sh
update-desktop-database -q /usr/share/applications || true
gtk-update-icon-cache /usr/share/icons/hicolor || true
