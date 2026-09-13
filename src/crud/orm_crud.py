from __future__ import annotations

from typing import Any, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class PersistentCrud:
    model: type[ModelType]
    id_field: str

    @classmethod
    def create(cls, session: Session, data: ModelType | Any) -> ModelType:
        if isinstance(data, cls.model):
            item = data
        else:
            fields = {column.name for column in cls.model.__table__.columns}
            values = {key: value for key, value in vars(data).items() if key in fields}
            for key, value in values.items():
                if isinstance(value, UUID):
                    values[key] = str(value)
            item = cls.model(**values)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    @classmethod
    def get_by_id(cls, session: Session, identifier: str | UUID) -> ModelType | None:
        value = str(identifier)
        item = session.scalar(
            select(cls.model).where(getattr(cls.model, cls.id_field) == value)
        )
        session.commit()
        return item

    @classmethod
    def get_all(cls, session: Session) -> list[ModelType]:
        items = list(session.scalars(select(cls.model)).all())
        session.commit()
        return items

    @classmethod
    def update(
        cls, session: Session, identifier: str | UUID, nuevos_datos: dict
    ) -> ModelType | None:
        item = cls.get_by_id(session, identifier)
        if item is None:
            return None
        fields = {column.name for column in cls.model.__table__.columns}
        for key, value in nuevos_datos.items():
            if key in fields and key != cls.id_field:
                setattr(item, key, str(value) if isinstance(value, UUID) else value)
        session.commit()
        session.refresh(item)
        return item

    @classmethod
    def delete(cls, session: Session, identifier: str | UUID) -> bool:
        item = cls.get_by_id(session, identifier)
        if item is None:
            return False
        session.delete(item)
        session.commit()
        return True
