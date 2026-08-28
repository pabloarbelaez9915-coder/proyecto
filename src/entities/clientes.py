from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Membresia:
    id_membresia: UUID = field(default_factory=uuid4)
    nombre: str = ""
    precio: float = 0.0
    fecha_inscripcion: date = field(default_factory=date.today)
    fecha_edicion: date | None = None

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la membresía es obligatorio.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.fecha_inscripcion is None:
            self.fecha_inscripcion = date.today()

    def actualizar(
        self, nombre: str | None = None, precio: float | None = None
    ) -> None:
        if nombre is not None:
            if not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")
            self.nombre = nombre.strip()
        if precio is not None:
            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            self.precio = precio
        self.fecha_edicion = date.today()

    def __str__(self) -> str:
        return f"Membresia({self.id_membresia}, nombre={self.nombre}, precio={self.precio})"


@dataclass
class Cliente:
    id_cliente: UUID = field(default_factory=uuid4)
    primer_nombre: str = ""
    segundo_nombre: str = ""
    primer_apellido: str = ""
    segundo_apellido: str = ""
    correo: str = ""
    telefono: str = ""
    clave: str = ""
    id_membresia: UUID | None = None
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
        primer_nombre: str | None = None,
        primer_apellido: str | None = None,
        correo: str | None = None,
        clave: str | None = None,
        id_membresia: UUID | None = None,
        activo: bool | None = None,
    ) -> None:
        if primer_nombre is not None:
            if not primer_nombre.strip():
                raise ValueError("El primer nombre no puede estar vacío.")
            self.primer_nombre = primer_nombre.strip()
        if primer_apellido is not None:
            if not primer_apellido.strip():
                raise ValueError("El primer apellido no puede estar vacío.")
            self.primer_apellido = primer_apellido.strip()
        if correo is not None:
            if not correo.strip():
                raise ValueError("El correo no puede estar vacío.")
            self.correo = correo.strip()
        if clave is not None:
            if not clave.strip():
                raise ValueError("La clave no puede estar vacía.")
            self.clave = clave.strip()
        if id_membresia is not None:
            self.id_membresia = id_membresia
        if activo is not None:
            self.activo = activo

    def __str__(self) -> str:
        estado = "Activo" if self.activo else "Inactivo"
        return (
            f"Cliente({self.id_cliente}, nombre={self.primer_nombre} {self.primer_apellido}, "
            f"correo={self.correo}, estado={estado})"
        )
