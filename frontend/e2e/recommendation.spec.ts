import { expect, test } from "@playwright/test";

// Main journey for the M1 first slice: form submission shows one fixture
// card. Covers P01 (blank input feedback), P02 (one eligible album with a
// link), P05 (failed request keeps the text and allows retry) and the
// narrow-viewport plus keyboard path in P07.

test("valid description shows one fixture album", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).fill(
    "Late-night jazz with a steady beat and no vocals."
  );
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("heading", { name: /blue line trio/i })).toBeVisible();
  await expect(page.getByText(/fixture demo pick/i)).toBeVisible();
  const link = page.getByRole("link", { name: /search listening options/i });
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute("href", /https:\/\//);
});

test("blank description shows a clear message", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).fill("   ");
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("alert")).toContainText(/describe what you want/i);
});

test("failed request keeps the description and allows retry", async ({ page }) => {
  const description = "Something energetic and sample-heavy.";
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).fill(description);
  await page.route("**/api/recommendations", (route) => route.abort());
  await page.getByRole("button", { name: /recommend an album/i }).click();
  await expect(page.getByRole("alert")).toContainText(/still here/i);
  await expect(page.getByLabel(/what do you want to hear/i)).toHaveValue(description);
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

test("keyboard can reach the result and the listening link", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel(/what do you want to hear/i).focus();
  await page.keyboard.type("A quiet rainy evening, some groove.");
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: /recommend an album/i })).toBeFocused();
  await page.keyboard.press("Enter");
  const heading = page.getByRole("heading", { name: /—/ });
  await expect(heading).toBeVisible();
  await expect(heading).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: /search listening options/i })
  ).toBeFocused();
});
