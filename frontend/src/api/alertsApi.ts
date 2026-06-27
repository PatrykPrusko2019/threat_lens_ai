import { apiClient } from "./client";
import type { AlertExplanationResponse, AlertResponse } from "../types/alert";

export async function getAlerts(): Promise<AlertResponse[]> {
  const response = await apiClient.get<AlertResponse[]>("/alerts/");
  return response.data;
}

export async function explainAlert(
  alertId: number,
): Promise<AlertExplanationResponse> {
  const response = await apiClient.post<AlertExplanationResponse>(
    `/alerts/${alertId}/explain`,
  );

  return response.data;
}

export async function closeAlert(alertId: number): Promise<AlertResponse> {
  const response = await apiClient.patch<AlertResponse>(`/alerts/${alertId}`, {
    status: "closed",
  });

  return response.data;
}


