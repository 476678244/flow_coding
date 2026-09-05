import { test, expect } from "@playwright/test";

/**
 * 本夹 keep：features/__feature_id__/test_<slug>_e2e.spec.ts
 * 无 DOM：删掉本文件。不要放到 frontend/e2e/。
 * 前端 :5173 打同一套 /api。刷新后仍能做 Y。
 */
test.describe("__feature_id__", () => {
  test("看得见的 X → 刷新 → 仍能做 Y", async ({ page }) => {
    await page.goto("/");
    // await expect(page.getByTestId("demo-title")).toBeVisible();
    await page.reload();
    expect.soft(true, "replace with real assertions").toBeTruthy();
  });
});
