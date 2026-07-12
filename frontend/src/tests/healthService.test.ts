import { describe, expect, it, vi } from "vitest";

import { api } from "../services/api";
import { getApiHealth, getDatabaseHealth } from "../services/healthService";

describe("healthService", () => {
  it("getApiHealth returns the response body", async () => {
    vi.spyOn(api, "get").mockResolvedValue({ data: { status: "ok" } });
    const result = await getApiHealth();
    expect(result.status).toBe("ok");
    expect(api.get).toHaveBeenCalledWith("/health");
  });

  it("getDatabaseHealth returns the response body", async () => {
    vi.spyOn(api, "get").mockResolvedValue({
      data: { status: "ok", database: "connected" },
    });
    const result = await getDatabaseHealth();
    expect(result.database).toBe("connected");
    expect(api.get).toHaveBeenCalledWith("/health/db");
  });

  it("propagates errors from the API client", async () => {
    vi.spyOn(api, "get").mockRejectedValue(new Error("timeout"));
    await expect(getApiHealth()).rejects.toThrow("timeout");
  });
});
