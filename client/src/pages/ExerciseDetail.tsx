import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "@/api/client";
import CodeEditor from "@/components/editor/CodeEditor";
import { getPyodide, runPython } from "@/services/pyodide";
import { useProgressStore } from "@/store/useProgressStore";
import type { ExerciseDetail as ExerciseDetailType, SubmitResponse, TestCaseResult } from "@/types";

const DIFFICULTY_COLORS = {
  beginner: "text-green-400 bg-green-400/10",
  intermediate: "text-yellow-400 bg-yellow-400/10",
  advanced: "text-red-400 bg-red-400/10",
} as const;

function TestResultRow({
  result,
  isHidden,
}: {
  result: TestCaseResult;
  isHidden: boolean;
}) {
  return (
    <div
      className={`rounded-lg border p-3 font-mono text-xs ${
        result.passed
          ? "border-green-800 bg-green-900/20 text-green-300"
          : "border-red-800 bg-red-900/20 text-red-300"
      }`}
    >
      <div className="flex items-center gap-2">
        <span>{result.passed ? "✓" : "✗"}</span>
        <span className="text-gray-400">
          Test #{result.test_case_id}
          {isHidden && <span className="ml-1 text-gray-600">(hidden)</span>}
        </span>
      </div>
      {!result.passed && (
        <div className="mt-2 space-y-1 pl-5">
          {!isHidden && (
            <p>
              <span className="text-gray-500">expected: </span>
              {result.expected || "(empty)"}
            </p>
          )}
          <p>
            <span className="text-gray-500">got:      </span>
            {result.actual || "(empty)"}
          </p>
          {isHidden && (
            <p className="text-gray-600">expected output is hidden — figure it out!</p>
          )}
        </div>
      )}
    </div>
  );
}

