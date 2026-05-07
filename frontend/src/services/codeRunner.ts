import { getSandbox, type RunResult } from "@/sandbox";

export type { RunResult };

export async function runPythonCode(
  code: string,
  timeoutMs = 30_000,
): Promise<RunResult> {
  const sandbox = getSandbox();
  return sandbox.run(code, timeoutMs);
}

export function getCodeRunner() {
  return getSandbox();
}
