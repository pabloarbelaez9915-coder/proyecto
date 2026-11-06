from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Entrenador:
    # PK: clave primaria
    id_entrenador: UUID = field(default_factory=uuid4)

    # Datos del entrenador
    primer_nombre: str = ""
    segundo_nombre: Optional[str] = None
    primer_apellido: str = ""
    segundo_apellido: Optional[str] = None
    correo: str = ""
    telefono: Optional[str] = None
    clave: str = ""

    # FK: clave foránea, puede ser null
    id_sede: Optional[UUID] = None

    # Campos con valor por defecto y nulos
    fecha_registro: date = field(default_factory=date.today)
    fecha_edicion: Optional[date] = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.primer_nombre or not self.primer_nombre.strip():
            raise ValueError("El primer nombre es obligatorio.")
        if not self.primer_apellido or not self.primer_apellido.strip():
            raise ValueError("El primer apellido es obligatorio.")
        if not self.correo or not self.correo.strip():
            raise ValueError("El correo es obligatorio.")
        if not self.clave or not self.clave.strip():
            raise ValueError("La clave es obligatoria.")

    def actualizar(
        self,
        primer_nombre: Optional[str] = None,
        segundo_nombre: Optional[str] = None,
        primer_apellido: Optional[str] = None,
        segundo_apellido: Optional[str] = None,
        correo: Optional[str] = None,
        telefono: Optional[str] = None,
        clave: Optional[str] = None,
        id_sede: Optional[UUID] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if primer_nombre is not None:
            if not primer_nombre.strip():
                raise ValueError("El primer nombre no puede estar vacío.")
            self.primer_nombre = primer_nombre.strip()

        if segundo_nombre is not None:
            self.segundo_nombre = (
                segundo_nombre.strip() if segundo_nombre.strip() else None
            )

        if primer_apellido is not None:
            if not primer_apellido.strip():
                raise ValueError("El primer apellido no puede estar vacío.")
            self.primer_apellido = primer_apellido.strip()

        if segundo_apellido is not None:
            self.segundo_apellido = (
                segundo_apellido.strip() if segundo_apellido.strip() else None
            )

        if correo is not None:
            if not correo.strip():
                raise ValueError("El correo no puede estar vacío.")
            self.correo = correo.strip()

        if telefono is not None:
            self.telefono = telefono.strip() if telefono.strip() else None

        if clave is not None:
            if not clave.strip():
                raise ValueError("La clave no puede estar vacía.")
            self.clave = clave.strip()

        if id_sede is not None:
            self.id_sede = id_sede

        if activo is not None:
            self.activo = activo

        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return (
            f"Entrenador(id_entrenador={self.id_entrenador}, "
            f"nombre={self.primer_nombre} {self.primer_apellido}, "
            f"correo={self.correo}, sede={self.id_sede})"
        )