export default function ExerciseDetail() {
  const { id } = useParams<{ id: string }>();
  const [exercise, setExercise] = useState<ExerciseDetailType | null>(null);
  const [code, setCode] = useState("");
  const [result, setResult] = useState<(SubmitResponse & { stdout: string; stderr: string }) | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hintVisible, setHintVisible] = useState(false);
  const [pyodideReady, setPyodideReady] = useState(false);
  const { exercises: progress, fetch: fetchProgress } = useProgressStore();
  const exerciseProgress = id ? progress[Number(id)] : undefined;

  useEffect(() => {
    if (!id) return;
    api
      .get<ExerciseDetailType>(`/exercises/${id}`)
      .then((r) => {
        setExercise(r.data);
        setCode(r.data.starter_code || "# Write your solution here\n");
      })
      .catch(() => setError("Exercise not found."))
      .finally(() => setLoading(false));

    // Kick off Pyodide download in the background while the user reads the problem
    getPyodide()
      .then(() => setPyodideReady(true))
      .catch(() => {/* will surface as error on submit */});

    fetchProgress().catch(() => {});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function handleSubmit() {
    if (!exercise) return;
    setSubmitting(true);
    setResult(null);
    setError(null);
    try {
      const { stdout, stderr, durationMs } = await runPython(code);
      const trimmedActual = stdout.trim();

      const testResults: TestCaseResult[] = exercise.test_cases.map((tc) => ({
        test_case_id: tc.id,
        passed: !stderr && trimmedActual === tc.expected_output.trim(),
        expected: tc.expected_output,
        actual: trimmedActual,
        score_weight: tc.score_weight,
      }));

      const serverResp = await api.post<SubmitResponse>("/submit/", {
        exercise_id: exercise.id,
        code,
        test_results: testResults,
        time_taken_ms: durationMs,
      });

      setResult({ ...serverResp.data, stdout, stderr });
      fetchProgress().catch(() => {});
    } catch (e: unknown) {
      const msg =
        (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Submission failed.";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading)
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
      </div>
    );

  if (error || !exercise)
    return (
      <div className="mx-auto mt-12 max-w-md rounded-lg border border-red-800 bg-red-900/20 p-6 text-center text-red-400">
        {error ?? "Exercise not found."}
      </div>
    );

  const passed = result?.status === "completed";
  const failed = result?.status === "failed";

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Left — problem description */}
        <div className="space-y-6">
          <div>
            <div className="mb-1 flex items-center gap-3">
              <span
                className={`rounded-full px-2 py-0.5 text-xs font-medium ${DIFFICULTY_COLORS[exercise.difficulty_level]}`}
              >
                {exercise.difficulty_level}
              </span>
              {exercise.category && (
                <span className="text-xs text-gray-500">{exercise.category.name}</span>
              )}
            </div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold">{exercise.title}</h1>
              {exerciseProgress?.solved && (
                <span className="rounded-full bg-green-900/40 px-2.5 py-0.5 text-xs font-medium text-green-400 ring-1 ring-green-700">
                  ✓ Solved
                </span>
              )}
              {exerciseProgress && !exerciseProgress.solved && (
                <span className="rounded-full bg-yellow-900/30 px-2.5 py-0.5 text-xs font-medium text-yellow-500 ring-1 ring-yellow-700/50">
                  Best: {exerciseProgress.best_score}%
                </span>
              )}
            </div>
          </div>

          <div className="prose prose-invert prose-sm max-w-none rounded-xl border border-gray-800 bg-gray-900 p-5">
            <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-gray-300">
              {exercise.description}
            </pre>
          </div>

          {exercise.hint && (
            <div className="rounded-xl border border-gray-800 bg-gray-900">
              <button
                onClick={() => setHintVisible((v) => !v)}
                className="flex w-full items-center justify-between px-4 py-3 text-sm text-gray-400 hover:text-white"
              >
                <span>Hint</span>
                <span>{hintVisible ? "▲" : "▼"}</span>
              </button>
              {hintVisible && (
                <p className="border-t border-gray-800 px-4 py-3 text-sm text-yellow-300">
                  {exercise.hint}
                </p>
              )}
            </div>
          )}

          {/* Result panel */}
          {result && (
            <div
              className={`rounded-xl border p-5 ${
                passed
                  ? "border-green-700 bg-green-900/20"
                  : "border-red-700 bg-red-900/20"
              }`}
            >
              <div className="mb-3 flex items-center justify-between">
                <span
                  className={`text-lg font-bold ${passed ? "text-green-400" : "text-red-400"}`}
                >
                  {passed ? "All tests passed!" : `Score: ${result.score}%`}
                </span>
                <span className="text-xs text-gray-500">{result.time_taken_ms}ms</span>
              </div>
              <div className="space-y-2">
                {result.test_results.map((tr) => {
                  const tc = exercise.test_cases.find((t) => t.id === tr.test_case_id);
                  return (
                    <TestResultRow
                      key={tr.test_case_id}
                      result={tr}
                      isHidden={tc?.is_hidden ?? false}
                    />
                  );
                })}
              </div>
              {(result.stdout || result.stderr) && (
                <div className="mt-4 rounded-lg bg-gray-950 p-3 font-mono text-xs">
                  {result.stdout && (
                    <pre className="text-gray-300">{result.stdout}</pre>
                  )}
                  {result.stderr && (
                    <pre className="text-red-400">{result.stderr}</pre>
                  )}
                </div>
              )}
            </div>
          )}

          {error && (
            <div className="rounded-xl border border-red-800 bg-red-900/20 p-4 text-sm text-red-400">
              {error}
            </div>
          )}
        </div>

        {/* Right — editor + submit */}
        <div className="flex flex-col gap-4">
          <CodeEditor value={code} onChange={setCode} height="480px" />

          <button
            onClick={handleSubmit}
            disabled={submitting}
            className={`flex items-center justify-center gap-2 rounded-xl py-3 font-semibold transition ${
              submitting
                ? "cursor-not-allowed bg-gray-700 text-gray-400"
                : passed
                  ? "bg-brand-500 text-white hover:bg-brand-600"
                  : failed
                    ? "bg-red-700 text-white hover:bg-red-600"
                    : "bg-brand-500 text-white hover:bg-brand-600"
            }`}
          >
            {submitting && (
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            )}
            {submitting
              ? pyodideReady
                ? "Running…"
                : "Loading Python runtime…"
              : "Run & Submit"}
          </button>
        </div>
      </div>
    </div>
  );
}
