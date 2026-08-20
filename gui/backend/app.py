"""
FastAPI backend for the Winder desktop GUI.

Wraps the existing `src.winding.Wind` control class (the same class used by
the terminal menu in scripts/main.py) so a Tauri/React frontend can drive the
winding machine over HTTP instead of a terminal.

Run in dev:
    uvicorn gui.backend.app:app --reload --port 8760

Run standalone (used by PyInstaller / the Tauri sidecar):
    python -m gui.backend.app
"""

import os
import shutil
import sys
import threading
import traceback
from enum import Enum
from typing import Optional

# Allow `from src.winding import Wind` to resolve when this file is executed
# directly (e.g. from the PyInstaller-built sidecar) instead of as a package.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


def _bundled_example_config_path() -> str:
    # PyInstaller extracts --add-data files under sys._MEIPASS at runtime.
    base_dir = getattr(sys, "_MEIPASS", _REPO_ROOT)
    return os.path.join(base_dir, "settings-example.yml")


def _user_config_dir() -> str:
    # A sidecar's cwd is whatever launched it (Tauri, a shell, etc.), and a
    # frozen executable has no repo checkout next to it, so settings.yml must
    # live in a stable, user-writable location instead of "next to the code".
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return os.path.join(base, "winder")


def _default_config_path() -> str:
    config_dir = _user_config_dir()
    config_path = os.path.join(config_dir, "settings.yml")
    if not os.path.exists(config_path):
        example_path = _bundled_example_config_path()
        if os.path.exists(example_path):
            os.makedirs(config_dir, exist_ok=True)
            shutil.copyfile(example_path, config_path)
    return config_path


# Wind(simulation=True) opens "data/motors.db" (a path relative to cwd, see
# src/db.py) — pin cwd to our own data dir so that resolves consistently no
# matter what process/directory launched this sidecar.
os.makedirs(os.path.join(_user_config_dir(), "data"), exist_ok=True)
os.chdir(_user_config_dir())


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.winding import Wind


class OperationState(str, Enum):
    IDLE = "idle"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


class AppState:
    """In-memory state shared between requests. Only one machine/operation at a time."""

    def __init__(self):
        self.lock = threading.Lock()
        self.wind: Optional[Wind] = None
        self.op_state = OperationState.IDLE
        self.operation: Optional[str] = None
        self.pending_wire_idx: Optional[int] = None
        self.message: str = ""
        self.error: Optional[str] = None

    def to_dict(self):
        with self.lock:
            return {
                "connected": self.wind is not None,
                "state": self.op_state.value,
                "operation": self.operation,
                "message": self.message,
                "error": self.error,
            }


state = AppState()
app = FastAPI(title="Winder Control API")
app.add_middleware(
    CORSMiddleware,
    # The Tauri WebView is the only client of this localhost-only service.
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectRequest(BaseModel):
    config_path: Optional[str] = None
    simulation: bool = False


class ConfirmRequest(BaseModel):
    confirmed: bool


class MoveMotorRequest(BaseModel):
    target: float


def _get_wind() -> Wind:
    if state.wind is None:
        raise HTTPException(status_code=503, detail="Machine not connected yet")
    return state.wind


@app.get("/api/config-path")
def config_path():
    return {"config_path": _default_config_path()}


@app.post("/api/connect")
def connect(body: ConnectRequest):
    with state.lock:
        if state.wind is not None:
            raise HTTPException(status_code=400, detail="Already connected")
    config_path = body.config_path or _default_config_path()
    try:
        wind = Wind(config_path, simulation=body.simulation)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect using '{config_path}': {exc}"
        ) from exc
    with state.lock:
        state.wind = wind
        state.op_state = OperationState.IDLE
        state.message = "Connected"
    return {"status": "connected", "simulation": body.simulation, "config_path": config_path}


@app.post("/api/disconnect")
def disconnect():
    with state.lock:
        if state.wind is not None:
            state.wind.close()
        state.wind = None
        state.op_state = OperationState.IDLE
        state.operation = None
        state.message = "Disconnected"
    return {"status": "disconnected"}


@app.get("/api/status")
def status():
    body = state.to_dict()
    if state.wind is not None:
        try:
            body["positions"] = {
                "M0": state.wind.get_motor_position(0),
                "M1": state.wind.get_motor_position(1),
                "M2": state.wind.get_motor_position(2),
                "M3": state.wind.get_motor_position(3),
            }
        except Exception:
            body["positions"] = None
    else:
        body["positions"] = None
    return body


