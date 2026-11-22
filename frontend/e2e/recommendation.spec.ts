import { expect, test } from "@playwright/test";

// Main journey for the M1 first slice: form submission shows one fixture
// card. Covers P01 (blank input feedback), P02 (one demo album, no
// listening or search link), P05 (failed request keeps the text and allows retry) and the
// narrow-viewport plus keyboard path in P07.

test("valid description shows one fixture album", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).fill(
    "Late-night jazz with a steady beat and no vocals."
  );
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("heading", { name: /blue line trio/i })).toBeVisible();
  await expect(page.getByText(/fixture demo pick/i)).toBeVisible();
  await expect(page.getByText(/ignores your description/i).first()).toBeVisible();
  await expect(page.getByText(/same demo entry/i)).toBeVisible();
  await expect(page.getByText(/Reference/i)).toBeVisible();
  await expect(page.getByRole("link")).toHaveCount(0);
});

test("blank description shows a clear message", async ({ page }) => {
  await page.goto("/");
  const field = page.getByLabel(/what do you want to hear/i);
  await field.fill("   ");
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("alert")).toContainText(/describe what you want/i);
  await expect(field).toBeFocused();
});

test("shows a live character count matching the trimmed limit", async ({ page }) => {
  await page.goto("/");
  const field = page.getByLabel(/what do you want to hear/i);
  await expect(field).not.toHaveAttribute("maxlength", "500");
  await field.fill("Late-night jazz");
  await expect(page.getByText("15 / 500")).toBeVisible();
  await field.fill(`  ${"z".repeat(500)}  `);
  await expect(page.getByText("500 / 500")).toBeVisible();
});

test("server-rejected input shows inline guidance with a reference", async ({
  page
}) => {
  await page.goto("/");
  const field = page.getByLabel(/what do you want to hear/i);
  await field.fill("A quiet rainy evening.");
  await page.route("**/api/recommendations", (route) =>
    route.fulfill({
      status: 422,
      headers: {
        "Content-Type": "application/json",
        "X-Request-ID": "test-ref-422"
      },
      body: "{}"
    })
  );
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("alert")).toContainText(/not accepted/i);
  await expect(page.getByText(/test-ref-422/)).toBeVisible();
  await expect(field).toBeFocused();
  await page.unroute("**/api/recommendations");
});

test("malformed response keeps the description and allows retry", async ({ page }) => {
  const description = "Late-night jazz with a steady beat and no vocals.";
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).fill(description);
  await page.route("**/api/recommendations", async (route) => {
    await route.fulfill({
      status: 200,
      headers: { "Content-Type": "application/json", "X-Request-ID": "test-ref-bad-shape" },
      body: JSON.stringify({ album: { id: "FIX-001" }, mode: "local" })
    });
  });
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("alert")).toContainText(/still here/i);
  await expect(page.getByLabel(/what do you want to hear/i)).toHaveValue(description);
  await expect(page.getByRole("button", { name: /try again/i })).toBeFocused();
  await expect(page.getByText(/test-ref-bad-shape/)).toBeVisible();
  await page.unroute("**/api/recommendations");
});

test("failed request keeps the description and allows retry", async ({ page }) => {
  const description = "Something energetic and sample-heavy.";
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).fill(description);
  await page.route("**/api/recommendations", (route) => route.abort());
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("alert")).toContainText(/still here/i);
  await expect(page.getByLabel(/what do you want to hear/i)).toHaveValue(description);
  await expect(page.getByRole("button", { name: /try again/i })).toBeFocused();
  await page.unroute("**/api/recommendations");
  await page.getByRole("button", { name: /try again/i }).click();
  await expect(page.getByRole("heading", { name: /—/ })).toBeVisible();
});

test("loading limits duplicate submissions", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).fill(
    "Late-night jazz with a steady beat and no vocals."
  );
  await page.route("**/api/recommendations", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 500));
    await route.continue();
  });
  const submit = page.getByRole("button", { name: /recommend an album/i });
  await submit.click();
  await expect(page.getByText(/looking for one album/i)).toBeVisible();
  await expect(page.getByRole("button", { name: /finding an album/i })).toBeDisabled();
  await page.unroute("**/api/recommendations");
  await expect(page.getByRole("heading", { name: /blue line trio/i })).toBeVisible();
});

test("sends a single request on rapid double submit", async ({ page }) => {
  let calls = 0;
  await page.goto("/");
  await page.route("**/api/recommendations", async (route) => {
    calls += 1;
    await route.fulfill({
      status: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        album: {
          id: "FIX-001",
          artist: "Blue Line Trio",
          title: "Night Loop",
          year: null,
          reason: "Fixture demo pick.",
          tag_status: "fixture"
        },
        mode: "local"
      })
    });
  });
  await page.getByLabel(/what do you want to hear/i).fill(
    "Late-night jazz with a steady beat and no vocals."
  );
  // Two clicks in one task: the second handler runs before React
  // re-renders, so a guard reading stale state would fire twice.
  await page.evaluate(() => {
    const button = document.querySelector('button[type="submit"]');
    if (button) {
      button.dispatchEvent(
        new MouseEvent("click", { bubbles: true, cancelable: true })
      );
      button.dispatchEvent(
        new MouseEvent("click", { bubbles: true, cancelable: true })
      );
    }
  });
  await expect(page.getByRole("heading", { name: /blue line trio/i })).toBeVisible();
  expect(calls).toBe(1);
  await page.unroute("**/api/recommendations");
});

test("keyboard can reach the result", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).focus();
  await page.keyboard.type("A quiet rainy evening, some groove.");
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: /recommend an album/i })).toBeFocused();
  await page.keyboard.press("Enter");
  const heading = page.getByRole("heading", { name: /—/ });
  await expect(heading).toBeVisible();
  await expect(heading).toBeFocused();
  await expect(page.getByRole("link")).toHaveCount(0);
});
