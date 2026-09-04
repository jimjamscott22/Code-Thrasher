import { create } from "zustand";
import api from "@/api/client";
import type { LoginRequest, RegisterRequest, TokenResponse, User } from "@/types";
import { clearStoredAuth, getStoredAuth, setStoredAuth } from "@/store/authStorage";
import { useProgressStore } from "@/store/useProgressStore";

interface AuthState {
  user: User | null;
  token: string | null;
  initialized: boolean;
  login: (payload: LoginRequest) => Promise<void>;
  register: (payload: RegisterRequest) => Promise<void>;
  logout: () => void;
  hydrate: () => Promise<void>;
  refreshUser: () => Promise<User | null>;
}

function clearSession(set: (state: Partial<AuthState>) => void) {
  clearStoredAuth();
  useProgressStore.getState().reset();
  set({ user: null, token: null, initialized: true });
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  initialized: false,
  login: async (payload) => {
    const response = await api.post<TokenResponse>("/auth/login", payload);
    setStoredAuth(response.data.access_token, response.data.user);
    set({
      user: response.data.user,
      token: response.data.access_token,
      initialized: true,
    });
  },
  register: async (payload) => {
    const response = await api.post<TokenResponse>("/auth/register", payload);
    setStoredAuth(response.data.access_token, response.data.user);
    set({
      user: response.data.user,
      token: response.data.access_token,
      initialized: true,
    });
  },
  logout: () => clearSession(set),
  // Re-reads the user so server-updated stats (total_score, streak) are current.
  // Returns the fresh user so callers can diff it against a pre-action snapshot.
  refreshUser: async () => {
    const stored = getStoredAuth();
    if (!stored) return null;
    const response = await api.get<User>("/auth/me");
    setStoredAuth(stored.token, response.data);
    set({ user: response.data });
    return response.data;
  },
  hydrate: async () => {
    const stored = getStoredAuth();
    if (!stored) {
      set({ user: null, token: null, initialized: true });
      return;
    }

    set({ user: stored.user, token: stored.token, initialized: true });
    try {
      const response = await api.get<User>("/auth/me");
      setStoredAuth(stored.token, response.data);
      set({ user: response.data, token: stored.token, initialized: true });
    } catch {
      clearSession(set);
    }
  },
}));

if (typeof window !== "undefined") {
  window.addEventListener("code-thrasher:auth-expired", () => {
    useAuthStore.getState().logout();
  });
}
