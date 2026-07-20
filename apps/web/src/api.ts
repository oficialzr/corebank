import type {
  Account,
  ApiErrorBody,
  Currency,
  TokenResponse,
  Transaction,
  TransferResponse,
  User,
} from "./types";

const API_URL = (import.meta.env.VITE_API_URL ?? "/api").replace(/\/$/, "");
const TOKEN_KEY = "corebank_access_token";

const errorMessages: Record<string, string> = {
  email_already_registered: "Пользователь с такой почтой уже зарегистрирован",
  invalid_credentials: "Неверная почта или пароль",
  invalid_token: "Сессия истекла. Войдите снова",
  source_account_not_found: "Счёт списания не найден",
  destination_account_not_found: "Счёт получателя не найден",
  same_account_transfer: "Нельзя перевести деньги на тот же счёт",
  currency_mismatch: "Счета должны быть открыты в одной валюте",
  insufficient_funds: "На счёте недостаточно средств",
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const body = (await response.json().catch(() => ({}))) as ApiErrorBody;
    const detail = body.detail;
    const code = !Array.isArray(detail) ? detail?.code : undefined;
    const fallback = Array.isArray(detail)
      ? detail[0]?.msg
      : detail?.message;

    throw new ApiError(
      (code && errorMessages[code]) || fallback || "Не удалось выполнить запрос",
      response.status,
    );
  }

  return response.json() as Promise<T>;
}

async function authorizedRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();

  if (!token) {
    throw new ApiError("Необходимо войти в аккаунт", 401);
  }

  try {
    return await request<T>(path, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      },
    });
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      clearToken();
    }
    throw error;
  }
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function saveToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export function register(payload: {
  full_name: string;
  email: string;
  password: string;
}): Promise<User> {
  return request<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function login(email: string, password: string): Promise<TokenResponse> {
  return request<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function getCurrentUser(token: string): Promise<User> {
  return request<User>("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function getAccounts(): Promise<Account[]> {
  return authorizedRequest<Account[]>("/accounts");
}

export function createAccount(currency: Currency): Promise<Account> {
  return authorizedRequest<Account>("/accounts", {
    method: "POST",
    body: JSON.stringify({ currency }),
  });
}

export function getTransactions(): Promise<Transaction[]> {
  return authorizedRequest<Transaction[]>("/transactions");
}

export function createTransfer(payload: {
  from_account_id: string;
  to_account_id: string;
  amount: number;
}): Promise<TransferResponse> {
  return authorizedRequest<TransferResponse>("/transfers", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
