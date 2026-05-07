export type RunStatus = "idle" | "loading" | "running" | "ready" | "error";

export interface RunResult {
  ok: boolean;
  stdout: string;
  stderr: string;
  durationMs: number;
  timedOut: boolean;
  error?: string;
}

export interface RunRequest {
  code: string;
  timeoutMs?: number;
}

export interface KernelInfo {
  ready: boolean;
  pyodideVersion?: string;
}
