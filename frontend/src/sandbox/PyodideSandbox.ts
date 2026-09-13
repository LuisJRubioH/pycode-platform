import * as Comlink from "comlink";
import type {
  RunRequest,
  RunResult,
  KernelInfo,
  RunStatus,
  RunTestsRequest,
  RunTestsResult,
  RunCapstoneTestsRequest,
  CapstoneFileInput,
  HiddenTest,
} from "./types";
import {
  conWatchdog,
  SandboxAbortedError,
  SandboxTimeoutError,
} from "./watchdog";

/**
 * Margen sobre el timeout que el propio worker aplica a cada tramo. Ese timeout
 * de dentro solo funciona con codigo asincrono; el de aqui es el que salva de
 * un `while True:` (issue #32), y por eso va un poco por encima: primero se le
 * da al worker la oportunidad de cortar por las buenas.
 */
const MARGEN_WATCHDOG_MS = 3_000;

export class PyodideSandbox {
  private worker: Worker | null = null;
  private kernel: Comlink.Remote<{
    init(): Promise<KernelInfo>;
    run(req: RunRequest, latido?: () => void): Promise<RunResult>;
    runTests(req: RunTestsRequest, latido?: () => void): Promise<RunTestsResult>;
    runCapstoneTests(
      req: RunCapstoneTestsRequest,
      latido?: () => void,
    ): Promise<RunTestsResult>;
    setAuthToken(token: string): Promise<void>;
  }> | null = null;
  private _status: RunStatus = "idle";
  private listeners = new Set<(s: RunStatus) => void>();
  /**
   * Ultimo token empujado al worker. Se guarda aqui porque al matar el worker
   * (watchdog o boton de detener) el nuevo nace sin el, y `pycode.llm_complete`
   * dejaria de autenticarse hasta la siguiente ejecucion que lo reenvie.
   */
  private authToken = "";
  /**
   * Rechazos de las operaciones que esperan respuesta del worker actual. Es un
   * conjunto y no un unico campo porque el editor permite "Ejecutar" y
   * "Ejecutar tests" a la vez: al matar el worker hay que soltar a todas, o la
   * que no se rechace se queda esperando para siempre.
   */
  private enVuelo = new Set<(e: Error) => void>();

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
    if (this.authToken) await this.kernel.setAuthToken(this.authToken);
    this.setStatus("ready");
  }

  /** Empuja el token de sesion al worker para las llamadas LLM (Track 5). */
  async setAuthToken(token: string): Promise<void> {
    this.authToken = token || "";
    await this.init();
    await this.kernel!.setAuthToken(this.authToken);
  }

  /**
   * Corre una operacion del kernel bajo el limite duro del hilo principal.
   *
   * El worker avisa con un latido antes de cada tramo de codigo del alumno. Si
   * deja de latir, esta bloqueado en codigo sincrono y no hay nada que negociar:
   * se termina y se levanta otro en la siguiente llamada.
   */
  private async vigilada<T>(
    op: (latido: () => void) => Promise<T>,
    timeoutMs: number,
  ): Promise<T> {
    // Si el worker muere (abortado, reiniciado o por el watchdog), la llamada
    // pendiente no se resuelve nunca: hay que rechazarla desde aqui o el
    // editor se queda esperando.
    let rechazar!: (e: Error) => void;
    const cortada = new Promise<never>((_, reject) => {
      rechazar = reject;
    });
    this.enVuelo.add(rechazar);
    const limiteMs = timeoutMs + MARGEN_WATCHDOG_MS;
    // El watchdog vigila ESTE worker. Si para entonces ya hay otro (porque se
    // abortó y se relanzó), su temporizador rezagado no debe matarlo.
    const vigilado = this.worker;
    try {
      return await Promise.race([
        conWatchdog(op, limiteMs, () => {
          if (this.worker === vigilado) {
            this.dispose(new SandboxTimeoutError(limiteMs));
          }
        }),
        cortada,
      ]);
    } finally {
      this.enVuelo.delete(rechazar);
    }
  }

  async run(code: string, timeoutMs = 30_000): Promise<RunResult> {
    await this.init();
    this.setStatus("running");
    try {
      const result = await this.vigilada(
        (latido) =>
          this.kernel!.run({ code, timeoutMs }, Comlink.proxy(latido)),
        timeoutMs,
      );
      this.setStatus(result.ok ? "ready" : "error");
      return result;
    } catch (e) {
      this.setStatus("error");
      throw e;
    }
  }

  async runTests(
    studentCode: string,
    tests: { name: string; code: string }[],
    timeoutMs = 30_000,
  ): Promise<RunTestsResult> {
    await this.init();
    this.setStatus("running");
    try {
      const result = await this.vigilada(
        (latido) =>
          this.kernel!.runTests(
            { studentCode, tests, timeoutMs },
            Comlink.proxy(latido),
          ),
        timeoutMs,
      );
      this.setStatus(result.passed === result.total ? "ready" : "error");
      return result;
    } catch (e) {
      this.setStatus("error");
      throw e;
    }
  }

  async runCapstoneTests(
    files: CapstoneFileInput[],
    tests: HiddenTest[],
    timeoutMs = 30_000,
  ): Promise<RunTestsResult> {
    await this.init();
    this.setStatus("running");
    try {
      const result = await this.vigilada(
        (latido) =>
          this.kernel!.runCapstoneTests(
            { files, tests, timeoutMs },
            Comlink.proxy(latido),
          ),
        timeoutMs,
      );
      this.setStatus(result.passed === result.total ? "ready" : "error");
      return result;
    } catch (e) {
      this.setStatus("error");
      throw e;
    }
  }

  /**
   * Corta la ejecucion en curso a peticion del alumno. Matar el worker es la
   * unica via: si su codigo es sincrono, el worker no puede atender ningun
   * mensaje. Las ejecuciones en vuelo se rechazan con `SandboxAbortedError`.
   */
  abortRun(): void {
    if (!this.worker) return;
    this.dispose(new SandboxAbortedError());
  }

  /** True si hay algo ejecutandose ahora mismo en el worker. */
  get isRunning(): boolean {
    return this._status === "running";
  }

  async restartKernel(): Promise<void> {
    this.dispose();
    await this.init();
  }

  /**
   * Mata el worker. Lo que estuviera esperando su respuesta se rechaza con
   * `motivo` (por defecto, abortado): el worker ya no va a contestar.
   */
  dispose(motivo: Error = new SandboxAbortedError()): void {
    this.worker?.terminate();
    this.worker = null;
    this.kernel = null;
    const pendientes = [...this.enVuelo];
    this.enVuelo.clear();
    pendientes.forEach((rechazar) => rechazar(motivo));
    this.setStatus("idle");
  }
}

let _singleton: PyodideSandbox | null = null;
export function getSandbox(): PyodideSandbox {
  if (!_singleton) _singleton = new PyodideSandbox();
  return _singleton;
}