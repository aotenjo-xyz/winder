import { useEffect, useState, useCallback } from "react";
import { api, StatusResponse } from "./api";
import "./App.css";

type PendingConfirmation = {
  target: "wire" | "continuous";
  wireIdx?: number;
  message: string;
};

function App() {
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [configPath, setConfigPath] = useState<string | null>(null);
  const [connectError, setConnectError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [pending, setPending] = useState<PendingConfirmation | null>(null);
  const [calibMotorId, setCalibMotorId] = useState(0);
  const [calibTarget, setCalibTarget] = useState("0");
  const [calibError, setCalibError] = useState<string | null>(null);

  const refreshStatus = useCallback(async () => {
    try {
      const s = await api.status();
      setStatus(s);
    } catch {
      setStatus(null);
    }
  }, []);

  useEffect(() => {
    refreshStatus();
    const interval = setInterval(refreshStatus, 1000);
    return () => clearInterval(interval);
  }, [refreshStatus]);

  useEffect(() => {
    api.configPath().then((r) => setConfigPath(r.config_path)).catch(() => setConfigPath(null));
  }, []);

  const connect = async (simulation: boolean) => {
    setConnectError(null);
    try {
      await api.connect(simulation);
      await refreshStatus();
    } catch (err) {
      setConnectError((err as Error).message);
    }
  };

  const startWire = async (wireIdx: number) => {
    setActionError(null);
    try {
      const result = await api.windPrecheck(wireIdx);
      if (result.confirmation_required) {
        setPending({ target: "wire", wireIdx, message: result.message });
      } else {
        await api.windConfirm(wireIdx, true);
      }
    } catch (err) {
      setActionError((err as Error).message);
    }
  };

  const startContinuous = async () => {
    setActionError(null);
    try {
      const result = await api.continuousPrecheck();
      setPending({ target: "continuous", message: result.message });
    } catch (err) {
      setActionError((err as Error).message);
    }
  };

  const resolveConfirmation = async (confirmed: boolean) => {
    if (!pending) return;
    try {
      if (pending.target === "wire" && pending.wireIdx !== undefined) {
        await api.windConfirm(pending.wireIdx, confirmed);
      } else {
        await api.continuousConfirm(confirmed);
      }
    } catch (err) {
      setActionError((err as Error).message);
    } finally {
      setPending(null);
      refreshStatus();
    }
  };

  const estop = async () => {
    try {
      await api.estop();
    } catch (err) {
      setActionError((err as Error).message);
    } finally {
      refreshStatus();
    }
  };

  const moveMotor = async () => {
    setCalibError(null);
    const target = Number(calibTarget);
    if (Number.isNaN(target)) {
      setCalibError("Enter a valid number");
      return;
    }
    try {
      await api.moveMotor(calibMotorId, target);
    } catch (err) {
      setCalibError((err as Error).message);
    } finally {
      refreshStatus();
    }
  };

  const busy = status?.state === "running" || status?.state === "awaiting_confirmation";

  return (
    <main className="container">
      <h1>Winder Control</h1>

      {!status?.connected && (
        <section className="card">
          <h2>Connect to machine</h2>
          {configPath && <p className="message">Settings file: {configPath}</p>}
          <div className="row">
            <button onClick={() => connect(false)}>Connect (hardware)</button>
            <button onClick={() => connect(true)}>Connect (simulation)</button>
          </div>
          {connectError && <p className="error">{connectError}</p>}
        </section>
      )}

      {status?.connected && (
        <>
          <section className="card">
            <h2>Motor positions</h2>
            <div className="positions">
              {status.positions &&
                Object.entries(status.positions).map(([id, value]) => (
                  <div key={id} className="position">
                    <span className="label">{id}</span>
                    <span className="value">{value.toFixed(3)}</span>
                  </div>
                ))}
            </div>
            <p className="status-line">
              State: <strong>{status.state}</strong>
              {status.operation ? ` (${status.operation})` : ""}
            </p>
            {status.message && <p className="message">{status.message}</p>}
            {status.error && <p className="error">{status.error}</p>}
          </section>

          <section className="card">
            <h2>Wind wires</h2>
            <div className="row">
              <button disabled={busy} onClick={() => startWire(0)}>
                Wind wire 0
              </button>
              <button disabled={busy} onClick={() => startWire(1)}>
                Wind wire 1
              </button>
              <button disabled={busy} onClick={() => startWire(2)}>
                Wind wire 2
              </button>
              <button disabled={busy} onClick={startContinuous}>
                Continuous winding
              </button>
            </div>
            {actionError && <p className="error">{actionError}</p>}
          </section>

          <section className="card">
            <h2>Calibration</h2>
            <p className="message">Move a single motor to an exact position (for finding zero positions).</p>
            <div className="row">
              <select
                value={calibMotorId}
                onChange={(e) => setCalibMotorId(Number(e.target.value))}
              >
                <option value={0}>M0</option>
                <option value={1}>M1</option>
                <option value={2}>M2</option>
                <option value={3}>M3</option>
              </select>
              <input
                type="number"
                step="0.01"
                value={calibTarget}
                onChange={(e) => setCalibTarget(e.target.value)}
              />
              <button disabled={busy} onClick={moveMotor}>
                Move
              </button>
            </div>
            {calibError && <p className="error">{calibError}</p>}
          </section>

          <section className="card danger">
            <button className="estop" onClick={estop}>
              EMERGENCY STOP
            </button>
          </section>
        </>
      )}

      {pending && (
        <div className="modal-backdrop">
          <div className="modal">
            <p>{pending.message}</p>
            <div className="row">
              <button onClick={() => resolveConfirmation(true)}>Yes, continue</button>
              <button onClick={() => resolveConfirmation(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

export default App;
