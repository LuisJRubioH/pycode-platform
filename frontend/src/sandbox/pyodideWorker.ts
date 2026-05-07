/// <reference lib="webworker" />
import * as Comlink from "comlink";
import { loadPyodide, type PyodideInterface } from "pyodide";
import type { RunRequest, RunResult, KernelInfo } from "./types";

const PYODIDE_INDEX_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";

class Kernel {
  private py: PyodideInterface | null = null;
  private stdoutBuf: string[] = [];
  private stderrBuf: string[] = [];

  async init(): Promise<KernelInfo> {
    if (this.py) return { ready: true, pyodideVersion: this.py.version };
    this.py = await loadPyodide({
      indexURL: PYODIDE_INDEX_URL,
      stdout: (line) => this.stdoutBuf.push(line),
      stderr: (line) => this.stderrBuf.push(line),
    });
    return { ready: true, pyodideVersion: this.py.version };
  }

  async run({ code, timeoutMs = 30_000 }: RunRequest): Promise<RunResult> {
    if (!this.py) await this.init();
    this.stdoutBuf = [];
    this.stderrBuf = [];
    const start = performance.now();
    let timedOut = false;
    let timer: number | undefined;

    const timeoutPromise = new Promise<never>((_, reject) => {
      timer = self.setTimeout(() => {
        timedOut = true;
        reject(new Error(`Timeout (${timeoutMs}ms)`));
      }, timeoutMs);
    });

    try {
      await Promise.race([this.py!.runPythonAsync(code), timeoutPromise]);
      return {
        ok: true,
        stdout: this.stdoutBuf.join("\n"),
        stderr: this.stderrBuf.join("\n"),
        durationMs: performance.now() - start,
        timedOut: false,
      };
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      return {
        ok: false,
        stdout: this.stdoutBuf.join("\n"),
        stderr:
          this.stderrBuf.join("\n") +
          (this.stderrBuf.length ? "\n" : "") +
          msg,
        durationMs: performance.now() - start,
        timedOut,
        error: msg,
      };
    } finally {
      if (timer !== undefined) self.clearTimeout(timer);
    }
  }
}

Comlink.expose(new Kernel());
