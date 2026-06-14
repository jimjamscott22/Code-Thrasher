import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "@/api/client";
import type { DifficultyLevel, ResourceListItem } from "@/types";

const DIFFICULTY_COLORS: Record<DifficultyLevel, string> = {
  beginner: "text-green-400 bg-green-400/10 ring-green-400/20",
  intermediate: "text-yellow-400 bg-yellow-400/10 ring-yellow-400/20",
  advanced: "text-red-400 bg-red-400/10 ring-red-400/20",
};

export default function Resources() {
  const [resources, setResources] = useState<ResourceListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<ResourceListItem[]>("/resources/")
      .then((r) => setResources(r.data))
      .catch(() => setError("Failed to load resources."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto mt-12 max-w-md rounded-lg border border-red-800 bg-red-900/20 p-6 text-center text-red-400">
        {error}
      </div>
    );
  }

  const grouped = resources.reduce<Record<DifficultyLevel, ResourceListItem[]>>(
    (acc, res) => {
      (acc[res.difficulty_level] ??= []).push(res);
      return acc;
    },
    {} as Record<DifficultyLevel, ResourceListItem[]>,
  );

  const sections: { label: string; key: DifficultyLevel }[] = [
    { label: "Beginner", key: "beginner" },
    { label: "Intermediate", key: "intermediate" },
    { label: "Advanced", key: "advanced" },
  ];

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <div className="mb-8">
        <h1 className="mb-1 text-3xl font-bold">Python Resources</h1>
        <p className="text-gray-400">
          Reference guides covering Python fundamentals and intermediate topics — read one before
          tackling a challenge.
        </p>
      </div>

      {sections.map(({ label, key }) => {
        const items = grouped[key];
        if (!items?.length) return null;
        return (
          <section key={key} className="mb-10">
            <h2 className="mb-4 font-mono text-sm font-semibold uppercase tracking-widest text-gray-500">
              {label}
            </h2>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {items.map((res) => (
                <Link
                  key={res.id}
                  to={`/resources/${res.slug}`}
                  className="group flex flex-col rounded-xl border border-gray-800 bg-gray-900 p-5 transition hover:border-brand-500/50 hover:bg-gray-800"
                >
                  <div className="mb-3 flex items-start justify-between gap-2">
                    <h3 className="font-medium leading-snug text-gray-100 group-hover:text-white">
                      {res.title}
                    </h3>
                    <span
                      className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${DIFFICULTY_COLORS[res.difficulty_level]}`}
                    >
                      {res.difficulty_level}
                    </span>
                  </div>
                  <p className="mb-3 flex-1 text-sm leading-relaxed text-gray-400 group-hover:text-gray-300">
                    {res.summary}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="rounded-full bg-gray-800 px-2 py-0.5 text-xs font-medium text-gray-400 group-hover:bg-gray-700 group-hover:text-gray-300">
                      {res.topic_area}
                    </span>
                    <span className="text-xs text-gray-600 transition group-hover:text-gray-400">
                      Read →
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        );
      })}

      {resources.length === 0 && (
        <p className="text-center text-gray-500">No resources yet.</p>
      )}
    </div>
  );
}
