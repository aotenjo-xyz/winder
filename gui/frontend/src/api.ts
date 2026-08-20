// Thin client for the FastAPI backend (bundled as a Tauri sidecar).
const BASE_URL = "http://127.0.0.1:8760";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request to ${path} failed (${res.status})`);
  }
  return res.json();
}

export interface StatusResponse {
  connected: boolean;
  state: "idle" | "awaiting_confirmation" | "running" | "done" | "error";
  operation: string | null;
  message: string;
  error: string | null;
  positions: Record<"M0" | "M1" | "M2" | "M3", number> | null;
}

export interface PrecheckResponse {
  confirmation_required: boolean;
  side?: "left" | "right";
  message: string;
}

export const api = {
  configPath: () => request<{ config_path: string }>("/api/config-path"),
  connect: (simulation: boolean, configPath?: string) =>
    request<{ status: string; config_path: string }>("/api/connect", {
      method: "POST",
      body: JSON.stringify({ config_path: configPath ?? null, simulation }),
    }),
  disconnect: () => request<{ status: string }>("/api/disconnect", { method: "POST" }),
  status: () => request<StatusResponse>("/api/status"),
  windPrecheck: (wireIdx: number) =>
    request<PrecheckResponse>(`/api/wind/${wireIdx}/precheck`, { method: "POST" }),
  windConfirm: (wireIdx: number, confirmed: boolean) =>
    request<{ status: string }>(`/api/wind/${wireIdx}/confirm`, {
      method: "POST",
      body: JSON.stringify({ confirmed }),
    }),
  continuousPrecheck: () =>
    request<PrecheckResponse>("/api/wind/continuous/precheck", { method: "POST" }),
  continuousConfirm: (confirmed: boolean) =>
    request<{ status: string }>("/api/wind/continuous/confirm", {
      method: "POST",
      body: JSON.stringify({ confirmed }),
    }),
  estop: () => request<{ status: string }>("/api/estop", { method: "POST" }),
  resetState: () => request<{ status: string }>("/api/state/reset", { method: "POST" }),
};
