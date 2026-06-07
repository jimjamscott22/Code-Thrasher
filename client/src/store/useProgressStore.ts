import { create } from "zustand";
import api from "@/api/client";

export interface ExerciseProgress {
  best_score: number;
  attempts: number;
  solved: boolean;
}

interface ProgressState {
  totalExercises: number;
  completedCount: number;
  exercises: Record<number, ExerciseProgress>;
  loaded: boolean;
  fetch: () => Promise<void>;
  reset: () => void;
}

export const useProgressStore = create<ProgressState>((set) => ({
  totalExercises: 0,
  completedCount: 0,
  exercises: {},
  loaded: false,
  fetch: async () => {
    const r = await api.get<{
      total_exercises: number;
      completed_count: number;
      exercises: Record<number, ExerciseProgress>;
    }>("/progress/");
    set({
      totalExercises: r.data.total_exercises,
      completedCount: r.data.completed_count,
      exercises: r.data.exercises,
      loaded: true,
    });
  },
  reset: () =>
    set({
      totalExercises: 0,
      completedCount: 0,
      exercises: {},
      loaded: false,
    }),
}));
