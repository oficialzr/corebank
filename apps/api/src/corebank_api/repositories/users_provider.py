from corebank_api.database.session import SessionLocal
from corebank_api.repositories import sql_users
from corebank_api.schemas.user import UserRecord


def get_user_by_email(email: str) -> UserRecord | None:
    with SessionLocal() as session:
        return sql_users.get_user_by_email(session, email)


def save_user(user: UserRecord) -> UserRecord:
    with SessionLocal() as session:
        return sql_users.save_user(session, user)
