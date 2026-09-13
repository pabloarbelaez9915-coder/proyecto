from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    nombre_usuario: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    clave: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class MembresiaModel(Base):
    __tablename__ = "membresias"

    id_membresia: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500))
    fecha_inscripcion: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    clientes: Mapped[list[ClienteModel]] = relationship(back_populates="membresia")
    pagos: Mapped[list[PagoModel]] = relationship(back_populates="membresia")


class SedeModel(Base):
    __tablename__ = "sedes"

    id_sede: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    direccion: Mapped[str] = mapped_column(String(250), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(30))
    ciudad: Mapped[Optional[str]] = mapped_column(String(100))
    descripcion: Mapped[Optional[str]] = mapped_column(String(500))
    fecha_registro: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    entrenadores: Mapped[list[EntrenadorModel]] = relationship(back_populates="sede")
    clases: Mapped[list[ClaseModel]] = relationship(back_populates="sede")
    equipos: Mapped[list[EquipoModel]] = relationship(back_populates="sede")


class ClienteModel(Base):
    __tablename__ = "clientes"

    id_cliente: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    primer_nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_nombre: Mapped[Optional[str]] = mapped_column(String(100))
    primer_apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_apellido: Mapped[Optional[str]] = mapped_column(String(100))
    correo: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(30))
    clave: Mapped[str] = mapped_column(String(255), nullable=False)
    id_membresia: Mapped[Optional[str]] = mapped_column(
        ForeignKey("membresias.id_membresia")
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    membresia: Mapped[Optional[MembresiaModel]] = relationship(
        back_populates="clientes"
    )
    rutinas: Mapped[list[RutinaModel]] = relationship(back_populates="cliente")
    asistencias: Mapped[list[AsistenciaModel]] = relationship(back_populates="cliente")
    pagos: Mapped[list[PagoModel]] = relationship(back_populates="cliente")


class EntrenadorModel(Base):
    __tablename__ = "entrenadores"

    id_entrenador: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    primer_nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_nombre: Mapped[Optional[str]] = mapped_column(String(100))
    primer_apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_apellido: Mapped[Optional[str]] = mapped_column(String(100))
    correo: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(30))
    clave: Mapped[str] = mapped_column(String(255), nullable=False)
    id_sede: Mapped[Optional[str]] = mapped_column(ForeignKey("sedes.id_sede"))
    fecha_registro: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    sede: Mapped[Optional[SedeModel]] = relationship(back_populates="entrenadores")
    clases: Mapped[list[ClaseModel]] = relationship(back_populates="entrenador")
    rutinas: Mapped[list[RutinaModel]] = relationship(back_populates="entrenador")


class ClaseModel(Base):
    __tablename__ = "clases"

    id_clase: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500))
    capacidad_maxima: Mapped[int] = mapped_column(Integer, nullable=False)
    horario: Mapped[Optional[str]] = mapped_column(String(80))
    nivel: Mapped[Optional[str]] = mapped_column(String(50))
    id_entrenador: Mapped[Optional[str]] = mapped_column(
        ForeignKey("entrenadores.id_entrenador")
    )
    id_sede: Mapped[Optional[str]] = mapped_column(ForeignKey("sedes.id_sede"))
    fecha_registro: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    entrenador: Mapped[Optional[EntrenadorModel]] = relationship(
        back_populates="clases"
    )
    sede: Mapped[Optional[SedeModel]] = relationship(back_populates="clases")
    asistencias: Mapped[list[AsistenciaModel]] = relationship(back_populates="clase")


class RutinaModel(Base):
    __tablename__ = "rutinas"

    id_rutina: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500))
    duracion_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    nivel: Mapped[Optional[str]] = mapped_column(String(50))
    objetivo: Mapped[Optional[str]] = mapped_column(String(200))
    id_cliente: Mapped[Optional[str]] = mapped_column(ForeignKey("clientes.id_cliente"))
    id_entrenador: Mapped[Optional[str]] = mapped_column(
        ForeignKey("entrenadores.id_entrenador")
    )
    fecha_registro: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cliente: Mapped[Optional[ClienteModel]] = relationship(back_populates="rutinas")
    entrenador: Mapped[Optional[EntrenadorModel]] = relationship(
        back_populates="rutinas"
    )


class EquipoModel(Base):
    __tablename__ = "equipos"

    id_equipo: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500))
    categoria: Mapped[Optional[str]] = mapped_column(String(100))
    estado: Mapped[Optional[str]] = mapped_column(String(50))
    id_sede: Mapped[Optional[str]] = mapped_column(ForeignKey("sedes.id_sede"))
    fecha_registro: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    sede: Mapped[Optional[SedeModel]] = relationship(back_populates="equipos")


class AsistenciaModel(Base):
    __tablename__ = "asistencias"

    id_asistencia: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    fecha: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    hora_entrada: Mapped[Optional[datetime]] = mapped_column(DateTime)
    hora_salida: Mapped[Optional[datetime]] = mapped_column(DateTime)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    id_cliente: Mapped[Optional[str]] = mapped_column(ForeignKey("clientes.id_cliente"))
    id_clase: Mapped[Optional[str]] = mapped_column(ForeignKey("clases.id_clase"))
    fecha_registro: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cliente: Mapped[Optional[ClienteModel]] = relationship(back_populates="asistencias")
    clase: Mapped[Optional[ClaseModel]] = relationship(back_populates="asistencias")


class PagoModel(Base):
    __tablename__ = "pagos"

    id_pago: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    metodo_pago: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_pago: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    id_cliente: Mapped[Optional[str]] = mapped_column(ForeignKey("clientes.id_cliente"))
    id_membresia: Mapped[Optional[str]] = mapped_column(
        ForeignKey("membresias.id_membresia")
    )
    fecha_registro: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cliente: Mapped[Optional[ClienteModel]] = relationship(back_populates="pagos")
    membresia: Mapped[Optional[MembresiaModel]] = relationship(back_populates="pagos")


__all__ = [
    "Base",
    "UsuarioModel",
    "MembresiaModel",
    "SedeModel",
    "ClienteModel",
    "EntrenadorModel",
    "ClaseModel",
    "RutinaModel",
    "EquipoModel",
    "AsistenciaModel",
    "PagoModel",
]
