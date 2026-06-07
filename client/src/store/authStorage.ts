import type { User } from "@/types";

const AUTH_STORAGE_KEY = "code-thrasher-auth";

type StoredAuth = {
  token: string;
  user: User;
};

function parseStoredAuth(raw: string | null): StoredAuth | null {
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as Partial<StoredAuth>;
    if (typeof parsed.token === "string" && parsed.user) {
      return parsed as StoredAuth;
    }
  } catch {
    return null;
  }
  return null;
}

export function getStoredAuth(): StoredAuth | null {
  if (typeof window === "undefined") return null;
  return parseStoredAuth(window.localStorage.getItem(AUTH_STORAGE_KEY));
}

export function getAuthToken(): string | null {
  return getStoredAuth()?.token ?? null;
}

export function setStoredAuth(token: string, user: User) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify({ token, user }));
}

export function clearStoredAuth() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(AUTH_STORAGE_KEY);
}
