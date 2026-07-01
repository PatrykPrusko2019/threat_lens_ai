import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, Brain, CheckCircle2 } from "lucide-react";
import { useState } from "react";

import { getCurrentUser } from "../api/usersApi";
import { closeAlert, explainAlert, getAlerts } from "../api/alertsApi";
import type { AlertExplanationResponse, AlertResponse } from "../types/alert";

function getSeverityClass(severity: string) {
  if (severity === "critical") {
    return "bg-red-500/10 text-red-300 border-red-500/20";
  }

  if (severity === "high") {
    return "bg-orange-500/10 text-orange-300 border-orange-500/20";
  }

  if (severity === "medium") {
    return "bg-yellow-500/10 text-yellow-300 border-yellow-500/20";
  }

  return "bg-slate-700/60 text-slate-300 border-slate-600";
}

function getStatusClass(status: string) {
  if (status === "open") {
    return "bg-cyan-500/10 text-cyan-300 border-cyan-500/20";
  }

  if (status === "closed") {
    return "bg-emerald-500/10 text-emerald-300 border-emerald-500/20";
  }

  return "bg-slate-700/60 text-slate-300 border-slate-600";
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

export function AlertsPage() {
  const queryClient = useQueryClient();
  const [selectedAlert, setSelectedAlert] = useState<AlertResponse | null>(null);
  const [explanation, setExplanation] =
    useState<AlertExplanationResponse | null>(null);

  const { data: currentUser } = useQuery({
  queryKey: ["current-user"],
  queryFn: getCurrentUser,
  });

  const {
    data: alerts = [],
    isLoading: isAlertsLoading,
    isError: isAlertsError,
  } = useQuery({
    queryKey: ["alerts"],
    queryFn: getAlerts,
  });

  const canManageAlerts = currentUser?.role === "admin";

  const explainMutation = useMutation({
    mutationFn: explainAlert,
    onSuccess: (data) => {
      setExplanation(data);
    },
  });

  const closeMutation = useMutation({
    mutationFn: closeAlert,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["alerts"] });
      await queryClient.invalidateQueries({ queryKey: ["dashboard-summary"] });
    },
  });

  function handleExplain(alert: AlertResponse) {
    setSelectedAlert(alert);
    setExplanation(null);
    explainMutation.mutate(alert.id);
  }

  function handleClose(alertId: number) {
    closeMutation.mutate(alertId);
  }

  if (isAlertsLoading) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
        <p className="text-slate-400">Loading alerts...</p>
      </div>
    );
  }

  if (isAlertsError) {
    return (
      <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-6">
        <h3 className="text-lg font-semibold text-red-300">
          Alerts unavailable
        </h3>
        <p className="mt-2 text-sm text-red-200/80">
          Check if the backend is running and if you are signed in.
        </p>
      </div>
    );
  }

  return (
    <div className="grid gap-6 xl:grid-cols-3">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 xl:col-span-2">
        <div className="mb-5 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <h3 className="text-lg font-semibold">Security Alerts</h3>
            <p className="text-sm text-slate-400">
              AI and rule-based alerts detected by ThreatLens AI
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-slate-800 px-4 py-2 text-sm text-slate-300">
            <AlertTriangle size={16} />
            {alerts.length} alerts
          </div>
        </div>

        {currentUser && !canManageAlerts && (
          <div className="mb-5 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-300">
            Viewer mode: you can inspect alerts and generate explanations, but only admins can close alerts.
          </div>
        )}

        <div className="overflow-hidden rounded-xl border border-slate-800">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-950 text-slate-400">
              <tr>
                <th className="px-4 py-3">Alert</th>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Risk</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Created</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>

            <tbody>
              {alerts.length === 0 ? (
                <tr className="border-t border-slate-800">
                  <td className="px-4 py-6 text-slate-500" colSpan={6}>
                    No alerts available yet.
                  </td>
                </tr>
              ) : (
                alerts.map((alert) => (
                  <tr key={alert.id} className="border-t border-slate-800">
                    <td className="px-4 py-3">
                      <p className="font-medium text-slate-200">
                        {alert.title}
                      </p>
                      <p className="mt-1 max-w-md truncate text-xs text-slate-500">
                        {alert.description ?? "No description"}
                      </p>
                    </td>

                    <td className="px-4 py-3">
                      <span
                        className={[
                          "rounded-full border px-3 py-1 text-xs font-medium",
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
                          "rounded-full border px-3 py-1 text-xs font-medium",
                          getStatusClass(alert.status),
                        ].join(" ")}
                      >
                        {alert.status}
                      </span>
                    </td>

                    <td className="px-4 py-3 text-xs text-slate-500">
                      {formatDate(alert.created_at)}
                    </td>

                    <td className="px-4 py-3">
                      <div className="flex flex-wrap gap-2">
                        <button
                          onClick={() => handleExplain(alert)}
                          className="inline-flex items-center gap-2 rounded-lg border border-cyan-500/30 px-3 py-2 text-xs font-medium text-cyan-300 transition hover:bg-cyan-500/10"
                          type="button"
                        >
                          <Brain size={14} />
                          Explain
                        </button>

                        {canManageAlerts && alert.status !== "closed" &&  (
                          <button
                            onClick={() => handleClose(alert.id)}
                            className="inline-flex items-center gap-2 rounded-lg border border-emerald-500/30 px-3 py-2 text-xs font-medium text-emerald-300 transition hover:bg-emerald-500/10"
                            type="button"
                          >
                            <CheckCircle2 size={14} />
                            Close
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <aside className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
        <h3 className="text-lg font-semibold">AI Alert Explanation</h3>
        <p className="mt-1 text-sm text-slate-400">
          Select an alert and generate a security explanation.
        </p>

        {!selectedAlert && (
          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-500">
            No alert selected.
          </div>
        )}

        {selectedAlert && (
          <div className="mt-6 space-y-4">
            <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p className="text-sm text-slate-400">Selected alert</p>
              <p className="mt-1 font-medium text-slate-200">
                {selectedAlert.title}
              </p>
            </div>

            {explainMutation.isPending && (
              <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-4 text-sm text-cyan-300">
                Generating explanation...
              </div>
            )}

            {explainMutation.isError && (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
                Could not generate explanation.
              </div>
            )}

            {explanation && (
              <div className="space-y-4">
                <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <p className="text-sm font-medium text-cyan-300">Summary</p>
                  <p className="mt-2 text-sm text-slate-300">
                    {explanation.summary}
                  </p>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <p className="text-sm font-medium text-cyan-300">
                    Severity explanation
                  </p>
                  <p className="mt-2 text-sm text-slate-300">
                    {explanation.severity_explanation}
                  </p>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <p className="text-sm font-medium text-cyan-300">
                    Possible causes
                  </p>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-300">
                    {explanation.possible_causes.map((cause) => (
                      <li key={cause}>{cause}</li>
                    ))}
                  </ul>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <p className="text-sm font-medium text-cyan-300">
                    Recommended actions
                  </p>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-300">
                    {explanation.recommended_actions.map((action) => (
                      <li key={action}>{action}</li>
                    ))}
                  </ul>
                </div>

                <p className="text-xs text-slate-500">
                  Source: {explanation.source}
                </p>
              </div>
            )}
          </div>
        )}
      </aside>
    </div>
  );
}