import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import * as api from "./api";

vi.mock("./api", async (importOriginal) => {
  const original = await importOriginal<typeof import("./api")>();
  return {
    ...original,
    clearToken: vi.fn(),
    getAccounts: vi.fn().mockResolvedValue([]),
    getCurrentUser: vi.fn(),
    getToken: vi.fn().mockReturnValue(null),
    getTransactions: vi.fn().mockResolvedValue([]),
    login: vi.fn(),
    register: vi.fn(),
    saveToken: vi.fn(),
  };
});

const user = {
  id: "user-1",
  email: "alex@example.com",
  full_name: "Алексей Иванов",
  is_active: true,
  created_at: "2026-07-20T08:00:00Z",
};

describe("authentication", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(api.getToken).mockReturnValue(null);
  });

  it("logs in and opens the dashboard", async () => {
    vi.mocked(api.login).mockResolvedValue({ access_token: "jwt-token", token_type: "bearer" });
    vi.mocked(api.getCurrentUser).mockResolvedValue(user);
    const browser = userEvent.setup();

    render(<MemoryRouter><App /></MemoryRouter>);

    await browser.type(screen.getByLabelText("Электронная почта"), user.email);
    await browser.type(screen.getByLabelText("Пароль"), "strong-password");
    await browser.click(screen.getByRole("button", { name: "Войти в CoreBank" }));

    expect(await screen.findByText("Добрый день, Алексей")).toBeInTheDocument();
    expect(api.login).toHaveBeenCalledWith(user.email, "strong-password");
    expect(api.saveToken).toHaveBeenCalledWith("jwt-token");
  });
});
