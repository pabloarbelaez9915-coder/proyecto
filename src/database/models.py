from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Sede(Base):
    __tablename__ = "sedes"

    id_sede: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ciudad: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    entrenadores: Mapped[list["Entrenador"]] = relationship(back_populates="sede")
    clases: Mapped[list["Clase"]] = relationship(back_populates="sede")
    equipos: Mapped[list["Equipo"]] = relationship(back_populates="sede")


class Membresia(Base):
    __tablename__ = "membresias"

    id_membresia: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    fecha_inscripcion: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    clientes: Mapped[list["Cliente"]] = relationship(back_populates="membresia")
    pagos: Mapped[list["Pago"]] = relationship(back_populates="membresia")


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    primer_nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_nombre: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    primer_apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_apellido: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    correo: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    clave: Mapped[str] = mapped_column(String(255), nullable=False)
    id_membresia: Mapped[Optional[str]] = mapped_column(ForeignKey("membresias.id_membresia"), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    membresia: Mapped[Optional[Membresia]] = relationship(back_populates="clientes")
    pagos: Mapped[list["Pago"]] = relationship(back_populates="cliente")
    asistencias: Mapped[list["Asistencia"]] = relationship(back_populates="cliente")
    rutinas: Mapped[list["Rutina"]] = relationship(back_populates="cliente")


class Entrenador(Base):
    __tablename__ = "entrenadores"

    id_entrenador: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    primer_nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_nombre: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    primer_apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_apellido: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    correo: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    clave: Mapped[str] = mapped_column(String(255), nullable=False)
    id_sede: Mapped[Optional[str]] = mapped_column(ForeignKey("sedes.id_sede"), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    sede: Mapped[Optional[Sede]] = relationship(back_populates="entrenadores")
    clases: Mapped[list["Clase"]] = relationship(back_populates="entrenador")
    rutinas: Mapped[list["Rutina"]] = relationship(back_populates="entrenador")


class Clase(Base):
    __tablename__ = "clases"

    id_clase: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    capacidad_maxima: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    horario: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    nivel: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    id_entrenador: Mapped[Optional[str]] = mapped_column(ForeignKey("entrenadores.id_entrenador"), nullable=True)
    id_sede: Mapped[Optional[str]] = mapped_column(ForeignKey("sedes.id_sede"), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    entrenador: Mapped[Optional[Entrenador]] = relationship(back_populates="clases")
    sede: Mapped[Optional[Sede]] = relationship(back_populates="clases")
    asistencias: Mapped[list["Asistencia"]] = relationship(back_populates="clase")


class Rutina(Base):
    __tablename__ = "rutinas"

    id_rutina: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duracion_minutos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nivel: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    objetivo: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    id_cliente: Mapped[Optional[str]] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=True)
    id_entrenador: Mapped[Optional[str]] = mapped_column(ForeignKey("entrenadores.id_entrenador"), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cliente: Mapped[Optional[Cliente]] = relationship(back_populates="rutinas")
    entrenador: Mapped[Optional[Entrenador]] = relationship(back_populates="rutinas")


class Equipo(Base):
    __tablename__ = "equipos"

    id_equipo: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    categoria: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    estado: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    id_sede: Mapped[Optional[str]] = mapped_column(ForeignKey("sedes.id_sede"), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    sede: Mapped[Optional[Sede]] = relationship(back_populates="equipos")


class Asistencia(Base):
    __tablename__ = "asistencias"

    id_asistencia: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fecha: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    hora_entrada: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    hora_salida: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    id_cliente: Mapped[Optional[str]] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=True)
    id_clase: Mapped[Optional[str]] = mapped_column(ForeignKey("clases.id_clase"), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cliente: Mapped[Optional[Cliente]] = relationship(back_populates="asistencias")
    clase: Mapped[Optional[Clase]] = relationship(back_populates="asistencias")


class Pago(Base):
    __tablename__ = "pagos"

    id_pago: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    monto: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    metodo_pago: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_pago: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    id_cliente: Mapped[Optional[str]] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=True)
    id_membresia: Mapped[Optional[str]] = mapped_column(ForeignKey("membresias.id_membresia"), nullable=True)
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    fecha_edicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cliente: Mapped[Optional[Cliente]] = relationship(back_populates="pagos")
    membresia: Mapped[Optional[Membresia]] = relationship(back_populates="pagos")
