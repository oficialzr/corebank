import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";
import { Client } from "pg";

const password = "strong-password";

async function register(page: Page, name: string, email: string, phone: string) {
  await page.goto("/");
  await page.getByRole("tab", { name: "Регистрация" }).click();
  await page.getByLabel("Имя и фамилия").fill(name);
  await page.getByLabel("Номер телефона").fill(phone);
  await page.getByLabel("Электронная почта").fill(email);
  await page.locator('input[type="password"]').fill(password);
  await page.getByRole("button", { name: "Создать аккаунт" }).click();
  await expect(page.getByRole("heading", { name: new RegExp(name.split(" ")[0]) })).toBeVisible();
}

test("registration, account opening, session restoration and transfer", async ({ page }) => {
  const suffix = `${Date.now()}`.slice(-8);
  const senderEmail = `sender-${suffix}@example.com`;
  const recipientEmail = `recipient-${suffix}@example.com`;
  const senderPhone = `+791${suffix}`;
  const recipientPhone = `+792${suffix}`;

  await register(page, "Sender User", senderEmail, senderPhone);
  await page.getByRole("button", { name: /Открыть счёт/ }).click();
  await page.getByRole("button", { name: "Открыть счёт", exact: true }).click();
  await expect(page.getByText("Рублёвый счёт")).toBeVisible();

  await page.reload();
  await expect(page.getByRole("heading", { name: /Sender/ })).toBeVisible();
  await page.getByRole("button", { name: "Выйти" }).click();

  await register(page, "Recipient User", recipientEmail, recipientPhone);
  await page.getByRole("button", { name: /Открыть счёт/ }).click();
  await page.getByRole("button", { name: "Открыть счёт", exact: true }).click();
  await page.getByRole("button", { name: "Выйти" }).click();

  const database = new Client({
    connectionString: "postgresql://corebank:corebank@127.0.0.1:5433/corebank",
  });
  await database.connect();
  await database.query(
    "UPDATE accounts SET balance = 500.00 WHERE user_id = (SELECT id FROM users WHERE email = $1)",
    [senderEmail],
  );
  await database.end();

  await page.getByLabel("Электронная почта").fill(senderEmail);
  await page.locator('input[type="password"]').fill(password);
  await page.getByRole("button", { name: "Войти в CoreBank" }).click();
  await page.getByRole("button", { name: /Перевести/ }).click();
  await page.getByLabel("Телефон или номер карты").fill(recipientPhone);
  await page.getByLabel("Сумма, RUB").fill("25,50");
  await page.getByRole("button", { name: "Продолжить" }).click();
  await expect(page.getByText("Recipient User")).toBeVisible();
  await page.getByRole("button", { name: "Подтвердить" }).click();
  await expect(page.getByText("Перевод выполнен")).toBeVisible();
});
