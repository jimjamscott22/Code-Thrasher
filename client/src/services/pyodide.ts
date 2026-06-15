// Pyodide runs in a dedicated Web Worker so user code cannot block the UI thread.
// Each test case executes in an isolated namespace with enforced timeouts and output limits.

import {
  DEFAULT_TIMEOUT_MS,
  MAX_OUTPUT_CHARS,
} from "./pyodide.constants";
import type {
  RunResult,
  RunTestsResult,
  TestCaseInput,
  TestRunResult,
  WorkerRequest,
  WorkerResponse,
} from "./pyodide.types";

export type { RunResult, RunTestsResult, TestCaseInput, TestRunResult };
export { DEFAULT_TIMEOUT_MS, MAX_OUTPUT_CHARS };

interface PendingRun {
  resolve: (result: RunResult) => void;
  reject: (error: Error) => void;
  timer: ReturnType<typeof setTimeout>;
}

const INIT_TIMEOUT_MS = 30_000;

let worker: Worker | null = null;
let readyPromise: Promise<void> | null = null;
const pending = new Map<string, PendingRun>();
let requestCounter = 0;

function nextRequestId(): string {
  requestCounter += 1;
  return `run-${requestCounter}`;
}

function rejectAllPending(message: string) {
  for (const [id, entry] of pending) {
    clearTimeout(entry.timer);
    entry.reject(new Error(message));
    pending.delete(id);
  }
}

function handleWorkerMessage(event: MessageEvent<WorkerResponse>) {
  const msg = event.data;

  if (msg.type === "ready") {
    return;
  }

  if (msg.type === "error" && msg.id === "init") {
    readyPromise = null;
    rejectAllPending(msg.message);
    return;
  }

  if (msg.type !== "result") return;

  const entry = pending.get(msg.id);
  if (!entry) return;

  clearTimeout(entry.timer);
  pending.delete(msg.id);
  entry.resolve({
    stdout: msg.stdout,
    stderr: msg.stderr,
    durationMs: msg.durationMs,
    outputTruncated: msg.outputTruncated,
  });
}

function spawnWorker(): Worker {
  const instance = new Worker(
    new URL("./pyodide.worker.ts", import.meta.url),
    { type: "module" },
  );
  instance.onmessage = handleWorkerMessage;
  instance.onerror = () => {
    readyPromise = null;
    rejectAllPending("Python worker crashed.");
    worker = null;
  };
  return instance;
}

function ensureWorker(): Worker {
  if (!worker) {
    worker = spawnWorker();
  }
  return worker;
}

function initWorker(): Promise<void> {
  if (readyPromise) return readyPromise;

  readyPromise = new Promise<void>((resolve, reject) => {
    const instance = ensureWorker();

    const onMessage = (event: MessageEvent<WorkerResponse>) => {
      if (event.data.type === "ready") {
        clearTimeout(initTimer);
        instance.removeEventListener("message", onMessage);
        resolve();
      } else if (event.data.type === "error" && event.data.id === "init") {
        clearTimeout(initTimer);
        instance.removeEventListener("message", onMessage);
        readyPromise = null;
        reject(new Error(event.data.message));
      }
    };

    const initTimer = setTimeout(() => {
      instance.removeEventListener("message", onMessage);
      readyPromise = null;
      terminateWorker();
      reject(new Error("Python runtime took too long to load. Check your internet connection and try again."));
    }, INIT_TIMEOUT_MS);

    instance.addEventListener("message", onMessage);
    instance.postMessage({ type: "init" } satisfies WorkerRequest);
  });

  return readyPromise;
}

function terminateWorker() {
  if (worker) {
    worker.terminate();
    worker = null;
  }
  readyPromise = null;
}

async function runInWorker(
  code: string,
  inputData: string,
  timeoutMs: number,
  maxOutputChars: number,
): Promise<RunResult> {
  await initWorker();
  const instance = ensureWorker();
  const id = nextRequestId();

  return new Promise<RunResult>((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      terminateWorker();
      resolve({
        stdout: "",
        stderr: `Execution timed out after ${timeoutMs}ms`,
        durationMs: timeoutMs,
        timedOut: true,
      });
    }, timeoutMs);

    pending.set(id, { resolve, reject, timer });

    instance.postMessage({
      type: "run",
      id,
      code,
      inputData,
      maxOutputChars,
    } satisfies WorkerRequest);
  });
}

/** Preload the Pyodide runtime in the background worker. */
export function getPyodide(): Promise<void> {
  return initWorker();
}

/** Run user code once (fresh namespace). Kept for ad-hoc execution use cases. */
export async function runPython(
  code: string,
  options?: { timeoutMs?: number; maxOutputChars?: number; inputData?: string },
): Promise<RunResult> {
  return runInWorker(
    code,
    options?.inputData ?? "",
    options?.timeoutMs ?? DEFAULT_TIMEOUT_MS,
    options?.maxOutputChars ?? MAX_OUTPUT_CHARS,
  );
}

/** Run each test case in an isolated execution with its own timeout and output cap. */
export async function runPythonTests(
  code: string,
  testCases: TestCaseInput[],
  options?: { timeoutMs?: number; maxOutputChars?: number },
): Promise<RunTestsResult> {
  const timeoutMs = options?.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const maxOutputChars = options?.maxOutputChars ?? MAX_OUTPUT_CHARS;
  const results: TestRunResult[] = [];
  const totalStart = performance.now();

  for (const testCase of testCases) {
    const run = await runInWorker(
      code,
      testCase.input_data,
      timeoutMs,
      maxOutputChars,
    );

    const trimmedActual = run.stdout.trim();
    const trimmedExpected = testCase.expected_output.trim();
    let stderr = run.stderr;
    if (run.outputTruncated) {
      const limitMsg = `Output exceeded ${maxOutputChars} character limit`;
      stderr = stderr ? `${stderr}\n${limitMsg}` : limitMsg;
    }
    const hasError = Boolean(stderr) || run.timedOut;

    results.push({
      test_case_id: testCase.id,
      stdout: run.stdout,
      stderr,
      durationMs: run.durationMs,
      timedOut: run.timedOut,
      outputTruncated: run.outputTruncated,
      actual: trimmedActual,
      expected: testCase.expected_output,
      passed: !hasError && trimmedActual === trimmedExpected,
    });
  }

  const firstFailure = results.find((r) => !r.passed);
  const summaryStdout = firstFailure?.stdout ?? results[0]?.stdout ?? "";
  const summaryStderr = firstFailure?.stderr ?? results.find((r) => r.stderr)?.stderr ?? "";

  return {
    results,
    totalDurationMs: Math.round(performance.now() - totalStart),
    stdout: summaryStdout,
    stderr: summaryStderr,
  };
}
