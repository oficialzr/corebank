from corebank_api.database import models
from corebank_api.database.session import Base, engine


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("database tables created")


if __name__ == "__main__":
    main()
