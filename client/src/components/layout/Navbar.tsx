import { Link, NavLink, useNavigate } from "react-router-dom";
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
    <nav className="border-b border-gray-800 bg-gray-900/95 px-4 py-3 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <Link
          to="/"
          className="font-mono text-xl font-bold tracking-tight text-brand-500 transition hover:text-brand-600"
        >
          {"<CodeThrasher />"}
        </Link>
        <div className="flex items-center gap-1">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `rounded-lg px-3 py-1.5 text-sm font-medium transition ${
                isActive
                  ? "bg-gray-800 text-white"
                  : "text-gray-400 hover:bg-gray-800/60 hover:text-white"
              }`
            }
          >
            Exercises
          </NavLink>
          <NavLink
            to="/resources"
            className={({ isActive }) =>
              `rounded-lg px-3 py-1.5 text-sm font-medium transition ${
                isActive
                  ? "bg-gray-800 text-white"
                  : "text-gray-400 hover:bg-gray-800/60 hover:text-white"
              }`
            }
          >
            Resources
          </NavLink>
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
                className="cursor-pointer rounded-lg border border-gray-700 px-3 py-1.5 text-sm font-medium text-gray-300 transition-colors duration-200 hover:border-brand-500/60 hover:text-white focus:outline-none focus:ring-2 focus:ring-brand-500/40"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="rounded-lg px-3 py-1.5 text-sm font-medium text-gray-300 transition hover:text-white focus:outline-none focus:ring-2 focus:ring-brand-500/40"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="rounded-lg bg-brand-500 px-3 py-1.5 text-sm font-semibold text-white transition-colors duration-200 hover:bg-brand-600 focus:outline-none focus:ring-2 focus:ring-brand-500/50"
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
