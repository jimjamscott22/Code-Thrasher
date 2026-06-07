export const PYODIDE_VERSION = "0.26.4";
export const CDN_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

/** Per-test execution timeout (ms). */
export const DEFAULT_TIMEOUT_MS = 5_000;

/** Maximum combined stdout/stderr characters captured per test run. */
export const MAX_OUTPUT_CHARS = 100_000;
