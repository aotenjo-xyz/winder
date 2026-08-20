#!/usr/bin/env bash
# Builds the FastAPI backend into a single-file executable that Tauri bundles
# as a sidecar, and names it per Tauri's required "-<target-triple>" convention.
set -euo pipefail

cd "$(dirname "$0")/../.."  # repo root

TARGET_TRIPLE="$(rustc --print host-tuple)"
OUT_DIR="gui/frontend/src-tauri/binaries"
BIN_NAME="winder-backend"

mkdir -p "$OUT_DIR"

ADD_DATA_SEP=":"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  ADD_DATA_SEP=";"
fi

pyinstaller \
  --name "$BIN_NAME" \
  --onefile \
  --add-data "$(pwd)/settings-example.yml${ADD_DATA_SEP}." \
  --distpath "$OUT_DIR" \
  --workpath /tmp/winder-backend-build \
  --specpath /tmp/winder-backend-build \
  gui/backend/app.py

EXT=""
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  EXT=".exe"
fi

mv "$OUT_DIR/$BIN_NAME$EXT" "$OUT_DIR/$BIN_NAME-$TARGET_TRIPLE$EXT"
echo "Built $OUT_DIR/$BIN_NAME-$TARGET_TRIPLE$EXT"
