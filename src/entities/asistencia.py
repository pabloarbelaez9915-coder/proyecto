from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Asistencia:
    # PK: clave primaria
    id_asistencia: UUID = field(default_factory=uuid4)

    # Datos de asistencia
    fecha: date = field(default_factory=date.today)
    hora_entrada: Optional[datetime] = None
    hora_salida: Optional[datetime] = None
    estado: str = ""

    # FK: claves foráneas, pueden ser null
    id_cliente: Optional[UUID] = None
    id_clase: Optional[UUID] = None

    # Campos con valor por defecto y nulos
    fecha_registro: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.estado or not self.estado.strip():
            raise ValueError("El estado de asistencia es obligatorio.")

    def actualizar(
        self,
        fecha: Optional[date] = None,
        hora_entrada: Optional[datetime] = None,
        hora_salida: Optional[datetime] = None,
        estado: Optional[str] = None,
        id_cliente: Optional[UUID] = None,
        id_clase: Optional[UUID] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if fecha is not None:
            self.fecha = fecha

        if hora_entrada is not None:
            self.hora_entrada = hora_entrada

        if hora_salida is not None:
            self.hora_salida = hora_salida

        if estado is not None:
            if not estado.strip():
                raise ValueError("El estado no puede estar vacío.")
            self.estado = estado.strip()

        if id_cliente is not None:
            self.id_cliente = id_cliente

        if id_clase is not None:
            self.id_clase = id_clase

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Asistencia(id_asistencia={self.id_asistencia}, fecha={self.fecha}, "
            f"estado={self.estado}, cliente={self.id_cliente}, clase={self.id_clase})"
        )
