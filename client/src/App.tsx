import { useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import Dashboard from "@/pages/Dashboard";
import ExerciseDetail from "@/pages/ExerciseDetail";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Resources from "@/pages/Resources";
import ResourceDetail from "@/pages/ResourceDetail";
import { useAuthStore } from "@/store/useAuthStore";

export default function App() {
  const hydrate = useAuthStore((state) => state.hydrate);

  useEffect(() => {
    hydrate().catch(() => {});
  }, [hydrate]);

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/exercise/:id" element={<ExerciseDetail />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/resources/:slug" element={<ResourceDetail />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
