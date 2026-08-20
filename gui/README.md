# Winder GUI

A desktop GUI for the winding machine, built as:

- `backend/` — a FastAPI service that wraps `src/winding.py` (the same code the
  CLI in `scripts/main.py` uses) and exposes the "wind wires" flow over HTTP.
- `frontend/` — a [Tauri](https://tauri.app) + React app. Tauri launches the
  Python backend as a bundled "sidecar" executable (built with PyInstaller),
  so end users just install one app — no Python, conda, or CLI required.

This first version covers the most-used flow only: winding wire 0/1/2,
continuous winding, live motor position display, and emergency stop. The
settings editor and motor-position debug menu can be added the same way
later (add an endpoint in `backend/app.py`, add a screen in `frontend/src`).

## Where does settings.yml live?

Unlike the CLI (which reads `settings.yml` from the repo root you happen to
run it from), the GUI backend can be launched from anywhere — a bundled
sidecar has no repo checkout next to it, and `tauri dev` may run it from an
unpredictable working directory. So the backend always resolves a fixed,
per-user config location instead of trusting the current working directory:

- Linux: `~/.config/winder/settings.yml`
- macOS: `~/Library/Application Support/winder/settings.yml`
- Windows: `%APPDATA%\winder\settings.yml`

If that file doesn't exist yet, it's auto-created from `settings-example.yml`
on first connect. Edit the serial port, motor PID values, etc. in that file
before using "Connect (hardware)". The resolved path is also shown in the
GUI's connect screen, and via `GET /api/config-path`.

## Architecture

```
Tauri window (WebView, React UI)
   │  HTTP (http://127.0.0.1:8760)
   ▼
FastAPI backend (bundled as sidecar binary, or run manually in dev)
   │
   ▼
src/winding.py  ──serial──▶  Aotenjo Master board
```

## Prerequisites (install once, on your dev machine)

- Node.js 20+ and npm
- Rust toolchain (`rustup`) — required by Tauri
- Python 3.12 with the project's existing env (conda/uv) plus `fastapi`,
  `uvicorn`, and `pyinstaller` (see `backend/requirements.txt`)
- Tauri's OS-level dependencies for your platform:
  https://v2.tauri.app/start/prerequisites/

## First-time frontend setup

A placeholder `src-tauri/icons/icon.png` is included so the app builds out of
the box. Replace it with your real logo before shipping, e.g.:

```bash
cd gui/frontend
npm install
npm run tauri icon path/to/a-1024x1024-source-icon.png
```

## Development (run backend + frontend without building installers)

1. Start the backend (from the repo root, with the project's Python env active):
   ```bash
   pip install -r gui/backend/requirements.txt
   uvicorn gui.backend.app:app --reload --port 8760
   ```
2. In another terminal, start the Tauri dev app:
   ```bash
   cd gui/frontend
   npm install
   npm run tauri dev
   ```
   This opens a native window loading the React UI, which talks to the
   backend at `http://127.0.0.1:8760`.

## Building a distributable installer

1. Bundle the Python backend into a single executable with PyInstaller:
   ```bash
   cd gui/backend
   ./build_sidecar.sh
   ```
   This produces `gui/frontend/src-tauri/binaries/winder-backend-<target-triple>`
   (the suffix must match `rustc --print host-tuple`).
2. Build the installer:
   ```bash
   cd gui/frontend
   npm run tauri build
   ```
   Output installers (`.msi`/`.dmg`/`.AppImage`/`.deb`) are placed under
   `gui/frontend/src-tauri/target/release/bundle/`.

Repeat step 1 on each OS you want to ship for (PyInstaller only cross-compiles
to the OS it runs on), or use CI (GitHub Actions matrix) to build all three.
