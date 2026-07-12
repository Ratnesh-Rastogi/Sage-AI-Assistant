/**
 * End-to-end tests (Playwright), per SAGE_BLUEPRINT.md Section 128 / 258.
 *
 * Phase 1 provides only the foundation status screen, so this smoke test
 * checks that the app shell loads. Full user-flow E2E tests (chat, memory,
 * tasks, reminders) are added as those features are built in later phases.
 *
 * Run with: npx playwright test tests/e2e
 * (requires the full docker-compose stack running).
 */
import { expect, test } from "@playwright/test";

test("Sage foundation screen loads and shows service status", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await expect(page.getByText("Sage")).toBeVisible();
  await expect(page.getByText("Backend API")).toBeVisible();
  await expect(page.getByText("PostgreSQL")).toBeVisible();
});
