from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Sede:
    # PK: clave primaria
    id_sede: UUID = field(default_factory=uuid4)

    # Datos de la sede
    nombre: str = ""
    direccion: str = ""
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    descripcion: Optional[str] = None

    # Campos con valor por defecto y nulos
    fecha_registro: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la sede es obligatorio.")
        if not self.direccion or not self.direccion.strip():
            raise ValueError("La dirección de la sede es obligatoria.")

    def actualizar(
        self,
        nombre: Optional[str] = None,
        direccion: Optional[str] = None,
        telefono: Optional[str] = None,
        ciudad: Optional[str] = None,
        descripcion: Optional[str] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")
            self.nombre = nombre.strip()

        if direccion is not None:
            if not direccion.strip():
                raise ValueError("La dirección no puede estar vacía.")
            self.direccion = direccion.strip()

        if telefono is not None:
            self.telefono = telefono.strip() if telefono.strip() else None

        if ciudad is not None:
            self.ciudad = ciudad.strip() if ciudad.strip() else None

        if descripcion is not None:
            self.descripcion = descripcion.strip() if descripcion.strip() else None

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Sede(id_sede={self.id_sede}, nombre={self.nombre}, direccion={self.direccion}, "
            f"ciudad={self.ciudad})"
        )
