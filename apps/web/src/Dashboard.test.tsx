import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Dashboard from "./Dashboard";
import * as api from "./api";
import type { Account } from "./types";

vi.mock("./api", async (importOriginal) => {
  const original = await importOriginal<typeof import("./api")>();
  return {
    ...original,
    createAccount: vi.fn(),
    createTransfer: vi.fn(),
    getAccounts: vi.fn(),
    getTransferRecipient: vi.fn(),
    getTransactions: vi.fn(),
    updatePhoneNumber: vi.fn(),
  };
});

const user = {
  id: "user-1",
  email: "alex@example.com",
  full_name: "Алексей Иванов",
  phone_number: "+79991234567",
  is_active: true,
  is_admin: false,
  created_at: "2026-07-20T08:00:00Z",
};

const account: Account = {
  id: "acc-source-00000001",
  user_id: user.id,
  owner_name: user.full_name,
  card_number: "2200000000000004",
  balance: 100,
  currency: "RUB",
  created_at: "2026-07-20T08:00:00Z",
};

function renderDashboard() {
  return render(
    <MemoryRouter>
      <Dashboard user={user} onLogout={vi.fn()} onUserUpdated={vi.fn()} />
    </MemoryRouter>,
  );
}

describe("dashboard operations", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(api.getAccounts).mockResolvedValue([]);
    vi.mocked(api.getTransactions).mockResolvedValue([]);
    vi.mocked(api.getTransferRecipient).mockResolvedValue({
      display_name: "Мария Петрова",
      masked_card_number: "•••• 0012",
      currency: "RUB",
    });
  });

  it("opens a new account", async () => {
    vi.mocked(api.createAccount).mockResolvedValue({ ...account, currency: "USD" });
    const browser = userEvent.setup();
    renderDashboard();

    await screen.findByText("Пока нет счетов");
    await browser.click(screen.getByRole("button", { name: /Открыть счёт/ }));
    await browser.click(screen.getByRole("button", { name: /USD/ }));
    await browser.click(screen.getByRole("button", { name: "Открыть счёт" }));

    await waitFor(() => expect(api.createAccount).toHaveBeenCalledWith("USD"));
    expect(await screen.findByText("Долларовый счёт")).toBeInTheDocument();
  });

  it("confirms a transfer and refreshes dashboard data", async () => {
    const updatedAccount = { ...account, balance: 87.5 };
    vi.mocked(api.getAccounts)
      .mockResolvedValueOnce([account])
      .mockResolvedValueOnce([updatedAccount]);
    vi.mocked(api.createTransfer).mockResolvedValue({
      transaction_id: "tx-1",
      from_account_id: account.id,
      to_account_id: "acc-destination-0002",
      amount: 12.5,
      status: "completed",
    });
    const browser = userEvent.setup();
    renderDashboard();

    await screen.findByText("Рублёвый счёт");
    await browser.click(screen.getByRole("button", { name: /Перевести/ }));
    await browser.type(screen.getByLabelText("Телефон или номер карты"), "+79990000002");
    await browser.type(screen.getByLabelText("Сумма, RUB"), "12,50");
    await browser.click(screen.getByRole("button", { name: "Продолжить" }));
    await browser.click(screen.getByRole("button", { name: "Подтвердить" }));

    expect(await screen.findByText("Перевод выполнен")).toBeInTheDocument();
    expect(api.createTransfer).toHaveBeenCalledWith({
      from_account_id: account.id,
      recipient: "+79990000002",
      amount: 12.5,
    });
    expect(api.getAccounts).toHaveBeenCalledTimes(2);
    expect(api.getTransactions).toHaveBeenCalledTimes(2);
  });
});
