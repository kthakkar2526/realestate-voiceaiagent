"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface UserData {
  id: number;
  phone: string;
  name: string | null;
  email: string | null;
}

interface AuthContextType {
  user: UserData | null;
  token: string | null;
  loading: boolean;
  profileComplete: boolean;
  sendOtp: (phone: string) => Promise<void>;
  verifyOtp: (phone: string, otp: string) => Promise<void>;
  updateProfile: (name: string, email: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserData | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const profileComplete = !!(user?.name && user?.email);

  useEffect(() => {
    const stored = localStorage.getItem("re_auth_token");
    if (stored) {
      setToken(stored);
      fetchMe(stored);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchMe = async (t: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/auth/me`, {
        headers: { Authorization: `Bearer ${t}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
        setToken(t);
      } else {
        localStorage.removeItem("re_auth_token");
        setToken(null);
      }
    } catch {
      localStorage.removeItem("re_auth_token");
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  const sendOtp = async (phone: string) => {
    const res = await fetch(`${API_BASE}/api/auth/send-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to send OTP");
    }
  };

  const verifyOtp = async (phone: string, otp: string) => {
    const res = await fetch(`${API_BASE}/api/auth/verify-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone, otp }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Invalid OTP");
    }
    const data = await res.json();
    localStorage.setItem("re_auth_token", data.token);
    setToken(data.token);
    setUser(data.user);
  };

  const updateProfile = async (name: string, email: string) => {
    if (!token) throw new Error("Not authenticated");
    const res = await fetch(`${API_BASE}/api/auth/profile`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name, email }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to update profile");
    }
    const data = await res.json();
    setUser(data);
  };

  const logout = () => {
    localStorage.removeItem("re_auth_token");
    localStorage.removeItem("re_session_id");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, profileComplete, sendOtp, verifyOtp, updateProfile, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
