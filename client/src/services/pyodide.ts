// Loads Pyodide from CDN and runs Python code in the browser.
// The first call to runPython triggers a ~10 MB download; all subsequent calls are instant.

const PYODIDE_VERSION = "0.26.4";
const CDN_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

interface PyodideInstance {
  runPythonAsync(code: string): Promise<unknown>;
  setStdout(options: { batched: (text: string) => void }): void;
  setStderr(options: { batched: (text: string) => void }): void;
}

declare global {
  interface Window {
    loadPyodide(config: { indexURL: string }): Promise<PyodideInstance>;
  }
}

export interface RunResult {
  stdout: string;
  stderr: string;
  durationMs: number;
}

let _instance: PyodideInstance | null = null;
let _loading: Promise<PyodideInstance> | null = null;

function injectScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve();
      return;
    }
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error(`Failed to load ${src}`));
    document.head.appendChild(s);
  });
}

export function getPyodide(): Promise<PyodideInstance> {
  if (_instance) return Promise.resolve(_instance);
  if (_loading) return _loading;
  _loading = injectScript(`${CDN_BASE}pyodide.js`)
    .then(() => window.loadPyodide({ indexURL: CDN_BASE }))
    .then((p) => {
      _instance = p;
      return p;
    });
  return _loading;
}

export async function runPython(code: string): Promise<RunResult> {
  const pyodide = await getPyodide();

  const outLines: string[] = [];
  const errLines: string[] = [];

  pyodide.setStdout({ batched: (l) => outLines.push(l) });
  pyodide.setStderr({ batched: (l) => errLines.push(l) });

  const start = performance.now();
  try {
    // Run in a fresh namespace so repeated calls don't share state
    await pyodide.runPythonAsync(
      `exec(${JSON.stringify(code)}, {"__name__": "__main__"})`
    );
  } catch (e: unknown) {
    errLines.push(e instanceof Error ? e.message : String(e));
  }
  const durationMs = Math.round(performance.now() - start);

  // Restore defaults so stray output doesn't accumulate
  pyodide.setStdout({ batched: (l) => console.log("[py]", l) });
  pyodide.setStderr({ batched: (l) => console.error("[py]", l) });

  return {
    stdout: outLines.join("\n"),
    stderr: errLines.join("\n"),
    durationMs,
  };
}
