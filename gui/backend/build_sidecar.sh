#!/usr/bin/env bash
# Builds the FastAPI backend into a single-file executable that Tauri bundles
# as a sidecar, and names it per Tauri's required "-<target-triple>" convention.
set -euo pipefail

cd "$(dirname "$0")/../.."  # repo root

TARGET_TRIPLE="$(rustc --print host-tuple)"
OUT_DIR="gui/frontend/src-tauri/binaries"
BUILD_DIR="$(pwd)/.pyinstaller-build"
BIN_NAME="winder-backend"

mkdir -p "$OUT_DIR" "$BUILD_DIR"

pyinstaller \
  --name "$BIN_NAME" \
  --onefile \
  --add-data "../settings-example.yml:." \
  --distpath "$OUT_DIR" \
  --workpath "$BUILD_DIR" \
  --specpath "$BUILD_DIR" \
  gui/backend/app.py

EXT=""
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  EXT=".exe"
fi

SIDECAR_PATH="$OUT_DIR/$BIN_NAME-$TARGET_TRIPLE$EXT"
mv "$OUT_DIR/$BIN_NAME$EXT" "$SIDECAR_PATH"
"$SIDECAR_PATH" --check-bundle
echo "Built $SIDECAR_PATH"
