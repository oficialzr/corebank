import type { components } from "./generated/api-schema";

type Schemas = components["schemas"];

export type User = Schemas["UserResponse"];
export type SessionResponse = Schemas["SessionResponse"];
export type Currency = Schemas["Currency"];
export type Account = Omit<Schemas["AccountResponse"], "currency" | "user_id"> & {
  currency: Currency;
  user_id: string;
};
export type Transaction = Schemas["TransactionResponse"];
export type TransferResponse = Schemas["TransferResponse"];
export type RecipientLookup = Schemas["RecipientLookupResponse"];

export interface ApiErrorBody {
  detail?: {
    code?: string;
    message?: string;
  } | Array<{ msg?: string }>;
}
