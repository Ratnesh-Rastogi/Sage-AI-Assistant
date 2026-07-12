/// <reference types="vitest" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      // "localhost:8000" works whether the backend is a local `uvicorn`
      // process (README: "Running locally without Docker") or a Compose
      // container, since Compose publishes it to the host on port 8000.
      // Only used by `vite dev` — the built artifact is served by nginx,
      // which has its own proxy_pass in docker/frontend/nginx.conf.
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/tests/setup.ts",
  },
});
