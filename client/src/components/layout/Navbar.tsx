import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";

export default function Navbar() {
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  function handleLogout() {
    logout();
    navigate("/");
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
        <div className="flex items-center gap-6">
          <Link
            to="/resources"
            className="text-sm font-medium text-gray-400 transition hover:text-white"
          >
            Resources
          </Link>
        </div>
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="hidden text-sm text-gray-400 sm:inline">
                Signed in as <span className="font-medium text-gray-100">{user.username}</span>
              </span>
              <button
                type="button"
                onClick={handleLogout}
                className="rounded-lg border border-gray-700 px-3 py-1.5 text-sm font-medium text-gray-300 transition hover:border-brand-500/60 hover:text-white"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-sm font-medium text-gray-300 transition hover:text-white"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="rounded-lg bg-brand-500 px-3 py-1.5 text-sm font-semibold text-white transition hover:bg-brand-600"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
