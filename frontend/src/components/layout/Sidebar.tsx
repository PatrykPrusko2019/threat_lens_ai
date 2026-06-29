import { 
  Activity, 
  AlertTriangle, 
  LayoutDashboard, 
  ShieldCheck,
  BrainCircuit, 
} from "lucide-react";

import { NavLink } from "react-router-dom";

const navigation = [
    { label: "Dashboard", path: "/", icon: LayoutDashboard },
    { label: "Alerts", path: "/alerts", icon: AlertTriangle },
    { label: "Security Events", path: "/events", icon: Activity },
    { label: "AI Detection", path: "/ai-detection", icon: BrainCircuit },
];

export function Sidebar() {
  return (
    <aside className="hidden w-72 border-r border-slate-800 bg-slate-950/95 p-6 lg:block">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-cyan-500/10 p-2 text-cyan-400">
          <ShieldCheck size={28} />
        </div>

        <div>
          <h1 className="text-lg font-semibold">ThreatLens AI</h1>
          <p className="text-sm text-slate-400">Security AI Platform</p>
        </div>
      </div>

      <nav className="mt-10 space-y-2">
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-lg px-4 py-3 text-sm transition",
                  isActive
                    ? "bg-cyan-500/10 text-cyan-300"
                    : "text-slate-400 hover:bg-slate-900 hover:text-slate-100",
                ].join(" ")
              }
            >
              <Icon size={18} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}