/// <reference lib="webworker" />
import * as Comlink from "comlink";
import { loadPyodide, type PyodideInterface } from "pyodide";
import type {
  RunRequest,
  RunResult,
  KernelInfo,
  RunTestsRequest,
  RunTestsResult,
  RunCapstoneTestsRequest,
  TestVerdict,
} from "./types";

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

  async runTests({
    studentCode,
    tests,
    timeoutMs = 30_000,
  }: RunTestsRequest): Promise<RunTestsResult> {
    if (!this.py) await this.init();
    const start = performance.now();
    const verdicts: TestVerdict[] = [];

    // Cada test corre en un namespace fresco para aislar efectos
    // secundarios entre tests. Concatenamos studentCode + test.code y
    // tratamos "no excepción" como pass.
    for (const test of tests) {
      const ns = this.py!.toPy({});
      const program = `${studentCode}\n\n${test.code}\n`;
      let timer: number | undefined;
      let timedOut = false;
      const timeoutPromise = new Promise<never>((_, reject) => {
        timer = self.setTimeout(() => {
          timedOut = true;
          reject(new Error(`Timeout (${timeoutMs}ms)`));
        }, timeoutMs);
      });
      try {
        await Promise.race([
          this.py!.runPythonAsync(program, { globals: ns }),
          timeoutPromise,
        ]);
        verdicts.push({ name: test.name, passed: true });
      } catch (err) {
        const raw = err instanceof Error ? err.message : String(err);
        verdicts.push({
          name: test.name,
          passed: false,
          errorMessage: timedOut ? `Timeout (${timeoutMs}ms)` : truncateError(raw),
        });
      } finally {
        if (timer !== undefined) self.clearTimeout(timer);
        try {
          ns.destroy();
        } catch {
          /* ns ya liberado */
        }
      }
    }

    return {
      total: tests.length,
      passed: verdicts.filter((v) => v.passed).length,
      verdicts,
      durationMs: performance.now() - start,
    };
  }

  async runCapstoneTests({
    files,
    tests,
    timeoutMs = 30_000,
  }: RunCapstoneTestsRequest): Promise<RunTestsResult> {
    if (!this.py) await this.init();
    const start = performance.now();
    const verdicts: TestVerdict[] = [];

    // Escribe cada archivo del estudiante en el FS de Pyodide y mete
    // /home/pyodide en sys.path para que los imports relativos entre
    // modulos funcionen (`from reports import total_ventas`).
    const baseDir = "/home/pyodide/capstone";
    try {
      this.py!.FS.mkdir(baseDir);
    } catch {
      // ya existe
    }
    // Limpia archivos previos del capstone
    try {
      const prev = this.py!.FS.readdir(baseDir) as string[];
      for (const name of prev) {
        if (name === "." || name === "..") continue;
        try {
          this.py!.FS.unlink(`${baseDir}/${name}`);
        } catch {
          /* ignora */
        }
      }
    } catch {
      /* dir nuevo */
    }
    for (const f of files) {
      const safeName = f.path.replace(/[\\/]/g, "_");
      this.py!.FS.writeFile(`${baseDir}/${safeName}`, f.content);
    }

    // Anade el dir a sys.path una vez
    await this.py!.runPythonAsync(
      `import sys\nif '${baseDir}' not in sys.path: sys.path.insert(0, '${baseDir}')`
    );

    for (const test of tests) {
      const ns = this.py!.toPy({});
      // Limpia el cache de modulos del estudiante para que cada test
      // empiece con un import fresco — evita estado compartido entre tests.
      // Los tests del capstone son responsables de sus propios imports
      // (`from store import SalesStore`, `from reports import ...`).
      const program =
        `import sys\n` +
        `for _mod in list(sys.modules):\n` +
        `    _path = getattr(sys.modules[_mod], '__file__', None) or ''\n` +
        `    if _path.startswith('${baseDir}'):\n` +
        `        del sys.modules[_mod]\n` +
        `${test.code}\n`;

      let timer: number | undefined;
      let timedOut = false;
      const timeoutPromise = new Promise<never>((_, reject) => {
        timer = self.setTimeout(() => {
          timedOut = true;
          reject(new Error(`Timeout (${timeoutMs}ms)`));
        }, timeoutMs);
      });
      try {
        await Promise.race([
          this.py!.runPythonAsync(program, { globals: ns }),
          timeoutPromise,
        ]);
        verdicts.push({ name: test.name, passed: true });
      } catch (err) {
        const raw = err instanceof Error ? err.message : String(err);
        verdicts.push({
          name: test.name,
          passed: false,
          errorMessage: timedOut
            ? `Timeout (${timeoutMs}ms)`
            : truncateError(raw),
        });
      } finally {
        if (timer !== undefined) self.clearTimeout(timer);
        try {
          ns.destroy();
        } catch {
          /* ns ya liberado */
        }
      }
    }

    return {
      total: tests.length,
      passed: verdicts.filter((v) => v.passed).length,
      verdicts,
      durationMs: performance.now() - start,
    };
  }
}

function truncateError(msg: string, maxLines = 6): string {
  const lines = msg.split("\n");
  if (lines.length <= maxLines) return msg;
  return [...lines.slice(0, 2), "...", ...lines.slice(-3)].join("\n");
}

Comlink.expose(new Kernel());
