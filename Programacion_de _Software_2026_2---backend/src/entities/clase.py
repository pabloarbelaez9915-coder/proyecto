from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Clase:
    # PK: clave primaria
    id_clase: UUID = field(default_factory=uuid4)

    # Datos de la clase
    nombre: str = ""
    descripcion: Optional[str] = None
    capacidad_maxima: int = 0
    horario: Optional[str] = None
    nivel: Optional[str] = None

    # FK: clave foránea, puede ser null
    id_entrenador: Optional[UUID] = None
    id_sede: Optional[UUID] = None

    # Campos con valor por defecto y nulos
    fecha_registro: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la clase es obligatorio.")
        if self.capacidad_maxima <= 0:
            raise ValueError("La capacidad máxima debe ser mayor que cero.")

    def actualizar(
        self,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        capacidad_maxima: Optional[int] = None,
        horario: Optional[str] = None,
        nivel: Optional[str] = None,
        id_entrenador: Optional[UUID] = None,
        id_sede: Optional[UUID] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")
            self.nombre = nombre.strip()

        if descripcion is not None:
            self.descripcion = descripcion.strip() if descripcion.strip() else None

        if capacidad_maxima is not None:
            if capacidad_maxima <= 0:
                raise ValueError("La capacidad máxima debe ser mayor que cero.")
            self.capacidad_maxima = capacidad_maxima

        if horario is not None:
            self.horario = horario.strip() if horario.strip() else None

        if nivel is not None:
            self.nivel = nivel.strip() if nivel.strip() else None

        if id_entrenador is not None:
            self.id_entrenador = id_entrenador

        if id_sede is not None:
            self.id_sede = id_sede

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Clase(id_clase={self.id_clase}, nombre={self.nombre}, "
            f"capacidad_maxima={self.capacidad_maxima}, entrenador={self.id_entrenador}, "
            f"sede={self.id_sede})"
        )
