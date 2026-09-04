import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "@/api/client";
import { useAuthStore } from "@/store/useAuthStore";
import { useProgressStore } from "@/store/useProgressStore";
import type { ExerciseListItem, DifficultyLevel } from "@/types";

const DIFFICULTY_COLORS: Record<DifficultyLevel, string> = {
  beginner: "text-green-400 bg-green-400/10 ring-green-400/20",
  intermediate: "text-yellow-400 bg-yellow-400/10 ring-yellow-400/20",
  advanced: "text-red-400 bg-red-400/10 ring-red-400/20",
};

const DIFFICULTY_CHIP_ACTIVE: Record<DifficultyLevel, string> = {
  beginner: "bg-green-400 text-gray-950",
  intermediate: "bg-yellow-400 text-gray-950",
  advanced: "bg-red-400 text-gray-950",
};

const DIFFICULTIES: DifficultyLevel[] = ["beginner", "intermediate", "advanced"];

type DifficultyFilter = DifficultyLevel | "all";

interface CategoryProgress {
  solved: number;
  total: number;
}

function CheckIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-3.5 w-3.5"
      aria-hidden="true"
    >
      <path d="M4 12.5l5.5 5.5L20 6.5" />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      className="h-3.5 w-3.5 shrink-0"
      aria-hidden="true"
    >
      <circle cx="11" cy="11" r="7" />
      <path d="M20 20l-3.5-3.5" />
    </svg>
  );
}

