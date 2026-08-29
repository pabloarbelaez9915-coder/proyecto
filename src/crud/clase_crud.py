from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Clase


class ClaseCrud:
    _clases: Dict[str, Clase] = {}

    @classmethod
    def create(cls, clase: Clase) -> Clase:
        cls._clases[str(clase.id_clase)] = clase
        return clase

    @classmethod
    def get_by_id(cls, id_clase: Union[str, UUID]) -> Optional[Clase]:
        return cls._clases.get(str(id_clase))

    @classmethod
    def get_all(cls) -> List[Clase]:
        return list(cls._clases.values())

    @classmethod
    def update(cls, id_clase: Union[str, UUID], nuevos_datos: dict) -> Optional[Clase]:
        clase = cls.get_by_id(id_clase)
        if clase is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(clase, key):
                setattr(clase, key, value)
        return clase

    @classmethod
    def delete(cls, id_clase: Union[str, UUID]) -> bool:
        return cls._clases.pop(str(id_clase), None) is not None
