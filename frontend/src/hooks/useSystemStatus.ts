import { useEffect, useState } from "react";

import { getApiHealth, getDatabaseHealth, HealthStatus } from "../services/healthService";

export interface SystemStatus {
  api: HealthStatus | null;
  database: HealthStatus | null;
  loading: boolean;
  error: string | null;
}

export function useSystemStatus(): SystemStatus {
  const [status, setStatus] = useState<SystemStatus>({
    api: null,
    database: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;

    async function check() {
      try {
        const [api, database] = await Promise.all([getApiHealth(), getDatabaseHealth()]);
        if (!cancelled) {
          setStatus({ api, database, loading: false, error: null });
        }
      } catch (err) {
        if (!cancelled) {
          setStatus({
            api: null,
            database: null,
            loading: false,
            error: err instanceof Error ? err.message : "Unknown error",
          });
        }
      }
    }

    check();
    return () => {
      cancelled = true;
    };
  }, []);

  return status;
}
