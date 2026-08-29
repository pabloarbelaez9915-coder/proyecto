from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Equipo


class EquipoCrud:
    _equipos: Dict[str, Equipo] = {}

    @classmethod
    def create(cls, equipo: Equipo) -> Equipo:
        cls._equipos[str(equipo.id_equipo)] = equipo
        return equipo

    @classmethod
    def get_by_id(cls, id_equipo: Union[str, UUID]) -> Optional[Equipo]:
        return cls._equipos.get(str(id_equipo))

    @classmethod
    def get_all(cls) -> List[Equipo]:
        return list(cls._equipos.values())

    @classmethod
    def update(
        cls, id_equipo: Union[str, UUID], nuevos_datos: dict
    ) -> Optional[Equipo]:
        equipo = cls.get_by_id(id_equipo)
        if equipo is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(equipo, key):
                setattr(equipo, key, value)
        return equipo

    @classmethod
    def delete(cls, id_equipo: Union[str, UUID]) -> bool:
        return cls._equipos.pop(str(id_equipo), None) is not None
