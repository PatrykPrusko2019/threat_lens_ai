import { Lock, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { removeAccessToken } from "../../app/auth";

export function Topbar() {
  const navigate = useNavigate();

  function handleLogout() {
    removeAccessToken();
    navigate("/login");
  }

  return (
    <header className="border-b border-slate-800 bg-slate-950/70 px-6 py-5">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm text-cyan-400">SOC / SIEM Dashboard</p>
          <h2 className="text-2xl font-semibold tracking-tight">
            AI-powered threat monitoring
          </h2>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex w-fit items-center gap-2 rounded-full border border-slate-800 px-4 py-2 text-sm text-slate-300">
            <Lock size={16} />
            Admin protected
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 rounded-full border border-slate-800 px-4 py-2 text-sm text-slate-300 transition hover:border-red-500/50 hover:text-red-300"
            type="button"
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}