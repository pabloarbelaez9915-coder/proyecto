from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Membresia


class MembresiaCrud:
    _membresias: Dict[str, Membresia] = {}

    @classmethod
    def create(cls, membresia: Membresia) -> Membresia:
        cls._membresias[str(membresia.id_membresia)] = membresia
        return membresia

    @classmethod
    def get_by_id(cls, id_membresia: Union[str, UUID]) -> Optional[Membresia]:
        return cls._membresias.get(str(id_membresia))

    @classmethod
    def get_all(cls) -> List[Membresia]:
        return list(cls._membresias.values())

    @classmethod
    def update(
        cls, id_membresia: Union[str, UUID], nuevos_datos: dict
    ) -> Optional[Membresia]:
        membresia = cls.get_by_id(id_membresia)
        if membresia is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(membresia, key):
                setattr(membresia, key, value)
        return membresia

    @classmethod
    def delete(cls, id_membresia: Union[str, UUID]) -> bool:
        return cls._membresias.pop(str(id_membresia), None) is not None
