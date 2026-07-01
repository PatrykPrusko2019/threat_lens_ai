import axios from "axios";
import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";

import { register } from "../api/authApi";

function getRegisterErrorMessage(error: unknown) {
    if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail;

        if (typeof detail === "string") {
            return detail;
        }

        if (Array.isArray(detail)) {
            return detail
                .map((item) => item?.msg ?? "Invalid registration data.")
                .join(" ");
        }

        return "Registration failed. Check the form data.";
    }

    return "Registration failed. Try again.";
}

function isValidEmail(email: string) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function RegisterPage() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const normalizedEmail = email.trim();

        if (!normalizedEmail) {
            setError("Email is required.");
            return;
        }

        if (!isValidEmail(normalizedEmail)) {
            setError("Enter a valid email address.");
            return;
        }

        if (password.length < 8) {
            setError("Password must be at least 8 characters long.");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setError(null);
        setIsLoading(true);

        try {
            await register({ email: normalizedEmail, password });
            navigate("/login", {
                state: {
                    message: "Account created successfully. You can now sign in.",
                },
            });
        } catch (requestError) {
            setError(getRegisterErrorMessage(requestError));
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-slate-100">
            <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-2xl shadow-black/30">
                <div>
                    <p className="text-sm text-cyan-400">ThreatLens AI</p>
                    <h1 className="mt-2 text-2xl font-semibold">Create account</h1>
                    <p className="mt-2 text-sm text-slate-400">
                        Register a user account for the local security dashboard.
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
                            placeholder="analyst@example.com"
                        />
                    </div>

                    <div>
                        <label className="text-sm text-slate-300">Password</label>
                        <input
                            className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-500"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            type="password"
                            autoComplete="new-password"
                            placeholder="At least 8 characters"
                        />
                    </div>

                    <div>
                        <label className="text-sm text-slate-300">
                            Confirm password
                        </label>
                        <input
                            className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-500"
                            value={confirmPassword}
                            onChange={(event) =>
                                setConfirmPassword(event.target.value)
                            }
                            type="password"
                            autoComplete="new-password"
                            placeholder="Repeat password"
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
                        {isLoading ? "Creating account..." : "Create account"}
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-slate-400">
                    Already have an account?{" "}
                    <Link
                        className="font-medium text-cyan-300 hover:text-cyan-200"
                        to="/login"
                    >
                        Sign in
                    </Link>
                </p>
            </div>
        </div>
    );
}