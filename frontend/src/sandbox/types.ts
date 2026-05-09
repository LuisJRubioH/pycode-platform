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

export interface HiddenTest {
  name: string;
  code: string;
}

export interface TestVerdict {
  name: string;
  passed: boolean;
  errorMessage?: string;
}

export interface RunTestsRequest {
  studentCode: string;
  tests: HiddenTest[];
  timeoutMs?: number;
}

export interface RunTestsResult {
  total: number;
  passed: number;
  verdicts: TestVerdict[];
  durationMs: number;
}
