import { useCallback, useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import {
  ApiError,
  clearToken,
  getCurrentUser,
  getToken,
  login,
  register,
  saveToken,
} from "./api";
import type { User } from "./types";
import Dashboard from "./Dashboard";

type AuthMode = "login" | "register";

function ArrowIcon() {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true">
      <path d="M4 10h12M11.5 5.5 16 10l-4.5 4.5" />
    </svg>
  );
}

function SparkIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3.5c.55 4.95 3.55 7.95 8.5 8.5-4.95.55-7.95 3.55-8.5 8.5-.55-4.95-3.55-7.95-8.5-8.5 4.95-.55 7.95-3.55 8.5-8.5Z" />
    </svg>
  );
}

function AuthPanel({
  mode,
  onModeChange,
  onAuthenticated,
}: {
  mode: AuthMode;
  onModeChange: (mode: AuthMode) => void;
  onAuthenticated: (user: User) => void;
}) {
  const emailRef = useRef<HTMLInputElement>(null);
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setError("");
    emailRef.current?.focus();
  }, [mode]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (mode === "register") {
        await register({ full_name: fullName, email, password, phone_number: phoneNumber });
      }

      const token = await login(email, password);
      saveToken(token.access_token);
      const user = await getCurrentUser(token.access_token);
      onAuthenticated(user);
    } catch (requestError) {
      setError(
        requestError instanceof ApiError
          ? requestError.message
          : "Сервис временно недоступен. Попробуйте ещё раз",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-card" id="auth" aria-labelledby="auth-title">
      <div className="auth-tabs" role="tablist" aria-label="Авторизация">
        <button
          className={mode === "login" ? "active" : ""}
          onClick={() => onModeChange("login")}
          role="tab"
          aria-selected={mode === "login"}
          type="button"
        >
          Войти
        </button>
        <button
          className={mode === "register" ? "active" : ""}
          onClick={() => onModeChange("register")}
          role="tab"
          aria-selected={mode === "register"}
          type="button"
        >
          Регистрация
        </button>
      </div>

      <div className="auth-copy">
        <span className="eyebrow">Личный кабинет</span>
        <h2 id="auth-title">
          {mode === "login" ? "С возвращением" : "Начнём знакомство"}
        </h2>
        <p>
          {mode === "login"
            ? "Войдите, чтобы управлять финансами."
            : "Создайте аккаунт — это займёт меньше минуты."}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="auth-form">
        {mode === "register" && (
          <>
            <label>
              <span>Имя и фамилия</span>
              <input
                autoComplete="name"
                minLength={1}
                maxLength={200}
                onChange={(event) => setFullName(event.target.value)}
                placeholder="Алексей Иванов"
                required
                value={fullName}
              />
            </label>
            <label>
              <span>Номер телефона</span>
              <input
                autoComplete="tel"
                inputMode="tel"
                onChange={(event) => setPhoneNumber(event.target.value)}
                placeholder="+7 999 123-45-67"
                required
                value={phoneNumber}
              />
            </label>
          </>
        )}

        <label>
          <span>Электронная почта</span>
          <input
            autoComplete="email"
            onChange={(event) => setEmail(event.target.value)}
            placeholder="name@example.com"
            ref={emailRef}
            required
            type="email"
            value={email}
          />
        </label>

        <label>
          <span>Пароль</span>
          <span className="password-field">
            <input
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              minLength={8}
              maxLength={128}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Не менее 8 символов"
              required
              type={showPassword ? "text" : "password"}
              value={password}
            />
            <button
              aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
              onClick={() => setShowPassword((visible) => !visible)}
              type="button"
            >
              {showPassword ? "Скрыть" : "Показать"}
            </button>
          </span>
        </label>

        {error && <p className="form-error" role="alert">{error}</p>}

        <button className="submit-button" disabled={loading} type="submit">
          <span>
            {loading
              ? "Подождите…"
              : mode === "login"
                ? "Войти в CoreBank"
                : "Создать аккаунт"}
          </span>
          {!loading && <ArrowIcon />}
        </button>
      </form>

      <p className="security-note">
        <span aria-hidden="true">✓</span> Пароль не хранится в открытом виде
      </p>
    </section>
  );
}

