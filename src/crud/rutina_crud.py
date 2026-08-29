from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Rutina


class RutinaCrud:
    _rutinas: Dict[str, Rutina] = {}

    @classmethod
    def create(cls, rutina: Rutina) -> Rutina:
        cls._rutinas[str(rutina.id_rutina)] = rutina
        return rutina

    @classmethod
    def get_by_id(cls, id_rutina: Union[str, UUID]) -> Optional[Rutina]:
        return cls._rutinas.get(str(id_rutina))

    @classmethod
    def get_all(cls) -> List[Rutina]:
        return list(cls._rutinas.values())

    @classmethod
    def update(
        cls, id_rutina: Union[str, UUID], nuevos_datos: dict
    ) -> Optional[Rutina]:
        rutina = cls.get_by_id(id_rutina)
        if rutina is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(rutina, key):
                setattr(rutina, key, value)
        return rutina

    @classmethod
    def delete(cls, id_rutina: Union[str, UUID]) -> bool:
        return cls._rutinas.pop(str(id_rutina), None) is not None
