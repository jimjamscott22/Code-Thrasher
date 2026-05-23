import { useEffect } from "react";
import { Link } from "react-router-dom";
import api from "@/api/client";
import { useProgressStore } from "@/store/useProgressStore";
import type { ExerciseListItem, DifficultyLevel } from "@/types";
import { useState } from "react";

const DIFFICULTY_COLORS: Record<DifficultyLevel, string> = {
  beginner: "text-green-400 bg-green-400/10 ring-green-400/20",
  intermediate: "text-yellow-400 bg-yellow-400/10 ring-yellow-400/20",
  advanced: "text-red-400 bg-red-400/10 ring-red-400/20",
};

export default function Dashboard() {
  const [exercises, setExercises] = useState<ExerciseListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { totalExercises, completedCount, exercises: progress, fetch: fetchProgress } = useProgressStore();

  useEffect(() => {
    api
      .get<ExerciseListItem[]>("/exercises/")
      .then((r) => setExercises(r.data))
      .catch(() => setError("Failed to load exercises."))
      .finally(() => setLoading(false));

    fetchProgress().catch(() => {/* progress is non-critical */});
  }, [fetchProgress]);

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

  const grouped = exercises.reduce<Record<string, ExerciseListItem[]>>(
    (acc, ex) => {
      const cat = ex.category?.name ?? "Uncategorized";
      (acc[cat] ??= []).push(ex);
      return acc;
    },
    {},
  );

  const pct = totalExercises > 0 ? Math.round((completedCount / totalExercises) * 100) : 0;

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <div className="mb-8 flex items-end justify-between">
        <div>
          <h1 className="mb-1 text-3xl font-bold">Exercises</h1>
          <p className="text-gray-400">Pick a challenge and start thrashing.</p>
        </div>

        {totalExercises > 0 && (
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

      {Object.entries(grouped).map(([category, items]) => (
        <section key={category} className="mb-10">
          <h2 className="mb-4 font-mono text-sm font-semibold uppercase tracking-widest text-gray-500">
            {category}
          </h2>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((ex) => {
              const p = progress[ex.id];
              return (
                <Link
                  key={ex.id}
                  to={`/exercise/${ex.id}`}
                  className="group rounded-xl border border-gray-800 bg-gray-900 p-5 transition hover:border-brand-500/50 hover:bg-gray-800"
                >
                  <div className="mb-3 flex items-start justify-between gap-2">
                    <h3 className="font-medium leading-snug text-gray-100 group-hover:text-white">
                      {ex.title}
                    </h3>
                    <span
                      className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${DIFFICULTY_COLORS[ex.difficulty_level]}`}
                    >
                      {ex.difficulty_level}
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    {p?.solved ? (
                      <span className="text-xs font-medium text-green-400">✓ Solved</span>
                    ) : p ? (
                      <span className="text-xs text-yellow-500">Best: {p.best_score}%</span>
                    ) : (
                      <span className="text-xs text-gray-600 group-hover:text-gray-500">
                        Solve →
                      </span>
                    )}
                    {p && !p.solved && (
                      <span className="text-xs text-gray-600">
                        {p.attempts} {p.attempts === 1 ? "attempt" : "attempts"}
                      </span>
                    )}
                  </div>
                </Link>
              );
            })}
          </div>
        </section>
      ))}

      {exercises.length === 0 && (
        <p className="text-center text-gray-500">No exercises yet.</p>
      )}
    </div>
  );
}
