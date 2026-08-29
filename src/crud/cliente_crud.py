from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from src.entities import Cliente


class ClienteCrud:
    _clientes: Dict[str, Cliente] = {}

    @classmethod
    def create(cls, cliente: Cliente) -> Cliente:
        cls._clientes[str(cliente.id_cliente)] = cliente
        return cliente

    @classmethod
    def get_by_id(cls, id_cliente: Union[str, UUID]) -> Optional[Cliente]:
        return cls._clientes.get(str(id_cliente))

    @classmethod
    def get_all(cls) -> List[Cliente]:
        return list(cls._clientes.values())

    @classmethod
    def update(
        cls, id_cliente: Union[str, UUID], nuevos_datos: dict
    ) -> Optional[Cliente]:
        cliente = cls.get_by_id(id_cliente)
        if cliente is None:
            return None
        for key, value in nuevos_datos.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)
        return cliente

    @classmethod
    def delete(cls, id_cliente: Union[str, UUID]) -> bool:
        return cls._clientes.pop(str(id_cliente), None) is not None
