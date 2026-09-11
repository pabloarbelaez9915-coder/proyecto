from __future__ import annotations

from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import (
    Asistencia,
    Clase,
    Cliente,
    Entrenador,
    Equipo,
    Membresia,
    Pago,
    Rutina,
    Sede,
)

T = TypeVar("T")


class CrudMixin:
    model: type[T]

    @staticmethod
    def create(session: Session, obj: T) -> T:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def get_all(cls, session: Session) -> list[T]:
        return session.scalars(select(cls.model)).all()

    @classmethod
    def get_by_id(cls, session: Session, obj_id: str) -> T | None:
        return session.get(cls.model, obj_id)

    @classmethod
    def update(cls, session: Session, obj_id: str, new_data: dict[str, Any]) -> T | None:
        obj = cls.get_by_id(session, obj_id)
        if obj is None:
            return None
        for key, value in new_data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def delete(cls, session: Session, obj_id: str) -> bool:
        obj = cls.get_by_id(session, obj_id)
        if obj is None:
            return False
        session.delete(obj)
        session.commit()
        return True


class SedeCrud(CrudMixin):
    model = Sede


class MembresiaCrud(CrudMixin):
    model = Membresia


class ClienteCrud(CrudMixin):
    model = Cliente


class EntrenadorCrud(CrudMixin):
    model = Entrenador


class ClaseCrud(CrudMixin):
    model = Clase


class RutinaCrud(CrudMixin):
    model = Rutina


class EquipoCrud(CrudMixin):
    model = Equipo


class AsistenciaCrud(CrudMixin):
    model = Asistencia


class PagoCrud(CrudMixin):
    model = Pago
