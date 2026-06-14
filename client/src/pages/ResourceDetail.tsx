import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "@/api/client";
import type { DifficultyLevel, ResourceDetail as ResourceDetailType } from "@/types";

const DIFFICULTY_COLORS: Record<DifficultyLevel, string> = {
  beginner: "text-green-400 bg-green-400/10 ring-green-400/20",
  intermediate: "text-yellow-400 bg-yellow-400/10 ring-yellow-400/20",
  advanced: "text-red-400 bg-red-400/10 ring-red-400/20",
};

export default function ResourceDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [resource, setResource] = useState<ResourceDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    api
      .get<ResourceDetailType>(`/resources/${slug}`)
      .then((r) => setResource(r.data))
      .catch((err) => {
        if (err?.response?.status === 404) {
          setError("Resource not found.");
        } else {
          setError("Failed to load resource.");
        }
      })
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
      </div>
    );
  }

  if (error || !resource) {
    return (
      <div className="mx-auto mt-12 max-w-md rounded-lg border border-red-800 bg-red-900/20 p-6 text-center text-red-400">
        {error ?? "Resource not found."}
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <div className="mb-2">
        <Link
          to="/resources"
          className="text-sm text-gray-500 transition hover:text-gray-300"
        >
          ← All Resources
        </Link>
      </div>

      <div className="mb-8">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-gray-800 px-2.5 py-0.5 text-xs font-medium text-gray-400">
            {resource.topic_area}
          </span>
          <span
            className={`rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${DIFFICULTY_COLORS[resource.difficulty_level]}`}
          >
            {resource.difficulty_level}
          </span>
        </div>
        <h1 className="mb-2 text-3xl font-bold">{resource.title}</h1>
        <p className="text-base leading-relaxed text-gray-400">{resource.summary}</p>
      </div>

      <div className="space-y-6">
        {resource.sections.map((section, i) => (
          <div
            key={i}
            className="rounded-xl border border-gray-800 bg-gray-900 overflow-hidden"
          >
            <div className="border-b border-gray-800 bg-gray-900 px-5 py-4">
              <h2 className="font-semibold text-gray-100">{section.heading}</h2>
            </div>
            <div className="px-5 py-4">
              <p className="whitespace-pre-line text-sm leading-7 text-gray-300">{section.body}</p>

              {section.code && (
                <div className="mt-4">
                  <p className="mb-1.5 font-mono text-xs font-semibold uppercase tracking-widest text-gray-600">
                    Example
                  </p>
                  <pre className="overflow-x-auto rounded-lg bg-gray-950 p-4 font-mono text-sm leading-relaxed text-gray-200">
                    <code>{section.code}</code>
                  </pre>
                </div>
              )}

              {section.output && (
                <div className="mt-3">
                  <p className="mb-1.5 font-mono text-xs font-semibold uppercase tracking-widest text-gray-600">
                    Output
                  </p>
                  <pre className="overflow-x-auto rounded-lg border border-brand-500/20 bg-brand-500/5 p-4 font-mono text-sm leading-relaxed text-green-300">
                    <code>{section.output}</code>
                  </pre>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-10 flex items-center justify-between border-t border-gray-800 pt-6">
        <Link
          to="/resources"
          className="text-sm text-gray-500 transition hover:text-gray-300"
        >
          ← Back to Resources
        </Link>
        <Link
          to="/"
          className="rounded-lg bg-brand-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-600"
        >
          Try an Exercise →
        </Link>
      </div>
    </div>
  );
}
