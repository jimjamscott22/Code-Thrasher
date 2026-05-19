import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import api from "@/api/client";
import { useAuthStore } from "@/store/useAuthStore";
import type { User } from "@/types";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.post<User>("/auth/register", { username, email, password });
      // auto-login after register
      const form = new URLSearchParams({ username, password });
      const tokenRes = await api.post<{ access_token: string }>(
        "/auth/login",
        form,
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } },
      );
      const meRes = await api.get<User>("/auth/me", {
        headers: { Authorization: `Bearer ${tokenRes.data.access_token}` },
      });
      setAuth(tokenRes.data.access_token, meRes.data);
      navigate("/");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail ?? "Registration failed.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-8rem)] items-center justify-center px-4">
      <div className="w-full max-w-sm rounded-2xl border border-gray-800 bg-gray-900 p-8">
        <h1 className="mb-6 text-center text-2xl font-bold">Create account</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm text-gray-400">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              minLength={3}
              maxLength={50}
              className="w-full rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm outline-none focus:border-brand-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm text-gray-400">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm outline-none focus:border-brand-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm text-gray-400">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              className="w-full rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm outline-none focus:border-brand-500"
            />
          </div>
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-brand-500 py-2 font-semibold text-white transition hover:bg-brand-600 disabled:opacity-60"
          >
            {loading ? "Creating account…" : "Sign up"}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-500">
          Already have an account?{" "}
          <Link to="/login" className="text-brand-500 hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
