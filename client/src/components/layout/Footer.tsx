export default function Footer() {
  return (
    <footer className="border-t border-gray-800 bg-gray-900 py-5 text-center text-xs text-gray-600">
      <p className="mx-auto max-w-7xl px-4">
        Code Thrasher &copy; {new Date().getFullYear()} — Keep thrashing.
      </p>
    </footer>
  );
}
