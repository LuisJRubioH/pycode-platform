import * as Comlink from "comlink";
import type { RunRequest, RunResult, KernelInfo, RunStatus } from "./types";

export class PyodideSandbox {
  private worker: Worker | null = null;
  private kernel: Comlink.Remote<{
    init(): Promise<KernelInfo>;
    run(req: RunRequest): Promise<RunResult>;
  }> | null = null;
  private _status: RunStatus = "idle";
  private listeners = new Set<(s: RunStatus) => void>();

  get status(): RunStatus {
    return this._status;
  }

  onStatusChange(cb: (s: RunStatus) => void): () => void {
    this.listeners.add(cb);
    return () => {
      this.listeners.delete(cb);
    };
  }

  private setStatus(s: RunStatus) {
    this._status = s;
    this.listeners.forEach((l) => l(s));
  }

  async init(): Promise<void> {
    if (this.kernel) return;
    this.setStatus("loading");
    this.worker = new Worker(
      new URL("./pyodideWorker.ts", import.meta.url),
      { type: "module", name: "pyodide-kernel" },
    );
    this.kernel = Comlink.wrap(this.worker);
    await this.kernel.init();
    this.setStatus("ready");
  }

  async run(code: string, timeoutMs = 30_000): Promise<RunResult> {
    await this.init();
    this.setStatus("running");
    try {
      const result = await this.kernel!.run({ code, timeoutMs });
      this.setStatus(result.ok ? "ready" : "error");
      return result;
    } catch (e) {
      this.setStatus("error");
      throw e;
    }
  }

  async restartKernel(): Promise<void> {
    this.dispose();
    await this.init();
  }

  dispose(): void {
    this.worker?.terminate();
    this.worker = null;
    this.kernel = null;
    this.setStatus("idle");
  }
}

let _singleton: PyodideSandbox | null = null;
export function getSandbox(): PyodideSandbox {
  if (!_singleton) _singleton = new PyodideSandbox();
  return _singleton;
}
