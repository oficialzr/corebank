import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import * as api from "./api";

vi.mock("./api", async (importOriginal) => {
  const original = await importOriginal<typeof import("./api")>();
  return {
    ...original,
    getAccounts: vi.fn().mockResolvedValue([]),
    getCurrentUser: vi.fn(),
    getTransactions: vi.fn().mockResolvedValue([]),
    login: vi.fn(),
    logout: vi.fn().mockResolvedValue({ authenticated: false }),
    register: vi.fn(),
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

describe("authentication", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(api.getCurrentUser).mockRejectedValue(new api.ApiError("No session", 401));
  });

  it("logs in and opens the dashboard", async () => {
    vi.mocked(api.login).mockResolvedValue({ authenticated: true });
    vi.mocked(api.getCurrentUser)
      .mockRejectedValueOnce(new api.ApiError("No session", 401))
      .mockResolvedValue(user);
    const browser = userEvent.setup();

    render(<MemoryRouter><App /></MemoryRouter>);

    await browser.type(await screen.findByLabelText("Электронная почта"), user.email);
    await browser.type(screen.getByLabelText("Пароль"), "strong-password");
    await browser.click(screen.getByRole("button", { name: "Войти в CoreBank" }));

    expect(await screen.findByText("Добрый день, Алексей")).toBeInTheDocument();
    expect(api.login).toHaveBeenCalledWith(user.email, "strong-password");
  });

  it("registers with a phone number before logging in", async () => {
    vi.mocked(api.register).mockResolvedValue(user);
    vi.mocked(api.login).mockResolvedValue({ authenticated: true });
    vi.mocked(api.getCurrentUser)
      .mockRejectedValueOnce(new api.ApiError("No session", 401))
      .mockResolvedValue(user);
    const browser = userEvent.setup();

    render(<MemoryRouter><App /></MemoryRouter>);

    await browser.click(await screen.findByRole("tab", { name: "Регистрация" }));
    await browser.type(screen.getByLabelText("Имя и фамилия"), user.full_name);
    await browser.type(screen.getByLabelText("Номер телефона"), "+7 999 123-45-67");
    await browser.type(screen.getByLabelText("Электронная почта"), user.email);
    await browser.type(screen.getByLabelText("Пароль"), "strong-password");
    await browser.click(screen.getByRole("button", { name: "Создать аккаунт" }));

    await waitFor(() => expect(api.register).toHaveBeenCalledWith({
      full_name: user.full_name,
      phone_number: "+7 999 123-45-67",
      email: user.email,
      password: "strong-password",
    }));
  });
});
