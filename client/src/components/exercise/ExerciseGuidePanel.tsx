import { useEffect, useMemo, useState } from "react";
import api from "@/api/client";
import type { ExerciseGuideBlock, ExerciseSolution } from "@/types";

type ExerciseGuidePanelProps = {
  exerciseId: number;
  guide: ExerciseGuideBlock[];
  fallbackHint: string | null;
  hasSolution: boolean;
};

const KIND_LABELS: Record<string, string> = {
  nudge: "Nudge",
  pattern: "Pattern",
  checklist: "Check",
  snippet: "Snippet",
};

function getKindClasses(kind: string) {
  switch (kind) {
    case "pattern":
      return "border-cyan-400/30 bg-cyan-400/10 text-cyan-200";
    case "checklist":
      return "border-yellow-400/30 bg-yellow-400/10 text-yellow-200";
    case "snippet":
      return "border-violet-400/30 bg-violet-400/10 text-violet-200";
    default:
      return "border-brand-500/30 bg-brand-500/10 text-green-200";
  }
}

export default function ExerciseGuidePanel({
  exerciseId,
  guide,
  fallbackHint,
  hasSolution,
}: ExerciseGuidePanelProps) {
  const guideBlocks = useMemo<ExerciseGuideBlock[]>(() => {
    if (guide.length > 0) return guide;
    if (!fallbackHint) return [];

    return [
      {
        kind: "nudge",
        title: "First foothold",
        body: fallbackHint,
      },
    ];
  }, [fallbackHint, guide]);

  const [revealedBlocks, setRevealedBlocks] = useState<Set<number>>(() => new Set());
  const [solution, setSolution] = useState<ExerciseSolution | null>(null);
  const [solutionLoading, setSolutionLoading] = useState(false);
  const [solutionError, setSolutionError] = useState<string | null>(null);
  const [confirmReveal, setConfirmReveal] = useState(false);

  useEffect(() => {
    setRevealedBlocks(new Set());
    setSolution(null);
    setSolutionLoading(false);
    setSolutionError(null);
    setConfirmReveal(false);
  }, [exerciseId]);

  function toggleBlock(index: number) {
    setRevealedBlocks((current) => {
      const next = new Set(current);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  }

  async function revealSolution() {
    if (!confirmReveal) {
      setConfirmReveal(true);
      return;
    }

    setSolutionLoading(true);
    setSolutionError(null);
    try {
      const response = await api.get<ExerciseSolution>(`/exercises/${exerciseId}/solution`);
      setSolution(response.data);
    } catch (error: unknown) {
      const status = (error as { response?: { status?: number } })?.response?.status;
      if (status === 401) {
        setSolutionError("Log in to reveal the reference solution.");
      } else {
        setSolutionError("The reference solution is not available for this challenge yet.");
      }
    } finally {
      setSolutionLoading(false);
    }
  }

  return (
    <aside className="overflow-hidden rounded-[1.75rem] border border-brand-500/20 bg-gray-950 shadow-[0_0_48px_rgba(34,197,94,0.10)] xl:sticky xl:top-6">
      <div className="relative border-b border-gray-800 bg-[radial-gradient(circle_at_top_right,rgba(34,197,94,0.20),transparent_32%),linear-gradient(135deg,rgba(17,24,39,1),rgba(3,7,18,1))] p-5">
        <div className="absolute right-4 top-4 h-16 w-16 rounded-full border border-brand-500/20" />
        <p className="font-mono text-[0.65rem] font-semibold uppercase tracking-[0.36em] text-brand-500">
          Field guide
        </p>
        <h2 className="mt-3 max-w-56 text-2xl font-black leading-none tracking-tight text-white">
          Stuck is a place to start.
        </h2>
        <p className="mt-3 text-sm leading-6 text-gray-400">
          Unlock small nudges first. Save the full answer for when you want to compare approaches.
        </p>
      </div>

      <div className="space-y-3 p-4">
        {guideBlocks.length === 0 && (
          <div className="rounded-2xl border border-gray-800 bg-gray-900/70 p-4 text-sm text-gray-400">
            No guide notes yet for this challenge. Try running your code and use the test output as your next clue.
          </div>
        )}

        {guideBlocks.map((block, index) => {
          const isRevealed = revealedBlocks.has(index);

          return (
            <section
              key={`${block.kind}-${block.title}`}
              className="group rounded-2xl border border-gray-800 bg-gray-900/80 transition hover:border-gray-700"
            >
              <button
                type="button"
                aria-expanded={isRevealed}
                onClick={() => toggleBlock(index)}
                className="flex w-full items-start gap-3 p-4 text-left"
              >
                <span className="mt-0.5 font-mono text-xs text-gray-600">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <span className="min-w-0 flex-1">
                  <span
                    className={`inline-flex rounded-full border px-2 py-0.5 font-mono text-[0.62rem] uppercase tracking-[0.22em] ${getKindClasses(block.kind)}`}
                  >
                    {KIND_LABELS[block.kind] ?? "Guide"}
                  </span>
                  <span className="mt-2 block text-sm font-semibold text-gray-100">
                    {block.title}
                  </span>
                </span>
                <span className="text-gray-500 transition group-hover:text-brand-500">
                  {isRevealed ? "Hide" : "Open"}
                </span>
              </button>

              {isRevealed && (
                <div className="border-t border-gray-800 px-4 pb-4 pt-3">
                  <p className="text-sm leading-6 text-gray-300">{block.body}</p>
                  {block.code && (
                    <pre className="mt-3 overflow-x-auto rounded-xl border border-gray-800 bg-black/50 p-3 font-mono text-xs leading-5 text-green-100">
                      <code>{block.code}</code>
                    </pre>
                  )}
                </div>
              )}
            </section>
          );
        })}

        <section className="rounded-2xl border border-yellow-500/20 bg-yellow-500/[0.06] p-4">
          <p className="font-mono text-[0.62rem] font-semibold uppercase tracking-[0.28em] text-yellow-300">
            Last resort
          </p>
          <h3 className="mt-2 text-sm font-semibold text-yellow-100">Reveal the full answer</h3>
          <p className="mt-2 text-sm leading-6 text-yellow-100/70">
            Use this when you are ready to study the reference solution. It will not replace your editor code.
          </p>

          {!solution && (
            <button
              type="button"
              disabled={!hasSolution || solutionLoading}
              onClick={revealSolution}
              className="mt-4 w-full rounded-xl border border-yellow-400/30 bg-yellow-300 px-3 py-2 text-sm font-bold text-gray-950 transition hover:bg-yellow-200 disabled:cursor-not-allowed disabled:border-gray-700 disabled:bg-gray-800 disabled:text-gray-500"
            >
              {solutionLoading
                ? "Loading solution..."
                : confirmReveal
                  ? "Yes, show the reference solution"
                  : hasSolution
                    ? "I am ready to compare approaches"
                    : "Solution unavailable"}
            </button>
          )}

          {solutionError && <p className="mt-3 text-sm text-red-300">{solutionError}</p>}

          {solution && (
            <div className="mt-4 space-y-3">
              {solution.explanation && (
                <p className="text-sm leading-6 text-yellow-100/80">{solution.explanation}</p>
              )}
              <pre className="overflow-x-auto rounded-xl border border-yellow-400/20 bg-black/60 p-3 font-mono text-xs leading-5 text-yellow-50">
                <code>{solution.code}</code>
              </pre>
            </div>
          )}
        </section>
      </div>
    </aside>
  );
}
