export type SecurityEventResponse = {
    id: number;
    event_type: string;
    severity: string;
    source_ip: string | null;
    description: string | null;
    user_id?: number | null;
    created_at?: string | null;
};

export type EventFilters = {
    event_type?: string;
    severity?: string;
    source_ip?: string;
    limit?: number;
};