from corebank_api.database.session import SessionLocal
from corebank_api.repositories import sql_users
from corebank_api.schemas.user import UserRecord


def get_user_by_email(email: str) -> UserRecord | None:
    with SessionLocal() as session:
        return sql_users.get_user_by_email(session, email)


def get_user_by_phone_number(phone_number: str) -> UserRecord | None:
    with SessionLocal() as session:
        return sql_users.get_user_by_phone_number(session, phone_number)


def save_user(user: UserRecord) -> UserRecord:
    with SessionLocal() as session:
        return sql_users.save_user(session, user)


def update_user_phone_number(user_id: str, phone_number: str) -> UserRecord:
    with SessionLocal() as session:
        return sql_users.update_user_phone_number(session, user_id, phone_number)
