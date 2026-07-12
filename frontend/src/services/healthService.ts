import { api } from "./api";

export interface HealthStatus {
  status: string;
  service?: string;
  database?: string;
  detail?: string;
}

export async function getApiHealth(): Promise<HealthStatus> {
  const response = await api.get<HealthStatus>("/health");
  return response.data;
}

export async function getDatabaseHealth(): Promise<HealthStatus> {
  const response = await api.get<HealthStatus>("/health/db");
  return response.data;
}
