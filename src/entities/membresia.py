from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Membresia:
    # PK: clave primaria
    id_membresia: UUID = field(default_factory=uuid4)

    # Datos de la membresía
    nombre: str = ""
    precio: float = 0.0
    descripcion: Optional[str] = None

    # Campos con valor por defecto y nulos
    fecha_inscripcion: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la membresía es obligatorio.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")

    def actualizar(
        self,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        precio: Optional[float] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")
            self.nombre = nombre.strip()

        if descripcion is not None:
            self.descripcion = descripcion.strip() if descripcion.strip() else None

        if precio is not None:
            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            self.precio = precio

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Membresia(id_membresia={self.id_membresia}, nombre={self.nombre}, "
            f"precio={self.precio}, activo={self.activo})"
        )
