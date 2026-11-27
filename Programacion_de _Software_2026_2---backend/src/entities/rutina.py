from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Rutina:
    # PK: clave primaria
    id_rutina: UUID = field(default_factory=uuid4)

    # Datos de la rutina
    nombre: str = ""
    descripcion: Optional[str] = None
    duracion_minutos: int = 0
    nivel: Optional[str] = None
    objetivo: Optional[str] = None

    # FK: clave foránea, puede ser null
    id_cliente: Optional[UUID] = None
    id_entrenador: Optional[UUID] = None

    # Campos con valor por defecto y nulos
    fecha_registro: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la rutina es obligatorio.")
        if self.duracion_minutos <= 0:
            raise ValueError("La duración en minutos debe ser mayor que cero.")

    def actualizar(
        self,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        duracion_minutos: Optional[int] = None,
        nivel: Optional[str] = None,
        objetivo: Optional[str] = None,
        id_cliente: Optional[UUID] = None,
        id_entrenador: Optional[UUID] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")
            self.nombre = nombre.strip()

        if descripcion is not None:
            self.descripcion = descripcion.strip() if descripcion.strip() else None

        if duracion_minutos is not None:
            if duracion_minutos <= 0:
                raise ValueError("La duración en minutos debe ser mayor que cero.")
            self.duracion_minutos = duracion_minutos

        if nivel is not None:
            self.nivel = nivel.strip() if nivel.strip() else None

        if objetivo is not None:
            self.objetivo = objetivo.strip() if objetivo.strip() else None

        if id_cliente is not None:
            self.id_cliente = id_cliente

        if id_entrenador is not None:
            self.id_entrenador = id_entrenador

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Rutina(id_rutina={self.id_rutina}, nombre={self.nombre}, "
            f"duracion_minutos={self.duracion_minutos}, cliente={self.id_cliente}, "
            f"entrenador={self.id_entrenador})"
        )
