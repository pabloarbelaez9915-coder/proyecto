from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Equipo:
    # PK: clave primaria
    id_equipo: UUID = field(default_factory=uuid4)

    # Datos del equipo
    nombre: str = ""
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None

    # FK: clave foránea, puede ser null
    id_sede: Optional[UUID] = None

    # Campos con valor por defecto y nulos
    fecha_registro: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del equipo es obligatorio.")

    def actualizar(
        self,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        categoria: Optional[str] = None,
        estado: Optional[str] = None,
        id_sede: Optional[UUID] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")
            self.nombre = nombre.strip()

        if descripcion is not None:
            self.descripcion = descripcion.strip() if descripcion.strip() else None

        if categoria is not None:
            self.categoria = categoria.strip() if categoria.strip() else None

        if estado is not None:
            self.estado = estado.strip() if estado.strip() else None

        if id_sede is not None:
            self.id_sede = id_sede

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Equipo(id_equipo={self.id_equipo}, nombre={self.nombre}, "
            f"categoria={self.categoria}, sede={self.id_sede})"
        )
