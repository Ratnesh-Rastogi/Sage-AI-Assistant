import axios from "axios";

/**
 * Central Axios instance. Components must never call the API directly
 * (SAGE_BLUEPRINT.md Section 125) — they go through services/*.ts.
 */
export const api = axios.create({
  baseURL: "/api/v1",
  timeout: 10000,
});
