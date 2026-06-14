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
    // Registra el modulo `pycode` con helpers para Track 2 (datasets).
    // Uso desde el editor:
    //   df = await pycode.load_dataset("iris")
    // La carga del CDN de pandas la dispara loadPackagesFromImports cuando
    // el codigo del estudiante haga `import pandas as pd`.
    await this.py.runPythonAsync(`
import sys, types

if 'pycode' not in sys.modules:
    _mod = types.ModuleType('pycode')

    async def load_dataset(slug):
        """Carga un dataset curado como pandas.DataFrame.

        Hace fetch a /api/v1/datasets/{slug}/csv (endpoint publico de PyCode).
        Usa await porque el browser no expone HTTP sincronico.
        """
        from pyodide.http import pyfetch
        import io
        import pandas as pd
        response = await pyfetch(f'/api/v1/datasets/{slug}/csv')
        if response.status != 200:
            raise FileNotFoundError(
                f'Dataset no encontrado: {slug!r} (status {response.status})'
            )
        text = await response.string()
        return pd.read_csv(io.StringIO(text))

    _mod.load_dataset = load_dataset
    sys.modules['pycode'] = _mod
`);
    return { ready: true, pyodideVersion: this.py.version };
  }

  /**
   * Configura matplotlib lazy: backend Agg + hook plt.show() que emite
   * PNG base64 en stdout con marker. Solo corre cuando el codigo del
   * estudiante importa matplotlib (detectado por loadPackagesFromImports).
   * Idempotente — re-ejecutar no rompe nada.
   */
  private async setupMatplotlibHookIfLoaded(): Promise<void> {
    if (!this.py) return;
    // Solo aplica el hook si matplotlib quedo cargado (sino, no perdamos
    // tiempo importandolo desde Python). Pyodide expone loadedPackages.
    const loaded = (this.py as unknown as { loadedPackages?: Record<string, string> })
      .loadedPackages;
    if (!loaded || !("matplotlib" in loaded)) return;
    await this.py.runPythonAsync(`
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as _plt
import io as _io
import base64 as _b64

if not getattr(_plt.show, '_pycode_patched', False):
    def _pycode_show(*args, **kwargs):
        fig = _plt.gcf()
        if not fig.get_axes():
            return
        buf = _io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        _plt.close(fig)
        buf.seek(0)
        encoded = _b64.b64encode(buf.read()).decode('ascii')
        print(f'<<MATPLOTLIB_PNG:{encoded}>>')
    _pycode_show._pycode_patched = True
    _plt.show = _pycode_show
`);
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
      // Carga numpy/pandas/etc desde el CDN de Pyodide si el codigo los importa.
      await this.py!.loadPackagesFromImports(code);
      // Si matplotlib quedo cargado, monta el hook de plt.show().
      await this.setupMatplotlibHookIfLoaded();
      await Promise.race([this.py!.runPythonAsync(code), timeoutPromise]);
      const { stdout, images } = extractImagesFromStdout(
        this.stdoutBuf.join("\n"),
      );
      return {
        ok: true,
        stdout,
        stderr: this.stderrBuf.join("\n"),
        durationMs: performance.now() - start,
        timedOut: false,
        images,
      };
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      const { stdout, images } = extractImagesFromStdout(
        this.stdoutBuf.join("\n"),
      );
      return {
        ok: false,
        stdout,
        stderr:
          this.stderrBuf.join("\n") +
          (this.stderrBuf.length ? "\n" : "") +
          msg,
        durationMs: performance.now() - start,
        timedOut,
        error: msg,
        images,
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

    // Pre-carga paquetes (numpy, pandas, etc.) escaneando los imports de
    // studentCode + todos los tests en una sola pasada. Los paquetes
    // quedan disponibles en el runtime de Pyodide para el resto de la
    // sesion; los namespaces frescos por test no los pierden.
    const allCode =
      studentCode + "\n" + tests.map((t) => t.code).join("\n");
    await this.py!.loadPackagesFromImports(allCode);

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

    // Pre-carga paquetes (numpy/pandas/etc.) desde los archivos del
    // estudiante + los tests, antes de empezar el loop.
    const allCode =
      files.map((f) => f.content).join("\n") +
      "\n" +
      tests.map((t) => t.code).join("\n");
    await this.py!.loadPackagesFromImports(allCode);

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

// Extrae PNGs base64 emitidos por el hook de plt.show() en stdout.
// El hook imprime `<<MATPLOTLIB_PNG:BASE64DATA>>`; capturamos cada match
// y devolvemos el stdout SIN los markers para que el editor no muestre
// la data binaria como texto.
const MPL_PNG_REGEX = /<<MATPLOTLIB_PNG:([A-Za-z0-9+/=]+)>>/g;

function extractImagesFromStdout(stdout: string): {
  stdout: string;
  images: string[];
} {
  const images: string[] = [];
  let m: RegExpExecArray | null;
  MPL_PNG_REGEX.lastIndex = 0;
  while ((m = MPL_PNG_REGEX.exec(stdout)) !== null) {
    images.push(m[1]);
  }
  const cleaned = stdout.replace(MPL_PNG_REGEX, "").replace(/\n{3,}/g, "\n\n");
  return { stdout: cleaned.trim() === "" && images.length > 0 ? "" : cleaned, images };
}

Comlink.expose(new Kernel());
