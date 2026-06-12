import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "@/api/client";
import CodeEditor from "@/components/editor/CodeEditor";
import ExerciseGuidePanel from "@/components/exercise/ExerciseGuidePanel";
import { getPyodide, runPythonTests } from "@/services/pyodide";
import { useAuthStore } from "@/store/useAuthStore";
import { useProgressStore } from "@/store/useProgressStore";
import type {
  ExerciseDetail as ExerciseDetailType,
  ExerciseListItem,
  SubmitResponse,
  TestCaseResult,
} from "@/types";

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
  const navigate = useNavigate();
  const [exercise, setExercise] = useState<ExerciseDetailType | null>(null);
  const [navExercises, setNavExercises] = useState<ExerciseListItem[]>([]);
  const [code, setCode] = useState("");
  const [result, setResult] = useState<(SubmitResponse & { stdout: string; stderr: string }) | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pyodideReady, setPyodideReady] = useState(false);
  const user = useAuthStore((state) => state.user);
  const {
    exercises: progress,
    fetch: fetchProgress,
    reset: resetProgress,
  } = useProgressStore();
  const exerciseProgress = id ? progress[Number(id)] : undefined;
  const currentExerciseId = id ? Number(id) : undefined;
  const currentIndex = useMemo(
    () => navExercises.findIndex((item) => item.id === currentExerciseId),
    [currentExerciseId, navExercises],
  );
  const canNavigate = navExercises.length > 1 && currentIndex >= 0;
  const previousExercise = canNavigate
    ? navExercises[(currentIndex - 1 + navExercises.length) % navExercises.length]
    : undefined;
  const nextExercise = canNavigate
    ? navExercises[(currentIndex + 1) % navExercises.length]
    : undefined;

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    setResult(null);

    api
      .get<ExerciseDetailType>(`/exercises/${id}`)
      .then((r) => {
        setExercise(r.data);
        setCode(r.data.starter_code || "# Write your solution here\n");
      })
      .catch(() => setError("Exercise not found."))
      .finally(() => setLoading(false));

    api
      .get<ExerciseListItem[]>("/exercises/")
      .then((r) => setNavExercises([...r.data].sort((a, b) => a.id - b.id)))
      .catch(() => setNavExercises([]));

    // Kick off Pyodide download in the background while the user reads the problem
    getPyodide()
      .then(() => setPyodideReady(true))
      .catch(() => {/* will surface as error on submit */});

  }, [id]);

  useEffect(() => {
    if (user) {
      fetchProgress().catch(() => {});
    } else {
      resetProgress();
    }
  }, [fetchProgress, resetProgress, user]);

  function goToExercise(exerciseId: number | undefined) {
    if (!exerciseId) return;
    navigate(`/exercise/${exerciseId}`);
  }

  async function handleSubmit() {
    if (!exercise) return;
    if (!user) {
      navigate("/login", { state: { from: `/exercise/${exercise.id}` } });
      return;
    }
    setSubmitting(true);
    setResult(null);
    setError(null);
    try {
      const visibleTests = exercise.test_cases.filter(
        (testCase) => testCase.expected_output != null,
      );
      const preview = visibleTests.length
        ? await runPythonTests(
            code,
            visibleTests.map((testCase) => ({
              id: testCase.id,
              input_data: testCase.input_data,
              expected_output: testCase.expected_output as string,
              score_weight: testCase.score_weight,
            })),
          )
        : { stdout: "", stderr: "", totalDurationMs: 0 };

      const serverResp = await api.post<SubmitResponse>("/submit/", {
        exercise_id: exercise.id,
        code,
        time_taken_ms: preview.totalDurationMs,
      });

      setResult({ ...serverResp.data, stdout: preview.stdout, stderr: preview.stderr });
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

  if (!exercise)
    return (
      <div className="mx-auto mt-12 max-w-md rounded-lg border border-red-800 bg-red-900/20 p-6 text-center text-red-400">
        {error ?? "Exercise not found."}
      </div>
    );

  const passed = result?.status === "completed";
  const failed = result?.status === "failed";

  return (
    <div className="mx-auto max-w-[96rem] px-4 py-8">
      <div className="grid gap-6 xl:grid-cols-[minmax(0,0.9fr)_minmax(0,1.15fr)_minmax(18rem,0.75fr)]">
        {/* Left — problem description */}
        <div className="order-1 space-y-6 xl:order-none">
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

          <div className="overflow-hidden rounded-2xl border border-brand-500/20 bg-gray-950 shadow-[0_0_36px_rgba(34,197,94,0.08)]">
            <div className="flex flex-col gap-4 p-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="font-mono text-[0.65rem] font-semibold uppercase tracking-[0.3em] text-brand-500">
                  Challenge nav
                </p>
                <p className="mt-1 text-sm text-gray-400">
                  Jump around, or cycle through exercises without returning to the list.
                </p>
              </div>

              <div className="flex flex-col gap-2 sm:min-w-72">
                <select
                  value={exercise.id}
                  onChange={(event) => goToExercise(Number(event.target.value))}
                  className="w-full rounded-xl border border-gray-700 bg-gray-900 px-3 py-2 text-sm text-gray-100 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
                  aria-label="Choose exercise"
                >
                  {navExercises.length === 0 ? (
                    <option value={exercise.id}>{exercise.title}</option>
                  ) : (
                    navExercises.map((item, index) => (
                      <option key={item.id} value={item.id}>
                        {index + 1}. {item.title}
                      </option>
                    ))
                  )}
                </select>

                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => goToExercise(previousExercise?.id)}
                    disabled={!previousExercise}
                    className="rounded-xl border border-gray-700 px-3 py-2 text-sm font-medium text-gray-300 transition hover:border-brand-500/60 hover:text-white disabled:cursor-not-allowed disabled:border-gray-800 disabled:text-gray-600"
                  >
                    ← Previous
                  </button>
                  <button
                    type="button"
                    onClick={() => goToExercise(nextExercise?.id)}
                    disabled={!nextExercise}
                    className="rounded-xl bg-brand-500 px-3 py-2 text-sm font-semibold text-white transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:bg-gray-800 disabled:text-gray-600"
                  >
                    Next →
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="prose prose-invert prose-sm max-w-none rounded-xl border border-gray-800 bg-gray-900 p-5">
            <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-gray-300">
              {exercise.description}
            </pre>
          </div>

        </div>

        {/* Right — editor + submit */}
        <div className="order-3 flex flex-col gap-4 xl:order-none">
          <CodeEditor value={code} onChange={setCode} height="480px" />

          {!user && (
            <div className="rounded-xl border border-brand-500/20 bg-gray-950 p-4 text-sm text-gray-400">
              <p>
                Log in before submitting to save this attempt and update your progress.
              </p>
              <Link
                to="/login"
                state={{ from: `/exercise/${exercise.id}` }}
                className="mt-3 inline-flex rounded-lg bg-brand-500 px-3 py-2 text-sm font-semibold text-white transition hover:bg-brand-600"
              >
                Login to submit
              </Link>
            </div>
          )}

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
              : user
                ? "Run & Submit"
                : "Login to Submit"}
          </button>

          {error && (
            <div className="rounded-xl border border-red-800 bg-red-900/20 p-4 text-sm text-red-400">
              {error}
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
              {passed && nextExercise && (
                <Link
                  to={`/exercise/${nextExercise.id}`}
                  className="mt-4 inline-flex w-full items-center justify-center rounded-xl bg-brand-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-600 sm:w-auto"
                >
                  Continue to next challenge: {nextExercise.title} →
                </Link>
              )}
            </div>
          )}
        </div>

        <div className="order-2 xl:order-none">
          <ExerciseGuidePanel
            exerciseId={exercise.id}
            guide={exercise.guide}
            fallbackHint={exercise.hint}
            hasSolution={exercise.has_solution}
          />
        </div>
      </div>
    </div>
  );
}
