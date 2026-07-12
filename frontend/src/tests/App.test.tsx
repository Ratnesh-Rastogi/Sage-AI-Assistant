import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import App from "../App";
import * as healthService from "../services/healthService";

describe("App (foundation status screen)", () => {
  it("renders the Sage heading", () => {
    vi.spyOn(healthService, "getApiHealth").mockResolvedValue({ status: "ok" });
    vi.spyOn(healthService, "getDatabaseHealth").mockResolvedValue({ status: "ok" });

    render(<App />);
    expect(screen.getByText("Sage")).toBeInTheDocument();
  });

  it("shows both services online when health checks succeed", async () => {
    vi.spyOn(healthService, "getApiHealth").mockResolvedValue({
      status: "ok",
      service: "sage-backend",
    });
    vi.spyOn(healthService, "getDatabaseHealth").mockResolvedValue({
      status: "ok",
      database: "connected",
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getAllByText("online")).toHaveLength(2);
    });
  });

  it("shows an error message when the backend is unreachable", async () => {
    vi.spyOn(healthService, "getApiHealth").mockRejectedValue(
      new Error("Network Error")
    );
    vi.spyOn(healthService, "getDatabaseHealth").mockRejectedValue(
      new Error("Network Error")
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Couldn't reach the backend/i)).toBeInTheDocument();
    });
  });
});
