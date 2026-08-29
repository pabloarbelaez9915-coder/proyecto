from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Pago


class PagoCrud:
    _pagos: Dict[str, Pago] = {}

    @classmethod
    def create(cls, pago: Pago) -> Pago:
        cls._pagos[str(pago.id_pago)] = pago
        return pago

    @classmethod
    def get_by_id(cls, id_pago: Union[str, UUID]) -> Optional[Pago]:
        return cls._pagos.get(str(id_pago))

    @classmethod
    def get_all(cls) -> List[Pago]:
        return list(cls._pagos.values())

    @classmethod
    def update(cls, id_pago: Union[str, UUID], nuevos_datos: dict) -> Optional[Pago]:
        pago = cls.get_by_id(id_pago)
        if pago is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(pago, key):
                setattr(pago, key, value)
        return pago

    @classmethod
    def delete(cls, id_pago: Union[str, UUID]) -> bool:
        return cls._pagos.pop(str(id_pago), None) is not None
