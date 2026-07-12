import { useSystemStatus } from "./hooks/useSystemStatus";

function StatusPill({ label, ok }: { label: string; ok: boolean | null }) {
  const color =
    ok === null ? "bg-neutral-300" : ok ? "bg-sage-500" : "bg-red-500";
  const text = ok === null ? "checking..." : ok ? "online" : "unreachable";
  return (
    <div className="flex items-center gap-3 rounded-lg border border-neutral-200 bg-white px-4 py-3">
      <span className={`h-2.5 w-2.5 rounded-full ${color}`} />
      <span className="font-medium text-neutral-800">{label}</span>
      <span className="ml-auto text-sm text-neutral-500">{text}</span>
    </div>
  );
}

function App() {
  const { api, database, loading, error } = useSystemStatus();

  return (
    <div className="min-h-screen bg-neutral-50 text-neutral-900">
      <div className="mx-auto flex max-w-xl flex-col gap-6 px-6 py-16">
        <div>
          <h1 className="text-2xl font-semibold text-sage-700">Sage</h1>
          <p className="mt-1 text-neutral-600">
            Foundation phase — the chat interface, memory tools, and dashboards
            arrive in later phases. This screen confirms the backend and
            database are reachable.
          </p>
        </div>

        <div className="flex flex-col gap-3">
          <StatusPill label="Backend API" ok={loading ? null : api?.status === "ok"} />
          <StatusPill
            label="PostgreSQL"
            ok={loading ? null : database?.status === "ok"}
          />
        </div>

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            Couldn't reach the backend: {error}. Make sure the backend
            container is running and reachable at /api/v1.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