export default function Dashboard() {
  const [exercises, setExercises] = useState<ExerciseListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [difficulty, setDifficulty] = useState<DifficultyFilter>("all");
  const [unsolvedOnly, setUnsolvedOnly] = useState(false);
  const [query, setQuery] = useState("");
  const user = useAuthStore((state) => state.user);
  const {
    totalExercises,
    completedCount,
    exercises: progress,
    fetch: fetchProgress,
    reset: resetProgress,
  } = useProgressStore();

  useEffect(() => {
    api
      .get<ExerciseListItem[]>("/exercises/")
      .then((r) => setExercises(r.data))
      .catch(() => setError("Failed to load exercises."))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (user) {
      fetchProgress().catch(() => {/* progress is non-critical */});
    } else {
      resetProgress();
      setUnsolvedOnly(false);
    }
  }, [fetchProgress, resetProgress, user]);

  // Per-category totals come from the full list, not the filtered one, so the
  // section progress stays stable while the user narrows the view.
  const categoryProgress = useMemo(() => {
    return exercises.reduce<Record<string, CategoryProgress>>((acc, ex) => {
      const cat = ex.category?.name ?? "Uncategorized";
      const entry = (acc[cat] ??= { solved: 0, total: 0 });
      entry.total += 1;
      if (progress[ex.id]?.solved) entry.solved += 1;
      return acc;
    }, {});
  }, [exercises, progress]);

  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return exercises.filter((ex) => {
      if (difficulty !== "all" && ex.difficulty_level !== difficulty) return false;
      if (unsolvedOnly && progress[ex.id]?.solved) return false;
      if (needle && !ex.title.toLowerCase().includes(needle)) return false;
      return true;
    });
  }, [exercises, difficulty, unsolvedOnly, query, progress]);

  const grouped = useMemo(() => {
    return visible.reduce<Record<string, ExerciseListItem[]>>((acc, ex) => {
      const cat = ex.category?.name ?? "Uncategorized";
      (acc[cat] ??= []).push(ex);
      return acc;
    }, {});
  }, [visible]);

  if (loading)
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
      </div>
    );

  if (error)
    return (
      <div className="mx-auto mt-12 max-w-md rounded-lg border border-red-800 bg-red-900/20 p-6 text-center text-red-400">
        {error}
      </div>
    );

  const pct = totalExercises > 0 ? Math.round((completedCount / totalExercises) * 100) : 0;
  const filtersActive = difficulty !== "all" || unsolvedOnly || query.trim() !== "";

  function clearFilters() {
    setDifficulty("all");
    setUnsolvedOnly(false);
    setQuery("");
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <div className="mb-8 flex items-end justify-between">
        <div>
          <h1 className="mb-1 text-3xl font-bold">Exercises</h1>
          <p className="text-gray-400">Pick a challenge and start thrashing.</p>
        </div>

        {user && totalExercises > 0 && (
          <div className="text-right">
            <p className="text-sm text-gray-400">
              <span className="font-semibold text-white">{completedCount}</span>
              <span className="text-gray-600"> / {totalExercises} solved</span>
            </p>
            <div className="mt-1.5 h-1.5 w-40 overflow-hidden rounded-full bg-gray-800">
              <div
                className="h-full rounded-full bg-brand-500 transition-all duration-500"
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {!user && (
        <div className="mb-8 rounded-2xl border border-brand-500/20 bg-gray-950 p-5">
          <p className="font-mono text-xs font-semibold uppercase tracking-[0.28em] text-brand-500">
            Progress sync
          </p>
          <div className="mt-3 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-sm leading-6 text-gray-400">
              Browse every challenge freely. Log in before submitting to save solved badges,
              attempts, and best scores to your account.
            </p>
            <div className="flex gap-2">
              <Link
                to="/login"
                className="rounded-xl border border-gray-700 px-4 py-2 text-sm font-medium text-gray-300 transition hover:border-brand-500/60 hover:text-white"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="rounded-xl bg-brand-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-600"
              >
                Register
              </Link>
            </div>
          </div>
        </div>
      )}

      {exercises.length > 0 && (
        <div className="mb-8 flex flex-wrap items-center justify-between gap-4 rounded-xl border border-gray-800 bg-gray-900 px-3.5 py-3">
          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={() => setDifficulty("all")}
              aria-pressed={difficulty === "all"}
              className={`rounded-full px-3.5 py-1.5 text-[13px] transition ${
                difficulty === "all"
                  ? "bg-brand-500 font-semibold text-white"
                  : "border border-gray-700 font-medium text-gray-400 hover:text-white"
              }`}
            >
              All
            </button>

            {DIFFICULTIES.map((level) => (
              <button
                key={level}
                type="button"
                onClick={() => setDifficulty(level)}
                aria-pressed={difficulty === level}
                className={`rounded-full px-3.5 py-1.5 text-[13px] capitalize transition ${
                  difficulty === level
                    ? `font-semibold ${DIFFICULTY_CHIP_ACTIVE[level]}`
                    : `font-medium ring-1 ring-inset ${DIFFICULTY_COLORS[level]}`
                }`}
              >
                {level}
              </button>
            ))}

            {user && (
              <>
                <span className="mx-1 h-5 w-px bg-gray-800" aria-hidden="true" />
                <button
                  type="button"
                  onClick={() => setUnsolvedOnly((v) => !v)}
                  aria-pressed={unsolvedOnly}
                  className={`inline-flex items-center gap-2 rounded-full border py-1 pl-2.5 pr-3.5 text-[13px] font-medium transition ${
                    unsolvedOnly
                      ? "border-brand-500/60 text-white"
                      : "border-gray-700 text-gray-400 hover:text-gray-200"
                  }`}
                >
                  <span
                    className={`flex h-4 w-7 items-center rounded-full p-0.5 transition ${
                      unsolvedOnly ? "bg-brand-500" : "bg-gray-800"
                    }`}
                  >
                    <span
                      className={`h-3 w-3 rounded-full transition-transform ${
                        unsolvedOnly ? "translate-x-3 bg-white" : "translate-x-0 bg-gray-500"
                      }`}
                    />
                  </span>
                  Unsolved only
                </button>
              </>
            )}
          </div>

          <div className="flex min-w-[200px] flex-1 items-center gap-2 rounded-lg border border-gray-700 bg-gray-950 px-3 py-1.5 text-gray-600 transition focus-within:border-brand-500/60 sm:flex-none">
            <SearchIcon />
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search exercises"
              aria-label="Search exercises by title"
              className="w-full bg-transparent text-[13px] text-gray-100 placeholder:text-gray-600 focus:outline-none"
            />
          </div>
        </div>
      )}

      {Object.entries(grouped).map(([category, items]) => {
        const catProgress = categoryProgress[category];
        const catPct =
          catProgress && catProgress.total > 0
            ? Math.round((catProgress.solved / catProgress.total) * 100)
            : 0;

        return (
          <section key={category} className="mb-10">
            <div className="mb-4 flex items-center gap-3.5">
              <h2 className="font-mono text-sm font-semibold uppercase tracking-widest text-gray-500">
                {category}
              </h2>
              {user && catProgress && (
                <span className="font-mono text-xs text-gray-700">
                  {catProgress.solved} / {catProgress.total}
                </span>
              )}
              <div className="h-px flex-1 bg-gray-800" />
              {user && catProgress && (
                <div className="h-1 w-[72px] overflow-hidden rounded-full bg-gray-800">
                  <div
                    className="h-full rounded-full bg-brand-500 transition-all duration-500"
                    style={{ width: `${catPct}%` }}
                  />
                </div>
              )}
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {items.map((ex) => {
                const p = progress[ex.id];
                const solved = Boolean(p?.solved);
                return (
                  <Link
                    key={ex.id}
                    to={`/exercise/${ex.id}`}
                    className={`group flex flex-col rounded-xl border bg-gray-900 p-5 transition hover:border-brand-500/50 hover:bg-gray-800 ${
                      solved
                        ? "border-brand-500/30 shadow-[0_0_24px_rgba(34,197,94,0.06)]"
                        : "border-gray-800"
                    }`}
                  >
                    <div className="mb-3 flex items-start justify-between gap-2">
                      <h3
                        className={`font-medium leading-snug group-hover:text-white ${
                          solved ? "text-white" : "text-gray-100"
                        }`}
                      >
                        {ex.title}
                      </h3>
                      <span
                        className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${DIFFICULTY_COLORS[ex.difficulty_level]}`}
                      >
                        {ex.difficulty_level}
                      </span>
                    </div>

                    <div className="mt-auto flex items-center justify-between gap-2">
                      {solved ? (
                        <span className="inline-flex items-center gap-1.5 text-xs font-medium text-green-400">
                          <CheckIcon />
                          Solved
                        </span>
                      ) : p ? (
                        <span className="text-xs text-yellow-500">Best: {p.best_score}%</span>
                      ) : (
                        <span className="text-xs text-gray-600 group-hover:text-gray-500">
                          Solve →
                        </span>
                      )}
                      {p && (
                        <span className="font-mono text-xs text-gray-600">
                          {p.attempts} {p.attempts === 1 ? "attempt" : "attempts"}
                        </span>
                      )}
                    </div>

                    {p && !solved && (
                      <div className="mt-3 h-[3px] overflow-hidden rounded-full bg-gray-800">
                        <div
                          className="h-full rounded-full bg-yellow-500 transition-all duration-500"
                          style={{ width: `${p.best_score}%` }}
                        />
                      </div>
                    )}
                  </Link>
                );
              })}
            </div>
          </section>
        );
      })}

      {exercises.length === 0 && (
        <p className="text-center text-gray-500">No exercises yet.</p>
      )}

      {exercises.length > 0 && visible.length === 0 && (
        <div className="flex flex-col items-center gap-4 rounded-2xl border border-dashed border-gray-700 bg-gray-950 px-8 py-12 text-center">
          <span className="text-gray-700">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.25"
              strokeLinecap="round"
              className="h-10 w-10"
              aria-hidden="true"
            >
              <circle cx="11" cy="11" r="7" />
              <path d="M20 20l-3.5-3.5" />
              <path d="M8.5 11h5" />
            </svg>
          </span>
          <div>
            <h3 className="mb-1.5 text-[17px] font-semibold text-gray-200">
              Nothing matches that yet
            </h3>
            <p className="mx-auto max-w-xs text-sm leading-6 text-gray-500">
              No exercises match your current filters. Try another difficulty, or clear them.
            </p>
          </div>
          {filtersActive && (
            <button
              type="button"
              onClick={clearFilters}
              className="rounded-xl border border-gray-700 px-4 py-2 text-sm font-medium text-gray-300 transition hover:border-brand-500/60 hover:text-white"
            >
              Clear filters
            </button>
          )}
        </div>
      )}
    </div>
  );
}
