import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ApiError, createAccount, getAccounts, getTransactions } from "./api";
import type { Account, Currency, Transaction, User } from "./types";
import "./dashboard.css";

const currencyNames: Record<Currency, string> = {
  RUB: "Рублёвый счёт",
  USD: "Долларовый счёт",
  EUR: "Счёт в евро",
};

function formatMoney(amount: number, currency: Currency): string {
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(amount / 100);
}

function shortAccountId(id: string): string {
  return `•• ${id.slice(-8).toUpperCase()}`;
}

function DashboardLogo() {
  return (
    <Link className="dashboard-brand" to="/" aria-label="CoreBank, на главную">
      <span className="brand-mark"><i /><i /></span>
      <span>CoreBank</span>
    </Link>
  );
}

export default function Dashboard({
  user,
  onLogout,
}: {
  user: User;
  onLogout: () => void;
}) {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showNewAccount, setShowNewAccount] = useState(false);
  const [currency, setCurrency] = useState<Currency>("RUB");
  const [creating, setCreating] = useState(false);

  const loadDashboard = useCallback(async () => {
    setError("");
    try {
      const [accountData, transactionData] = await Promise.all([
        getAccounts(),
        getTransactions(),
      ]);
      setAccounts(accountData);
      setTransactions(transactionData);
    } catch (requestError) {
      if (requestError instanceof ApiError && requestError.status === 401) {
        onLogout();
        return;
      }
      setError(
        requestError instanceof ApiError
          ? requestError.message
          : "Не удалось загрузить данные кабинета",
      );
    } finally {
      setLoading(false);
    }
  }, [onLogout]);

  useEffect(() => {
    void loadDashboard();
  }, [loadDashboard]);

  const ownedAccountIds = useMemo(
    () => new Set(accounts.map((account) => account.id)),
    [accounts],
  );

  const balances = useMemo(() => {
    return accounts.reduce<Partial<Record<Currency, number>>>((result, account) => {
      result[account.currency] = (result[account.currency] ?? 0) + account.balance;
      return result;
    }, {});
  }, [accounts]);

  async function handleCreateAccount() {
    setCreating(true);
    setError("");
    try {
      const account = await createAccount(currency);
      setAccounts((current) => [...current, account]);
      setShowNewAccount(false);
    } catch (requestError) {
      if (requestError instanceof ApiError && requestError.status === 401) {
        onLogout();
        return;
      }
      setError(
        requestError instanceof ApiError
          ? requestError.message
          : "Не удалось открыть счёт",
      );
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="dashboard-shell">
      <aside className="dashboard-sidebar">
        <DashboardLogo />
        <nav aria-label="Навигация кабинета">
          <a className="active" href="#overview"><span>⌂</span> Обзор</a>
          <a href="#accounts"><span>▣</span> Счета</a>
          <a href="#transactions"><span>↕</span> Операции</a>
          <span className="disabled"><span>→</span> Переводы <small>скоро</small></span>
          <span className="disabled"><span>◇</span> Карты <small>скоро</small></span>
        </nav>
        <div className="sidebar-footer">
          <div className="mini-avatar">{user.full_name.charAt(0).toUpperCase()}</div>
          <div><b>{user.full_name}</b><span>{user.email}</span></div>
          <button onClick={onLogout} type="button" aria-label="Выйти">↗</button>
        </div>
      </aside>

      <main className="dashboard-main" id="overview">
        <header className="dashboard-header">
          <div>
            <span className="dashboard-date">
              {new Intl.DateTimeFormat("ru-RU", { weekday: "long", day: "numeric", month: "long" }).format(new Date())}
            </span>
            <h1>Добрый день, {user.full_name.split(" ")[0]}</h1>
          </div>
          <button className="new-account-button" onClick={() => setShowNewAccount(true)} type="button">
            <span>+</span> Открыть счёт
          </button>
        </header>

        {error && (
          <div className="dashboard-error" role="alert">
            <span>{error}</span>
            <button onClick={() => void loadDashboard()} type="button">Повторить</button>
          </div>
        )}

        {loading ? (
          <div className="dashboard-loading"><div className="loader" /><span>Загружаем ваши финансы…</span></div>
        ) : (
          <>
            <section className="balance-summary" aria-label="Баланс по валютам">
              <div>
                <span>Средства на счетах</span>
                <h2>
                  {accounts.length === 0
                    ? "Пока нет счетов"
                    : Object.keys(balances).length === 1
                      ? formatMoney(Object.values(balances)[0] ?? 0, Object.keys(balances)[0] as Currency)
                      : `${accounts.length} активных счёта`}
                </h2>
                <p>{accounts.length === 0 ? "Откройте первый счёт, чтобы начать" : "Данные обновлены только что"}</p>
              </div>
              <div className="balance-breakdown">
                {(Object.entries(balances) as Array<[Currency, number]>).map(([code, amount]) => (
                  <span key={code}><small>{code}</small><b>{formatMoney(amount, code)}</b></span>
                ))}
              </div>
            </section>

            <section className="dashboard-section" id="accounts">
              <div className="section-heading">
                <div><span>Ваши продукты</span><h2>Счета</h2></div>
                <button onClick={() => setShowNewAccount(true)} type="button">Добавить +</button>
              </div>

              {accounts.length === 0 ? (
                <div className="empty-state">
                  <div>＋</div><h3>Здесь появятся ваши счета</h3>
                  <p>Открытие занимает несколько секунд и не требует документов.</p>
                  <button onClick={() => setShowNewAccount(true)} type="button">Открыть первый счёт</button>
                </div>
              ) : (
                <div className="account-grid">
                  {accounts.map((account, index) => (
                    <article className={`account-card tone-${index % 3}`} key={account.id}>
                      <div><span>{currencyNames[account.currency]}</span><small>{account.currency}</small></div>
                      <strong>{formatMoney(account.balance, account.currency)}</strong>
                      <footer><span>{shortAccountId(account.id)}</span><i>CB</i></footer>
                    </article>
                  ))}
                </div>
              )}
            </section>

            <section className="dashboard-section" id="transactions">
              <div className="section-heading">
                <div><span>История</span><h2>Последние операции</h2></div>
              </div>
              {transactions.length === 0 ? (
                <div className="transactions-empty">Операций пока нет — здесь появится история переводов.</div>
              ) : (
                <div className="transaction-list">
                  {transactions.slice(0, 8).map((transaction) => {
                    const incoming = ownedAccountIds.has(transaction.to_account_id);
                    return (
                      <article key={transaction.id}>
                        <span className={incoming ? "tx-icon incoming" : "tx-icon outgoing"}>{incoming ? "↓" : "↑"}</span>
                        <div>
                          <b>{incoming ? "Входящий перевод" : "Исходящий перевод"}</b>
                          <small>{new Intl.DateTimeFormat("ru-RU", { day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" }).format(new Date(transaction.created_at))}</small>
                        </div>
                        <strong className={incoming ? "positive" : ""}>
                          {incoming ? "+" : "−"}{formatMoney(transaction.amount, transaction.currency)}
                        </strong>
                      </article>
                    );
                  })}
                </div>
              )}
            </section>
          </>
        )}
      </main>

      {showNewAccount && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setShowNewAccount(false)}>
          <section className="account-modal" role="dialog" aria-modal="true" aria-labelledby="new-account-title" onMouseDown={(event) => event.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowNewAccount(false)} type="button" aria-label="Закрыть">×</button>
            <span className="eyebrow">Новый продукт</span>
            <h2 id="new-account-title">Открыть счёт</h2>
            <p>Выберите валюту. Счёт сразу появится в вашем кабинете.</p>
            <div className="currency-options">
              {(["RUB", "USD", "EUR"] as Currency[]).map((code) => (
                <button className={currency === code ? "selected" : ""} onClick={() => setCurrency(code)} type="button" key={code}>
                  <b>{code === "RUB" ? "₽" : code === "USD" ? "$" : "€"}</b>
                  <span>{code}</span>
                </button>
              ))}
            </div>
            <button className="modal-submit" disabled={creating} onClick={() => void handleCreateAccount()} type="button">
              {creating ? "Открываем…" : "Открыть счёт"}
            </button>
          </section>
        </div>
      )}
    </div>
  );
}
