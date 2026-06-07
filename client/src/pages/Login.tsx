import { FormEvent, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";

function getErrorMessage(error: unknown): string {
  return (
    (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
    "Login failed. Check your credentials and try again."
  );
}

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const login = useAuthStore((state) => state.login);
  const user = useAuthStore((state) => state.user);
  const [usernameOrEmail, setUsernameOrEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const from = (location.state as { from?: string } | null)?.from ?? "/";

  useEffect(() => {
    if (user) navigate(from, { replace: true });
  }, [from, navigate, user]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login({ username_or_email: usernameOrEmail, password });
      navigate(from, { replace: true });
    } catch (e: unknown) {
      setError(getErrorMessage(e));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-5xl items-center justify-center px-4 py-12">
      <div className="w-full max-w-md overflow-hidden rounded-2xl border border-brand-500/20 bg-gray-950">
        <div className="border-b border-gray-800 bg-gray-900 p-6">
          <p className="font-mono text-xs font-semibold uppercase tracking-[0.28em] text-brand-500">
            Session
          </p>
          <h1 className="mt-3 text-2xl font-black tracking-tight text-white">
            Log in to save progress
          </h1>
          <p className="mt-2 text-sm leading-6 text-gray-400">
            Your submissions, scores, and solved badges will be tied to this account.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 p-6">
          <label className="block">
            <span className="text-sm font-medium text-gray-300">Username or email</span>
            <input
              value={usernameOrEmail}
              onChange={(event) => setUsernameOrEmail(event.target.value)}
              required
              className="mt-2 w-full rounded-xl border border-gray-700 bg-gray-900 px-3 py-2 text-gray-100 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
              autoComplete="username"
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-gray-300">Password</span>
            <input
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              className="mt-2 w-full rounded-xl border border-gray-700 bg-gray-900 px-3 py-2 text-gray-100 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
              autoComplete="current-password"
            />
          </label>

          {error && (
            <div className="rounded-xl border border-red-800 bg-red-900/20 p-3 text-sm text-red-300">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-xl bg-brand-500 px-4 py-3 font-semibold text-white transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:bg-gray-700 disabled:text-gray-400"
          >
            {submitting ? "Logging in..." : "Log in"}
          </button>

          <p className="text-center text-sm text-gray-500">
            New here?{" "}
            <Link to="/register" state={{ from }} className="font-medium text-brand-500 hover:text-brand-400">
              Create an account
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
