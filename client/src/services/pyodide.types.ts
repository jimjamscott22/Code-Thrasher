export interface RunResult {
  stdout: string;
  stderr: string;
  durationMs: number;
  timedOut?: boolean;
  outputTruncated?: boolean;
}

export interface TestCaseInput {
  id: number;
  input_data: string;
  expected_output: string;
  score_weight: number;
}

export interface TestRunResult extends RunResult {
  test_case_id: number;
  passed: boolean;
  actual: string;
  expected: string;
}

export interface RunTestsResult {
  results: TestRunResult[];
  totalDurationMs: number;
  stdout: string;
  stderr: string;
}

// ── Worker message protocol ───────────────────────────────────────────────────

export type WorkerRequest =
  | { type: "init" }
  | {
      type: "run";
      id: string;
      code: string;
      inputData: string;
      maxOutputChars: number;
    };

export type WorkerResponse =
  | { type: "ready" }
  | {
      type: "result";
      id: string;
      stdout: string;
      stderr: string;
      durationMs: number;
      outputTruncated: boolean;
    }
  | { type: "error"; id: string; message: string };
