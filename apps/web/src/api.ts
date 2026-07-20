import type {
  Account,
  ApiErrorBody,
  Currency,
  RecipientLookup,
  SessionResponse,
  Transaction,
  TransferResponse,
  User,
} from "./types";

const API_URL = (import.meta.env.VITE_API_URL ?? "/api").replace(/\/$/, "");
const CSRF_COOKIE = "corebank_csrf";

const errorMessages: Record<string, string> = {
  email_already_registered: "Пользователь с такой почтой уже зарегистрирован",
  invalid_credentials: "Неверная почта или пароль",
  invalid_token: "Сессия истекла. Войдите снова",
  source_account_not_found: "Счёт списания не найден",
  destination_account_not_found: "Счёт получателя не найден",
  same_account_transfer: "Нельзя перевести деньги на тот же счёт",
  currency_mismatch: "Счета должны быть открыты в одной валюте",
  insufficient_funds: "На счёте недостаточно средств",
  phone_already_registered: "Этот номер телефона уже используется",
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
    credentials: "same-origin",
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
  const method = (options.method ?? "GET").toUpperCase();
  const csrfToken = document.cookie
    .split("; ")
    .find((entry) => entry.startsWith(`${CSRF_COOKIE}=`))
    ?.split("=")[1];
  if (!["GET", "HEAD", "OPTIONS"].includes(method) && !csrfToken) {
    throw new ApiError("Сессия недействительна. Войдите снова", 401);
  }
  return request<T>(path, {
    ...options,
    headers: {
      ...options.headers,
      ...(csrfToken ? { "X-CSRF-Token": decodeURIComponent(csrfToken) } : {}),
    },
  });
}

export function register(payload: {
  full_name: string;
  email: string;
  password: string;
  phone_number: string;
}): Promise<User> {
  return request<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function login(email: string, password: string): Promise<SessionResponse> {
  return request<SessionResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function getCurrentUser(): Promise<User> {
  return authorizedRequest<User>("/auth/me");
}

export function logout(): Promise<SessionResponse> {
  return authorizedRequest<SessionResponse>("/auth/logout", { method: "POST" });
}

export function updatePhoneNumber(phoneNumber: string): Promise<User> {
  return authorizedRequest<User>("/auth/me/phone", {
    method: "PATCH",
    body: JSON.stringify({ phone_number: phoneNumber }),
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

export function getTransactions(limit = 50, offset = 0): Promise<Transaction[]> {
  return authorizedRequest<Transaction[]>(`/transactions?limit=${limit}&offset=${offset}`);
}

export function createTransfer(payload: {
  from_account_id: string;
  recipient: string;
  amount: number;
}): Promise<TransferResponse> {
  return authorizedRequest<TransferResponse>("/transfers", {
    method: "POST",
    headers: { "Idempotency-Key": crypto.randomUUID() },
    body: JSON.stringify(payload),
  });
}

export function getTransferRecipient(
  fromAccountId: string,
  identifier: string,
): Promise<RecipientLookup> {
  const query = new URLSearchParams({
    from_account_id: fromAccountId,
    identifier,
  });
  return authorizedRequest<RecipientLookup>(`/transfers/recipient?${query}`);
}
