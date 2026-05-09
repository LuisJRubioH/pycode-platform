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
