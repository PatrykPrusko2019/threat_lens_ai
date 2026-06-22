import { Activity, AlertTriangle, Brain, Radar } from "lucide-react";

import { StatCard } from "../components/ui/StatCard";

const stats = [
  {
    label: "Total Alerts",
    value: "128",
    description: "Detected security alerts",
    icon: AlertTriangle,
  },
  {
    label: "Open Alerts",
    value: "37",
    description: "Waiting for review",
    icon: Activity,
  },
  {
    label: "Critical Events",
    value: "12",
    description: "High-risk security events",
    icon: Radar,
  },
  {
    label: "AI Checks",
    value: "284",
    description: "ML and anomaly checks",
    icon: Brain,
  },
];

const alerts = [
  {
    title: "Possible intrusion attempt",
    severity: "critical",
    sourceIp: "192.168.1.45",
    status: "open",
  },
  {
    title: "Suspicious transaction pattern",
    severity: "high",
    sourceIp: "10.0.0.23",
    status: "open",
  },
  {
    title: "Autoencoder anomaly detected",
    severity: "medium",
    sourceIp: "172.16.0.11",
    status: "closed",
  },
];

export function DashboardPage() {
  return (
    <div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((item) => (
          <StatCard key={item.label} {...item} />
        ))}
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 xl:col-span-2">
          <div className="mb-5">
            <h3 className="text-lg font-semibold">Latest Alerts</h3>
            <p className="text-sm text-slate-400">
              Recent AI and rule-based detections
            </p>
          </div>

          <div className="overflow-hidden rounded-xl border border-slate-800">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-950 text-slate-400">
                <tr>
                  <th className="px-4 py-3">Alert</th>
                  <th className="px-4 py-3">Severity</th>
                  <th className="px-4 py-3">Source IP</th>
                  <th className="px-4 py-3">Status</th>
                </tr>
              </thead>

              <tbody>
                {alerts.map((alert) => (
                  <tr key={alert.title} className="border-t border-slate-800">
                    <td className="px-4 py-3 text-slate-200">{alert.title}</td>
                    <td className="px-4 py-3">
                      <span className="rounded-full bg-red-500/10 px-3 py-1 text-xs font-medium text-red-300">
                        {alert.severity}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-slate-400">
                      {alert.sourceIp}
                    </td>
                    <td className="px-4 py-3">
                      <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">
                        {alert.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <h3 className="text-lg font-semibold">AI Security Modules</h3>
          <p className="mt-1 text-sm text-slate-400">
            Active detection components
          </p>

          <div className="mt-5 space-y-4">
            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p className="font-medium text-cyan-300">Intrusion Detection</p>
              <p className="mt-1 text-sm text-slate-400">
                RandomForest + rule-based analysis
              </p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p className="font-medium text-cyan-300">
                Autoencoder Anomaly Detection
              </p>
              <p className="mt-1 text-sm text-slate-400">
                Deep learning anomaly scoring
              </p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p className="font-medium text-cyan-300">AI Assistant</p>
              <p className="mt-1 text-sm text-slate-400">
                Future LLM-based security agent
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}