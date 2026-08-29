from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Asistencia


class AsistenciaCrud:
    _asistencias: Dict[str, Asistencia] = {}

    @classmethod
    def create(cls, asistencia: Asistencia) -> Asistencia:
        cls._asistencias[str(asistencia.id_asistencia)] = asistencia
        return asistencia

    @classmethod
    def get_by_id(cls, id_asistencia: Union[str, UUID]) -> Optional[Asistencia]:
        return cls._asistencias.get(str(id_asistencia))

    @classmethod
    def get_all(cls) -> List[Asistencia]:
        return list(cls._asistencias.values())

    @classmethod
    def update(
        cls, id_asistencia: Union[str, UUID], nuevos_datos: dict
    ) -> Optional[Asistencia]:
        asistencia = cls.get_by_id(id_asistencia)
        if asistencia is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(asistencia, key):
                setattr(asistencia, key, value)
        return asistencia

    @classmethod
    def delete(cls, id_asistencia: Union[str, UUID]) -> bool:
        return cls._asistencias.pop(str(id_asistencia), None) is not None
