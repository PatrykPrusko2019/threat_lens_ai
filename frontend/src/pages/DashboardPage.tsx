import { useQuery } from "@tanstack/react-query";
import { Activity, AlertTriangle, Brain, Radar } from "lucide-react";

import { getDashboardSummary } from "../api/dashboardApi";
import { StatCard } from "../components/ui/StatCard";

function getSeverityClass(severity: string) {
  if (severity === "critical") {
    return "bg-red-500/10 text-red-300";
  }

  if (severity === "high") {
    return "bg-orange-500/10 text-orange-300";
  }

  if (severity === "medium") {
    return "bg-yellow-500/10 text-yellow-300";
  }

  return "bg-slate-700 text-slate-300";
}

function getStatusClass(status: string) {
  if (status === "open") {
    return "bg-cyan-500/10 text-cyan-300";
  }

  if (status === "closed") {
    return "bg-emerald-500/10 text-emerald-300";
  }

  return "bg-slate-800 text-slate-300";
}

export function DashboardPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: getDashboardSummary,
  });

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
        <p className="text-slate-400">Loading dashboard data...</p>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-6">
        <h3 className="text-lg font-semibold text-red-300">
          Dashboard data unavailable
        </h3>
        <p className="mt-2 text-sm text-red-200/80">
          Check if the backend is running and if you are logged in with a valid
          admin token.
        </p>
      </div>
    );
  }

  const stats = [
    {
      label: "Total Alerts",
      value: String(data.total_alerts),
      description: "Detected security alerts",
      icon: AlertTriangle,
    },
    {
      label: "Open Alerts",
      value: String(data.open_alerts),
      description: "Waiting for review",
      icon: Activity,
    },
    {
      label: "Critical Alerts",
      value: String(data.critical_alerts),
      description: "Highest-risk active threats",
      icon: Radar,
    },
    {
      label: "Total Events",
      value: String(data.total_events),
      description: "Registered security events",
      icon: Brain,
    },
  ];

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
              Recent AI and rule-based detections from the backend API
            </p>
          </div>

          <div className="overflow-hidden rounded-xl border border-slate-800">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-950 text-slate-400">
                <tr>
                  <th className="px-4 py-3">Alert</th>
                  <th className="px-4 py-3">Severity</th>
                  <th className="px-4 py-3">Risk</th>
                  <th className="px-4 py-3">Status</th>
                </tr>
              </thead>

              <tbody>
                {data.latest_alerts.length === 0 ? (
                  <tr className="border-t border-slate-800">
                    <td className="px-4 py-6 text-slate-500" colSpan={4}>
                      No alerts available yet.
                    </td>
                  </tr>
                ) : (
                  data.latest_alerts.map((alert) => (
                    <tr key={alert.id} className="border-t border-slate-800">
                      <td className="px-4 py-3 text-slate-200">
                        <div>
                          <p className="font-medium">{alert.title}</p>
                          <p className="mt-1 line-clamp-1 text-xs text-slate-500">
                            {alert.description ?? "No description"}
                          </p>
                        </div>
                      </td>

                      <td className="px-4 py-3">
                        <span
                          className={[
                            "rounded-full px-3 py-1 text-xs font-medium",
                            getSeverityClass(alert.severity),
                          ].join(" ")}
                        >
                          {alert.severity}
                        </span>
                      </td>

                      <td className="px-4 py-3 text-slate-300">
                        {alert.risk_score}
                      </td>

                      <td className="px-4 py-3">
                        <span
                          className={[
                            "rounded-full px-3 py-1 text-xs font-medium",
                            getStatusClass(alert.status),
                          ].join(" ")}
                        >
                          {alert.status}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
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