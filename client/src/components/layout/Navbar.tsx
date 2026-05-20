import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="border-b border-gray-800 bg-gray-900 px-4 py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <Link
          to="/"
          className="font-mono text-xl font-bold tracking-tight text-brand-500 hover:text-brand-600"
        >
          {"<CodeThrasher />"}
        </Link>
      </div>
    </nav>
  );
}