def _require_idle():
    if state.op_state != OperationState.IDLE:
        raise HTTPException(
            status_code=409, detail=f"An operation is already {state.op_state.value}"
        )


@app.post("/api/wind/{wire_idx}/precheck")
def wind_precheck(wire_idx: int):
    """Mirrors the CLI's wire-position confirmation step, before winding starts."""
    wind = _get_wind()
    with state.lock:
        _require_idle()
        if wind.starts_at != 0:
            state.op_state = OperationState.AWAITING_CONFIRMATION
            state.operation = f"wind_wire_{wire_idx}"
            state.pending_wire_idx = wire_idx
            state.message = "Ready to start winding."
            return {"confirmation_required": False, "message": state.message}

        starting_from_cw = wind.is_starting_from_cw(wire_idx)
        side = "left" if starting_from_cw else "right"
        state.op_state = OperationState.AWAITING_CONFIRMATION
        state.operation = f"wind_wire_{wire_idx}"
        state.pending_wire_idx = wire_idx
        state.message = f"Place the wire on the {side} side, then confirm to continue."
        return {"confirmation_required": True, "side": side, "message": state.message}


def _run_in_background(target_fn, operation_name):
    def _runner():
        with state.lock:
            state.op_state = OperationState.RUNNING
            state.operation = operation_name
            state.error = None
        try:
            target_fn()
            with state.lock:
                state.op_state = OperationState.DONE
                state.message = f"{operation_name} finished"
        except Exception as exc:
            traceback.print_exc()
            with state.lock:
                state.op_state = OperationState.ERROR
                state.error = str(exc)

    threading.Thread(target=_runner, daemon=True).start()


@app.post("/api/wind/{wire_idx}/confirm")
def wind_confirm(wire_idx: int, body: ConfirmRequest):
    wind = _get_wind()
    with state.lock:
        if (
            state.op_state != OperationState.AWAITING_CONFIRMATION
            or state.pending_wire_idx != wire_idx
        ):
            raise HTTPException(status_code=409, detail="No pending confirmation for this wire")
        if not body.confirmed:
            state.op_state = OperationState.IDLE
            state.operation = None
            state.pending_wire_idx = None
            state.message = "Winding canceled"
            return {"status": "canceled"}

    def _do_wind():
        wind.init_position(True)
        wind.wind(wire_idx)
        wind.move_motor(0, wind.m0_zero)

    _run_in_background(_do_wind, f"wind_wire_{wire_idx}")
    return {"status": "started"}


@app.post("/api/wind/continuous/precheck")
def continuous_precheck():
    result = wind_precheck(0)
    with state.lock:
        state.operation = "continuous_winding"
    return result


@app.post("/api/wind/continuous/confirm")
def continuous_confirm(body: ConfirmRequest):
    wind = _get_wind()
    with state.lock:
        if state.op_state != OperationState.AWAITING_CONFIRMATION:
            raise HTTPException(status_code=409, detail="No pending confirmation")
        if not body.confirmed:
            state.op_state = OperationState.IDLE
            state.operation = None
            state.pending_wire_idx = None
            state.message = "Winding canceled"
            return {"status": "canceled"}

    _run_in_background(wind.continuous_winding, "continuous_winding")
    return {"status": "started"}


@app.post("/api/estop")
def estop():
    wind = _get_wind()
    wind.estop()
    with state.lock:
        state.op_state = OperationState.IDLE
        state.operation = None
        state.message = "Emergency stop triggered"
    return {"status": "stopped"}


@app.post("/api/motor/{motor_id}/move")
def move_motor(motor_id: int, body: MoveMotorRequest):
    """Move a single motor to an arbitrary position, for initial calibration (see scripts/calib.py)."""
    wind = _get_wind()
    if motor_id not in (0, 1, 2, 3):
        raise HTTPException(status_code=400, detail="motor_id must be 0, 1, 2, or 3")
    with state.lock:
        _require_idle()
    wind.move_motor(motor_id, body.target)
    return {"status": "ok"}


@app.post("/api/state/reset")
def reset_state():
    """Clear a DONE/ERROR state so a new operation can be started."""
    with state.lock:
        state.op_state = OperationState.IDLE
        state.operation = None
        state.error = None
        state.pending_wire_idx = None
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8760)
