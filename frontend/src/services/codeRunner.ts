import {
  getSandbox,
  SandboxAbortedError,
  SandboxTimeoutError,
  type HiddenTest,
  type RunResult,
  type RunTestsResult,
} from "@/sandbox";

export type { RunResult, RunTestsResult, HiddenTest };

export async function runPythonCode(
  code: string,
  timeoutMs = 30_000,
): Promise<RunResult> {
  const sandbox = getSandbox();
  // Empuja el token de sesion al worker para que `pycode.llm_complete`
  // pueda autenticarse contra el proxy LLM (Track 5). El worker no puede
  // leer localStorage, asi que lo pasamos desde el hilo principal.
  const token = localStorage.getItem("pycode_access_token") || "";
  await sandbox.setAuthToken(token);
  return sandbox.run(code, timeoutMs);
}

export async function runHiddenTests(
  studentCode: string,
  tests: HiddenTest[],
  timeoutMs = 30_000,
): Promise<RunTestsResult> {
  const sandbox = getSandbox();
  return sandbox.runTests(studentCode, tests, timeoutMs);
}

/**
 * Detiene lo que este corriendo en el sandbox (boton "Detener", issue #32).
 * Las ejecuciones en curso se rechazan con `SandboxAbortedError`.
 */
export function abortExecution(): void {
  getSandbox().abortRun();
}

/**
 * True si el error viene del propio sandbox (limite de tiempo o detenido por
 * el alumno). Su mensaje ya esta escrito para el alumno y se muestra tal cual.
 */
export function isSandboxInterruption(err: unknown): err is Error {
  return err instanceof SandboxTimeoutError || err instanceof SandboxAbortedError;
}

export function getCodeRunner() {
  return getSandbox();
}
