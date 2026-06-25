import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { login } from "../api/authApi";
import { saveAccessToken } from "../app/auth";

export function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError(null);
    setIsLoading(true);

    try {
      const response = await login({ email, password });
      saveAccessToken(response.access_token);
      navigate("/");
    } catch {
      setError("Invalid email or password.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-slate-100">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-2xl shadow-black/30">
        <div>
          <p className="text-sm text-cyan-400">ThreatLens AI</p>
          <h1 className="mt-2 text-2xl font-semibold">Security Dashboard Login</h1>
          <p className="mt-2 text-sm text-slate-400">
            Sign in to access the SOC/SIEM monitoring panel.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          <div>
            <label className="text-sm text-slate-300">Email</label>
            <input
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-500"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              type="email"
              autoComplete="email"
            />
          </div>

          <div>
            <label className="text-sm text-slate-300">Password</label>
            <input
              className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-500"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              type="password"
              autoComplete="current-password"
            />
          </div>

          {error && (
            <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}

          <button
            disabled={isLoading}
            className="w-full rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
            type="submit"
          >
            {isLoading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p className="mt-6 text-xs text-slate-500">
          This frontend uses JWT authentication from the FastAPI backend.
        </p>
      </div>
    </div>
  );
}