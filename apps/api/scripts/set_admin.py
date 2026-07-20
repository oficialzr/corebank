import argparse

from corebank_api.database.models import UserModel
from corebank_api.database.session import SessionLocal


def main() -> None:
    parser = argparse.ArgumentParser(description="Grant or revoke CoreBank admin access")
    parser.add_argument("email")
    parser.add_argument("--revoke", action="store_true")
    args = parser.parse_args()

    with SessionLocal() as session:
        user = session.query(UserModel).filter(UserModel.email == args.email.lower()).one_or_none()
        if user is None:
            parser.error(f"user not found: {args.email}")
        user.is_admin = not args.revoke
        session.commit()
        action = "revoked from" if args.revoke else "granted to"
        print(f"Admin access {action} {user.email}")


if __name__ == "__main__":
    main()
