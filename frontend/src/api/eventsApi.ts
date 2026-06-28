import { apiClient } from "./client";
import type { EventFilters, SecurityEventResponse } from "../types/event";


export async function getEvents(
    filters: EventFilters = {},
): Promise<SecurityEventResponse[]> {
    const response = await apiClient.get<SecurityEventResponse[]>("/events/", {
        params: {
            event_type: filters.event_type || undefined,
            severity: filters.severity || undefined,
            source_ip: filters.source_ip || undefined,
            limit: filters.limit ?? 50,
        },
    });

    return response.data;
}