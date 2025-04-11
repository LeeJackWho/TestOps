import { expect } from "@playwright/test";
import { test } from "../fixture";

test.beforeEach(async ({ page }) => {
  await page.goto("https://ui.example.com");
});

test("ai todo - Chinese Prompt", async ({ ai, aiQuery, aiAssert, aiTap }) => {
  await ai("账户输入：，密码输入：.，识别图形验证码并输入，进行登录");
});