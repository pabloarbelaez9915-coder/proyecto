from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Entrenador


class EntrenadorCrud:
    _entrenadores: Dict[str, Entrenador] = {}

    @classmethod
    def create(cls, entrenador: Entrenador) -> Entrenador:
        cls._entrenadores[str(entrenador.id_entrenador)] = entrenador
        return entrenador

    @classmethod
    def get_by_id(cls, id_entrenador: Union[str, UUID]) -> Optional[Entrenador]:
        return cls._entrenadores.get(str(id_entrenador))

    @classmethod
    def get_all(cls) -> List[Entrenador]:
        return list(cls._entrenadores.values())

    @classmethod
    def update(
        cls, id_entrenador: Union[str, UUID], nuevos_datos: dict
    ) -> Optional[Entrenador]:
        entrenador = cls.get_by_id(id_entrenador)
        if entrenador is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(entrenador, key):
                setattr(entrenador, key, value)
        return entrenador

    @classmethod
    def delete(cls, id_entrenador: Union[str, UUID]) -> bool:
        return cls._entrenadores.pop(str(id_entrenador), None) is not None
