export interface User {
  id: string;
  email: string;
  full_name: string;
  phone_number: string | null;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export type Currency = "RUB" | "USD" | "EUR";

export interface Account {
  id: string;
  user_id: string;
  owner_name: string;
  card_number: string;
  balance: number;
  currency: Currency;
  created_at: string;
}

export interface Transaction {
  id: string;
  from_account_id: string;
  to_account_id: string;
  amount: number;
  currency: Currency;
  status: "completed";
  created_at: string;
}

export interface TransferResponse {
  transaction_id: string;
  from_account_id: string;
  to_account_id: string;
  amount: number;
  status: "completed";
}

export interface RecipientLookup {
  display_name: string;
  masked_card_number: string;
  currency: Currency;
}

export interface ApiErrorBody {
  detail?: {
    code?: string;
    message?: string;
  } | Array<{ msg?: string }>;
}
