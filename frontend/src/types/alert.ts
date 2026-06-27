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

export type AlertExplanationResponse = {
  alert_id: number;
  title: string;
  severity: string;
  risk_score: number;
  status: string;
  summary: string;
  severity_explanation: string;
  possible_causes: string[];
  recommended_actions: string[];
  source: string;
};