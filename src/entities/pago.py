from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Pago:
    # PK: clave primaria
    id_pago: UUID = field(default_factory=uuid4)

    # Datos del pago
    monto: float = 0.0
    metodo_pago: str = ""
    estado: str = ""
    fecha_pago: date = field(default_factory=date.today)

    # FK: claves foráneas, pueden ser null
    id_cliente: Optional[UUID] = None
    id_membresia: Optional[UUID] = None

    # Campos con valor por defecto y nulos
    fecha_registro: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if self.monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        if not self.metodo_pago or not self.metodo_pago.strip():
            raise ValueError("El método de pago es obligatorio.")
        if not self.estado or not self.estado.strip():
            raise ValueError("El estado del pago es obligatorio.")

    def actualizar(
        self,
        monto: Optional[float] = None,
        metodo_pago: Optional[str] = None,
        estado: Optional[str] = None,
        fecha_pago: Optional[date] = None,
        id_cliente: Optional[UUID] = None,
        id_membresia: Optional[UUID] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if monto is not None:
            if monto <= 0:
                raise ValueError("El monto debe ser mayor que cero.")
            self.monto = monto

        if metodo_pago is not None:
            if not metodo_pago.strip():
                raise ValueError("El método de pago no puede estar vacío.")
            self.metodo_pago = metodo_pago.strip()

        if estado is not None:
            if not estado.strip():
                raise ValueError("El estado no puede estar vacío.")
            self.estado = estado.strip()

        if fecha_pago is not None:
            self.fecha_pago = fecha_pago

        if id_cliente is not None:
            self.id_cliente = id_cliente

        if id_membresia is not None:
            self.id_membresia = id_membresia

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Pago(id_pago={self.id_pago}, monto={self.monto}, "
            f"metodo={self.metodo_pago}, estado={self.estado}, cliente={self.id_cliente})"
        )
