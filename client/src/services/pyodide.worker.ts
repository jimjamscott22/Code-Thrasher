/// <reference lib="webworker" />

import { CDN_BASE } from "./pyodide.constants";
import type { WorkerRequest, WorkerResponse } from "./pyodide.types";

interface PyodideInstance {
  runPythonAsync(code: string): Promise<unknown>;
  setStdout(options: { batched: (text: string) => void }): void;
  setStderr(options: { batched: (text: string) => void }): void;
}

declare function loadPyodide(config: { indexURL: string }): Promise<PyodideInstance>;
declare function importScripts(...urls: string[]): void;

let pyodide: PyodideInstance | null = null;

async function ensurePyodide(): Promise<PyodideInstance> {
  if (pyodide) return pyodide;
  importScripts(`${CDN_BASE}pyodide.js`);
  pyodide = await loadPyodide({ indexURL: CDN_BASE });
  return pyodide;
}

function buildExecutionCode(userCode: string, inputData: string): string {
  if (inputData) {
    return [
      "import sys",
      "from io import StringIO",
      `sys.stdin = StringIO(${JSON.stringify(inputData)})`,
      `exec(${JSON.stringify(userCode)}, {"__name__": "__main__"})`,
    ].join("\n");
  }
  return `exec(${JSON.stringify(userCode)}, {"__name__": "__main__"})`;
}

function runInFreshNamespace(
  instance: PyodideInstance,
  code: string,
  inputData: string,
  maxOutputChars: number,
): Promise<{ stdout: string; stderr: string; outputTruncated: boolean }> {
  const outLines: string[] = [];
  const errLines: string[] = [];
  let capturedChars = 0;
  let outputTruncated = false;

  const capture = (lines: string[], text: string) => {
    if (outputTruncated) return;
    const remaining = maxOutputChars - capturedChars;
    if (remaining <= 0) {
      outputTruncated = true;
      return;
    }
    if (text.length > remaining) {
      lines.push(text.slice(0, remaining));
      capturedChars = maxOutputChars;
      outputTruncated = true;
      return;
    }
    lines.push(text);
    capturedChars += text.length;
  };

  instance.setStdout({ batched: (text) => capture(outLines, text) });
  instance.setStderr({ batched: (text) => capture(errLines, text) });

  return instance
    .runPythonAsync(buildExecutionCode(code, inputData))
    .then(() => ({
      stdout: outLines.join("\n"),
      stderr: errLines.join("\n"),
      outputTruncated,
    }))
    .catch((e: unknown) => {
      const msg = e instanceof Error ? e.message : String(e);
      capture(errLines, msg);
      return {
        stdout: outLines.join("\n"),
        stderr: errLines.join("\n"),
        outputTruncated,
      };
    })
    .finally(() => {
      instance.setStdout({ batched: () => {} });
      instance.setStderr({ batched: () => {} });
    });
}

function post(message: WorkerResponse) {
  self.postMessage(message);
}

self.onmessage = async (event: MessageEvent<WorkerRequest>) => {
  const msg = event.data;

  if (msg.type === "init") {
    try {
      await ensurePyodide();
      post({ type: "ready" });
    } catch (e: unknown) {
      post({
        type: "error",
        id: "init",
        message: e instanceof Error ? e.message : String(e),
      });
    }
    return;
  }

  if (msg.type === "run") {
    const start = performance.now();
    try {
      const instance = await ensurePyodide();
      const result = await runInFreshNamespace(
        instance,
        msg.code,
        msg.inputData,
        msg.maxOutputChars,
      );
      post({
        type: "result",
        id: msg.id,
        ...result,
        durationMs: Math.round(performance.now() - start),
      });
    } catch (e: unknown) {
      post({
        type: "result",
        id: msg.id,
        stdout: "",
        stderr: e instanceof Error ? e.message : String(e),
        durationMs: Math.round(performance.now() - start),
        outputTruncated: false,
      });
    }
  }
};
