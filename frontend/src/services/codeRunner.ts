import {
  getSandbox,
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

export function getCodeRunner() {
  return getSandbox();
}
