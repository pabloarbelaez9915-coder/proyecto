from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.config import SessionLocal, engine
from src.database.models import Base


def create_all_tables() -> None:
    Base.metadata.create_all(bind=engine)


def reset_database() -> None:
    with Session(engine) as session:
        session.execute(text("PRAGMA foreign_keys = OFF"))
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(text(f'DELETE FROM "{table.name}"'))
        session.execute(text("PRAGMA foreign_keys = ON"))
        session.commit()


def get_session() -> Session:
    return SessionLocal()


if __name__ == "__main__":
    create_all_tables()
    print("Tablas creadas correctamente.")
