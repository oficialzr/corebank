from sqlalchemy.orm import Session

from corebank_api.database.models import UserModel
from corebank_api.schemas.user import UserRecord


def model_to_schema(user: UserModel) -> UserRecord:
    return UserRecord(
        id=user.id,
        email=user.email,
        password_hash=user.password_hash,
        full_name=user.full_name,
        phone_number=user.phone_number,
        is_active=user.is_active,
        created_at=user.created_at,
    )


def get_user_by_email(session: Session, email: str) -> UserRecord | None:
    user = session.query(UserModel).filter(UserModel.email == email).one_or_none()

    if user is None:
        return None

    return model_to_schema(user)


def get_user_by_phone_number(session: Session, phone_number: str) -> UserRecord | None:
    user = session.query(UserModel).filter(UserModel.phone_number == phone_number).one_or_none()

    if user is None:
        return None

    return model_to_schema(user)


def save_user(session: Session, user: UserRecord) -> UserRecord:
    user_model = UserModel(**user.model_dump())

    session.add(user_model)
    session.commit()
    session.refresh(user_model)

    return model_to_schema(user_model)


def update_user_phone_number(session: Session, user_id: str, phone_number: str) -> UserRecord:
    user = session.query(UserModel).filter(UserModel.id == user_id).one()
    user.phone_number = phone_number
    session.commit()
    session.refresh(user)
    return model_to_schema(user)
