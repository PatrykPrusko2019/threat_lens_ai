import { useQuery } from "@tanstack/react-query";
import { Filter, ShieldAlert } from "lucide-react";
import { useState } from "react";

import { getEvents } from "../api/eventsApi";
import type { EventFilters } from "../types/event";

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

  if (severity === "low") {
    return "bg-emerald-500/10 text-emerald-300 border-emerald-500/20";
  }

  return "bg-slate-700/60 text-slate-300 border-slate-600";
}

function formatDate(value?: string | null) {
  if (!value) {
    return "—";
  }

  return new Date(value).toLocaleString();
}

export function EventsPage() {
  const [filters, setFilters] = useState<EventFilters>({
    event_type: "",
    severity: "",
    source_ip: "",
    limit: 50,
  });

  const [appliedFilters, setAppliedFilters] = useState<EventFilters>({
    limit: 50,
  });

  const { data, isLoading, isError } = useQuery({
    queryKey: ["events", appliedFilters],
    queryFn: () => getEvents(appliedFilters),
  });

  function handleApplyFilters() {
    setAppliedFilters({
      event_type: filters.event_type?.trim() || undefined,
      severity: filters.severity?.trim() || undefined,
      source_ip: filters.source_ip?.trim() || undefined,
      limit: filters.limit ?? 50,
    });
  }

  function handleClearFilters() {
    const emptyFilters = {
      event_type: "",
      severity: "",
      source_ip: "",
      limit: 50,
    };

    setFilters(emptyFilters);
    setAppliedFilters({ limit: 50 });
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
        <div className="mb-5 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <h3 className="text-lg font-semibold">Security Events</h3>
            <p className="text-sm text-slate-400">
              Raw security events collected and analyzed by ThreatLens AI
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-slate-800 px-4 py-2 text-sm text-slate-300">
            <ShieldAlert size={16} />
            {data?.length ?? 0} events
          </div>
        </div>

        <div className="grid gap-4 rounded-xl border border-slate-800 bg-slate-950 p-4 md:grid-cols-4">
          <div>
            <label className="text-xs text-slate-400">Event type</label>
            <input
              className="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
              value={filters.event_type ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  event_type: event.target.value,
                }))
              }
              placeholder="login_failed"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400">Severity</label>
            <select
              className="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
              value={filters.severity ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  severity: event.target.value,
                }))
              }
            >
              <option value="">All</option>
              <option value="low">low</option>
              <option value="medium">medium</option>
              <option value="high">high</option>
              <option value="critical">critical</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-slate-400">Source IP</label>
            <input
              className="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
              value={filters.source_ip ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  source_ip: event.target.value,
                }))
              }
              placeholder="192.168.1.10"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400">Limit</label>
            <input
              className="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
              value={filters.limit ?? 50}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  limit: Number(event.target.value),
                }))
              }
              type="number"
              min={1}
              max={200}
            />
          </div>

          <div className="flex gap-3 md:col-span-4">
            <button
              onClick={handleApplyFilters}
              className="inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
              type="button"
            >
              <Filter size={16} />
              Apply filters
            </button>

            <button
              onClick={handleClearFilters}
              className="rounded-lg border border-slate-800 px-4 py-2 text-sm text-slate-300 transition hover:border-slate-600"
              type="button"
            >
              Clear
            </button>
          </div>
        </div>

        {isLoading && (
          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-6">
            <p className="text-slate-400">Loading security events...</p>
          </div>
        )}

        {isError && (
          <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-6">
            <h3 className="text-lg font-semibold text-red-300">
              Security events unavailable
            </h3>
            <p className="mt-2 text-sm text-red-200/80">
              Check if the backend is running and your token is valid.
            </p>
          </div>
        )}

        {!isLoading && !isError && (
          <div className="mt-6 overflow-hidden rounded-xl border border-slate-800">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-950 text-slate-400">
                <tr>
                  <th className="px-4 py-3">Type</th>
                  <th className="px-4 py-3">Severity</th>
                  <th className="px-4 py-3">Source IP</th>
                  <th className="px-4 py-3">Description</th>
                  <th className="px-4 py-3">Created</th>
                </tr>
              </thead>

              <tbody>
                {!data || data.length === 0 ? (
                  <tr className="border-t border-slate-800">
                    <td className="px-4 py-6 text-slate-500" colSpan={5}>
                      No security events found.
                    </td>
                  </tr>
                ) : (
                  data.map((event) => (
                    <tr key={event.id} className="border-t border-slate-800">
                      <td className="px-4 py-3">
                        <p className="font-medium text-slate-200">
                          {event.event_type}
                        </p>
                      </td>

                      <td className="px-4 py-3">
                        <span
                          className={[
                            "rounded-full border px-3 py-1 text-xs font-medium",
                            getSeverityClass(event.severity),
                          ].join(" ")}
                        >
                          {event.severity}
                        </span>
                      </td>

                      <td className="px-4 py-3 font-mono text-xs text-slate-300">
                        {event.source_ip ?? "—"}
                      </td>

                      <td className="px-4 py-3">
                        <p className="max-w-lg truncate text-slate-400">
                          {event.description ?? "No description"}
                        </p>
                      </td>

                      <td className="px-4 py-3 text-xs text-slate-500">
                        {formatDate(event.created_at)}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}