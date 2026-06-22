import { Lock } from "lucide-react";

export function Topbar() {
  return (
    <header className="border-b border-slate-800 bg-slate-950/70 px-6 py-5">
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm text-cyan-400">SOC / SIEM Dashboard</p>
          <h2 className="text-2xl font-semibold tracking-tight">
            AI-powered threat monitoring
          </h2>
        </div>

        <div className="flex w-fit items-center gap-2 rounded-full border border-slate-800 px-4 py-2 text-sm text-slate-300">
          <Lock size={16} />
          Admin protected
        </div>
      </div>
    </header>
  );
}