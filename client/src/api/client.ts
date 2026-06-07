import axios from "axios";
import { clearStoredAuth, getAuthToken } from "@/store/authStorage";

const api = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers = config.headers ?? {};
    (config.headers as Record<string, string>).Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      clearStoredAuth();
      if (typeof window !== "undefined") {
        window.dispatchEvent(new Event("code-thrasher:auth-expired"));
      }
    }
    return Promise.reject(error);
  },
);

export default api;
