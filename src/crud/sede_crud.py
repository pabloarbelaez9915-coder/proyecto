from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Sede


class SedeCrud:
    _sedes: Dict[str, Sede] = {}

    @classmethod
    def create(cls, sede: Sede) -> Sede:
        cls._sedes[str(sede.id_sede)] = sede
        return sede

    @classmethod
    def get_by_id(cls, id_sede: Union[str, UUID]) -> Optional[Sede]:
        return cls._sedes.get(str(id_sede))

    @classmethod
    def get_all(cls) -> List[Sede]:
        return list(cls._sedes.values())

    @classmethod
    def update(cls, id_sede: Union[str, UUID], nuevos_datos: dict) -> Optional[Sede]:
        sede = cls.get_by_id(id_sede)
        if sede is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(sede, key):
                setattr(sede, key, value)
        return sede

    @classmethod
    def delete(cls, id_sede: Union[str, UUID]) -> bool:
        return cls._sedes.pop(str(id_sede), None) is not None
