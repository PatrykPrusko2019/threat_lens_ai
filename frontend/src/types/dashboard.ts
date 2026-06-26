export type AlertResponse = {
    id: number;
    event_id: number | null;
    title: string;
    severity: string;
    status: string;
    risk_score: number;
    description: string | null;
    created_at: string;
    updated_at: string | null;
};

export type DashboardSummaryResponse = {
    total_events: number;
    total_alerts: number;
    open_alerts: number;
    closed_alerts: number;
    critical_alerts: number;
    high_alerts: number;
    latest_alerts: AlertResponse[];
};