function UserPanel({
  user,
  onLogout,
  onDashboard,
}: {
  user: User;
  onLogout: () => void;
  onDashboard: () => void;
}) {
  return (
    <section className="auth-card user-card" id="auth" aria-labelledby="user-title">
      <div className="user-avatar" aria-hidden="true">
        {user.full_name.trim().charAt(0).toUpperCase()}
      </div>
      <span className="status-pill"><i /> Вы вошли</span>
      <h2 id="user-title">Здравствуйте, {user.full_name.split(" ")[0]}</h2>
      <p>{user.email}</p>
      <button className="submit-button" type="button" onClick={onDashboard}>
        <span>Перейти в кабинет</span>
        <ArrowIcon />
      </button>
      <button className="logout-button" onClick={onLogout} type="button">
        Выйти из аккаунта
      </button>
    </section>
  );
}

export default function App() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<AuthMode>("login");
  const [user, setUser] = useState<User | null>(null);
  const [sessionLoading, setSessionLoading] = useState(true);

  useEffect(() => {
    const token = getToken();

    if (!token) {
      setSessionLoading(false);
      return;
    }

    getCurrentUser(token)
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setSessionLoading(false));
  }, []);

  function openAuth(nextMode: AuthMode) {
    setMode(nextMode);
    document.getElementById("auth")?.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
    setMode("login");
    navigate("/");
  }, [navigate]);

  function handleAuthenticated(authenticatedUser: User) {
    setUser(authenticatedUser);
    navigate("/dashboard");
  }

  return (
    <Routes>
      <Route path="/" element={<main>
      <header className="site-header">
        <a className="brand" href="#top" aria-label="CoreBank, на главную">
          <span className="brand-mark"><i /><i /></span>
          <span>CoreBank</span>
        </a>

        <nav aria-label="Основная навигация">
          <a href="#benefits">Возможности</a>
          <a href="#about">О банке</a>
        </nav>

        {!user ? (
          <button className="header-login" onClick={() => openAuth("login")} type="button">
            Войти <ArrowIcon />
          </button>
        ) : (
          <button className="header-login" onClick={() => navigate("/dashboard")} type="button">
            Кабинет <ArrowIcon />
          </button>
        )}
      </header>

      <section className="hero" id="top">
        <div className="hero-content">
          <div className="hero-badge"><SparkIcon /> Финансы без лишнего шума</div>
          <h1>Банк, который <em>движется</em> с вами</h1>
          <p className="hero-lead">
            Переводы, счета и карты — просто, прозрачно и всегда под рукой.
          </p>
          <div className="hero-actions">
            <button className="primary-action" onClick={() => openAuth("register")} type="button">
              Стать клиентом <ArrowIcon />
            </button>
            <a href="#benefits">Узнать больше</a>
          </div>

          <div className="trust-row" aria-label="Преимущества">
            <span><b>24/7</b> доступ к финансам</span>
            <span><b>0 ₽</b> за обслуживание</span>
            <span><b>1 мин</b> на регистрацию</span>
          </div>
        </div>

        <div className="hero-panel-wrap">
          <div className="decorative-orbit orbit-one" />
          <div className="decorative-orbit orbit-two" />
          {sessionLoading ? (
            <section className="auth-card loading-card" aria-label="Загрузка сессии">
              <div className="loader" />
              <p>Проверяем сессию…</p>
            </section>
          ) : user ? (
            <UserPanel user={user} onLogout={logout} onDashboard={() => navigate("/dashboard")} />
          ) : (
            <AuthPanel mode={mode} onModeChange={setMode} onAuthenticated={handleAuthenticated} />
          )}
        </div>
      </section>

      <section className="benefits" id="benefits">
        <article>
          <span>01</span>
          <h3>Всё важное рядом</h3>
          <p>Баланс, карты и история операций в одном спокойном интерфейсе.</p>
        </article>
        <article>
          <span>02</span>
          <h3>Переводы без суеты</h3>
          <p>Понятный сценарий перевода и прозрачный статус каждой операции.</p>
        </article>
        <article id="about">
          <span>03</span>
          <h3>Безопасность по умолчанию</h3>
          <p>Защищённая авторизация и внимательное отношение к вашим данным.</p>
        </article>
      </section>
      </main>} />
      <Route
        path="/dashboard"
        element={
          sessionLoading ? (
            <div className="dashboard-loading"><div className="loader" /><span>Проверяем сессию…</span></div>
          ) : user ? (
            <Dashboard user={user} onLogout={logout} onUserUpdated={setUser} />
          ) : (
            <Navigate to="/" replace />
          )
        }
      />
      <Route path="*" element={<Navigate to={user ? "/dashboard" : "/"} replace />} />
    </Routes>
  );
}
