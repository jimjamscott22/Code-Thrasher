import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav className="border-b border-gray-800 bg-gray-900 px-4 py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <Link
          to="/"
          className="font-mono text-xl font-bold tracking-tight text-brand-500 hover:text-brand-600"
        >
          {"<CodeThrasher />"}
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <span className="hidden text-sm text-gray-400 sm:inline">
                {user.username}
                <span className="ml-2 rounded-full bg-brand-500/20 px-2 py-0.5 text-xs font-medium text-brand-500">
                  {user.total_score} pts
                </span>
              </span>
              <button
                onClick={handleLogout}
                className="rounded-md border border-gray-700 px-3 py-1.5 text-sm text-gray-300 transition hover:border-gray-500 hover:text-white"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-sm text-gray-300 hover:text-white"
              >
                Log in
              </Link>
              <Link
                to="/register"
                className="rounded-md bg-brand-500 px-3 py-1.5 text-sm font-medium text-white transition hover:bg-brand-600"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
