from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.entities.clientes import Cliente, Membresia
else:
    from src.entities.clientes import Cliente, Membresia

from src.crud import (
    AsistenciaCrud,
    ClaseCrud,
    ClienteCrud,
    EntrenadorCrud,
    EquipoCrud,
    MembresiaCrud,
    PagoCrud,
    RutinaCrud,
    SedeCrud,
)
from src.database import SessionLocal, init_db
from src.models import (
    AsistenciaModel,
    ClaseModel,
    ClienteModel,
    EntrenadorModel,
    EquipoModel,
    MembresiaModel,
    PagoModel,
    RutinaModel,
    SedeModel,
    UsuarioModel,
)


@dataclass
class Sede:
    id_sede: UUID = field(default_factory=uuid4)
    nombre: str = ""
    direccion: str = ""
    telefono: str = ""
    ciudad: str = ""
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la sede es obligatorio.")
        if not self.direccion or not self.direccion.strip():
            raise ValueError("La dirección es obligatoria.")

    def actualizar(
        self,
        nombre: Optional[str] = None,
        direccion: Optional[str] = None,
        telefono: Optional[str] = None,
        ciudad: Optional[str] = None,
        activo: Optional[bool] = None,
    ) -> None:
        if nombre is not None:
            self.nombre = nombre.strip()
        if direccion is not None:
            self.direccion = direccion.strip()
        if telefono is not None:
            self.telefono = telefono.strip()
        if ciudad is not None:
            self.ciudad = ciudad.strip()
        if activo is not None:
            self.activo = activo

    def __str__(self) -> str:
        estado = "Activa" if self.activo else "Inactiva"
        return f"Sede({self.id_sede}, nombre={self.nombre}, ciudad={self.ciudad}, estado={estado})"


CLIENTES: List[Cliente] = []
MEMBRESIAS: List[Membresia] = []
SEDES: List[Sede] = []
DB_SESSION: Optional[Session] = None


def db_session() -> Session:
    if DB_SESSION is None:
        raise RuntimeError("La sesión de base de datos no está inicializada.")
    return DB_SESSION


def mostrar_titulo(titulo: str) -> None:
    print("\n" + "=" * 70)
    print(f"{titulo:^70}")
    print("=" * 70)


def crear_usuario() -> None:
    mostrar_titulo("REGISTRO DE USUARIO")
    usuario = input("Ingrese nombre de usuario: ").strip()
    clave = input("Ingrese contraseña: ").strip()
    if not usuario or not clave:
        print("Los campos no pueden estar vacíos.")
        return
    existente = db_session().scalar(
        select(UsuarioModel).where(UsuarioModel.nombre_usuario == usuario)
    )
    if existente is not None:
        print("Ese usuario ya existe.")
        return
    try:
        item = UsuarioModel(nombre_usuario=usuario, clave=clave)
        db_session().add(item)
        db_session().commit()
        print(f"Usuario '{item.nombre_usuario}' registrado correctamente.")
    except SQLAlchemyError as exc:
        db_session().rollback()
        print(f"No se pudo registrar el usuario: {exc.orig}")


def iniciar_sesion() -> Optional[str]:
    mostrar_titulo("LOGIN")
    usuario = input("Usuario: ").strip()
    clave = input("Clave: ").strip()
    item = db_session().scalar(
        select(UsuarioModel).where(
            UsuarioModel.nombre_usuario == usuario,
            UsuarioModel.activo.is_(True),
        )
    )
    if item is not None and item.clave == clave:
        print(f"Bienvenido, {usuario}.")
        return usuario
    print("Usuario o contraseña incorrectos.")
    return None


def _asegurar_usuario_admin() -> None:
    admin = db_session().scalar(
        select(UsuarioModel).where(UsuarioModel.nombre_usuario == "admin")
    )
    if admin is None:
        db_session().add(UsuarioModel(nombre_usuario="admin", clave="1234"))
        db_session().commit()


def _asegurar_usuario_admin() -> None:
    admin = db_session().scalar(
        select(UsuarioModel).where(UsuarioModel.nombre_usuario == "admin")
    )
    if admin is None:
        db_session().add(UsuarioModel(nombre_usuario="admin", clave="1234"))
        db_session().commit()


def crear_membresia() -> None:
    mostrar_titulo("CREAR MEMBRESIA")
    try:
        nombre = input("Nombre: ").strip()
        precio = float(input("Precio: ").strip() or 0)
        membresia = Membresia(
            nombre=nombre, precio=precio, fecha_inscripcion=date.today()
        )
        item = MembresiaCrud.create(
            db_session(),
            MembresiaModel(
                id_membresia=str(membresia.id_membresia),
                nombre=membresia.nombre,
                precio=Decimal(str(membresia.precio)),
                fecha_inscripcion=membresia.fecha_inscripcion,
            ),
        )
        print(f"Membresía creada: {item.id_membresia} | {item.nombre}")
    except ValueError as exc:
        print(f"Error: {exc}")
    except SQLAlchemyError as exc:
        db_session().rollback()
        print(f"No se pudo guardar la membresía: {exc.orig}")


def listar_membresias() -> None:
    mostrar_titulo("MEMBRESIAS")
    membresias = MembresiaCrud.get_all(db_session())
    if not membresias:
        print("No hay membresías registradas.")
        return
    for item in membresias:
        print(
            f"- {item.id_membresia} | {item.nombre} | ${item.precio} | Inscrita: {item.fecha_inscripcion}"
        )


def actualizar_membresia() -> None:
    listar_membresias()
    membresias = MembresiaCrud.get_all(db_session())
    if not membresias:
        return
    id_buscar = input("Ingrese el ID de la membresía a editar: ").strip()
    item = MembresiaCrud.get_by_id(db_session(), id_buscar)
    if item is not None:
        try:
            nuevo_nombre = (
                input(f"Nuevo nombre ({item.nombre}): ").strip() or item.nombre
            )
            nuevo_precio = input(f"Nuevo precio ({item.precio}): ").strip()
            validated = Membresia(
                id_membresia=UUID(item.id_membresia),
                nombre=nuevo_nombre,
                precio=float(nuevo_precio) if nuevo_precio else float(item.precio),
                fecha_inscripcion=item.fecha_inscripcion,
            )
            MembresiaCrud.update(
                db_session(),
                id_buscar,
                {
                    "nombre": validated.nombre,
                    "precio": Decimal(str(validated.precio)),
                    "fecha_edicion": date.today(),
                },
            )
            print("Membresía actualizada correctamente.")
            return
        except ValueError as exc:
            print(f"Error: {exc}")
            return
    print("No se encontró la membresía.")


def eliminar_membresia() -> None:
    listar_membresias()
    if not MembresiaCrud.get_all(db_session()):
        return
    id_buscar = input("Ingrese el ID de la membresía a eliminar: ").strip()
    if MembresiaCrud.delete(db_session(), id_buscar):
        print("Membresía eliminada.")
        return
    print("No se encontró la membresía.")


def crear_cliente() -> None:
    mostrar_titulo("CREAR CLIENTE")
    primer_nombre = input("Primer nombre: ").strip()
    segundo_nombre = input("Segundo nombre: ").strip()
    primer_apellido = input("Primer apellido: ").strip()
    segundo_apellido = input("Segundo apellido: ").strip()
    correo = input("Correo: ").strip()
    telefono = input("Teléfono: ").strip()
    clave = input("Clave: ").strip()

    try:
        cliente = Cliente(
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            correo=correo,
            telefono=telefono,
            clave=clave,
        )
        item = ClienteCrud.create(
            db_session(),
            ClienteModel(
                id_cliente=str(cliente.id_cliente),
                primer_nombre=cliente.primer_nombre,
                segundo_nombre=cliente.segundo_nombre or None,
                primer_apellido=cliente.primer_apellido,
                segundo_apellido=cliente.segundo_apellido or None,
                correo=cliente.correo,
                telefono=cliente.telefono or None,
                clave=cliente.clave,
                id_membresia=(
                    str(cliente.id_membresia) if cliente.id_membresia else None
                ),
            ),
        )
        print(
            f"Cliente creado: {item.id_cliente} | {item.primer_nombre} {item.primer_apellido}"
        )
    except ValueError as exc:
        print(f"Error: {exc}")


def listar_clientes() -> None:
    mostrar_titulo("CLIENTES")
    clientes = ClienteCrud.get_all(db_session())
    if not clientes:
        print("No hay clientes registrados.")
        return
    for item in clientes:
        membresia = item.membresia.nombre if item.membresia else "Sin membresía"
        print(
            f"- {item.id_cliente} | {item.primer_nombre} {item.primer_apellido} | {item.correo} | Membresía: {membresia}"
        )


def actualizar_cliente() -> None:
    listar_clientes()
    if not ClienteCrud.get_all(db_session()):
        return
    id_buscar = input("Ingrese el ID del cliente a editar: ").strip()
    item = ClienteCrud.get_by_id(db_session(), id_buscar)
    if item is not None:
        try:
            nuevo_nombre = (
                input(f"Nuevo primer nombre ({item.primer_nombre}): ").strip()
                or item.primer_nombre
            )
            nuevo_apellido = (
                input(f"Nuevo primer apellido ({item.primer_apellido}): ").strip()
                or item.primer_apellido
            )
            nuevo_correo = (
                input(f"Nuevo correo ({item.correo}): ").strip() or item.correo
            )
            nueva_clave = (
                input("Nueva clave (dejar vacío para mantener): ").strip() or item.clave
            )
            validated = Cliente(
                id_cliente=UUID(item.id_cliente),
                primer_nombre=nuevo_nombre,
                primer_apellido=nuevo_apellido,
                correo=nuevo_correo,
                clave=nueva_clave,
            )
            ClienteCrud.update(
                db_session(),
                id_buscar,
                {
                    "primer_nombre": validated.primer_nombre,
                    "primer_apellido": validated.primer_apellido,
                    "correo": validated.correo,
                    "clave": validated.clave,
                },
            )
            print("Cliente actualizado correctamente.")
            return
        except ValueError as exc:
            print(f"Error: {exc}")
            return
    print("No se encontró el cliente.")


def eliminar_cliente() -> None:
    listar_clientes()
    if not ClienteCrud.get_all(db_session()):
        return
    id_buscar = input("Ingrese el ID del cliente a eliminar: ").strip()
    if ClienteCrud.delete(db_session(), id_buscar):
        print("Cliente eliminado.")
        return
    print("No se encontró el cliente.")


def crear_sede() -> None:
    mostrar_titulo("CREAR SEDE")
    nombre = input("Nombre: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()
    ciudad = input("Ciudad: ").strip()
    try:
        sede = Sede(
            nombre=nombre, direccion=direccion, telefono=telefono, ciudad=ciudad
        )
        item = SedeCrud.create(
            db_session(),
            SedeModel(
                id_sede=str(sede.id_sede),
                nombre=sede.nombre,
                direccion=sede.direccion,
                telefono=sede.telefono or None,
                ciudad=sede.ciudad or None,
            ),
        )
        print(f"Sede creada: {item.id_sede} | {item.nombre}")
    except ValueError as exc:
        print(f"Error: {exc}")


def listar_sedes() -> None:
    mostrar_titulo("SEDES")
    sedes = SedeCrud.get_all(db_session())
    if not sedes:
        print("No hay sedes registradas.")
        return
    for item in sedes:
        print(
            f"- {item.id_sede} | {item.nombre} | {item.ciudad} | {item.direccion} | {item.telefono} | {'Activa' if item.activo else 'Inactiva'}"
        )


def actualizar_sede() -> None:
    listar_sedes()
    if not SedeCrud.get_all(db_session()):
        return
    id_buscar = input("Ingrese el ID de la sede a editar: ").strip()
    item = SedeCrud.get_by_id(db_session(), id_buscar)
    if item is not None:
        nombre = input(f"Nuevo nombre ({item.nombre}): ").strip() or item.nombre
        direccion = (
            input(f"Nueva dirección ({item.direccion}): ").strip() or item.direccion
        )
        telefono = (
            input(f"Nuevo teléfono ({item.telefono or ''}): ").strip() or item.telefono
        )
        ciudad = input(f"Nueva ciudad ({item.ciudad or ''}): ").strip() or item.ciudad
        activo = input("¿Está activa? (s/n): ").strip().lower()
        try:
            validated = Sede(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono or "",
                ciudad=ciudad or "",
            )
            SedeCrud.update(
                db_session(),
                id_buscar,
                {
                    "nombre": validated.nombre,
                    "direccion": validated.direccion,
                    "telefono": validated.telefono or None,
                    "ciudad": validated.ciudad or None,
                    "activo": activo != "n" if activo else item.activo,
                },
            )
            print("Sede actualizada correctamente.")
            return
        except ValueError as exc:
            print(f"Error: {exc}")
            return
    print("No se encontró la sede.")


def eliminar_sede() -> None:
    listar_sedes()
    if not SedeCrud.get_all(db_session()):
        return
    id_buscar = input("Ingrese el ID de la sede a eliminar: ").strip()
    if SedeCrud.delete(db_session(), id_buscar):
        print("Sede eliminada.")
        return
    print("No se encontró la sede.")


def _mostrar_registros(crud, label: str) -> list:
    registros = crud.get_all(db_session())
    mostrar_titulo(label)
    if not registros:
        print("No hay registros.")
        return []
    for registro in registros:
        valores = " | ".join(
            f"{column.name}={getattr(registro, column.name)}"
            for column in registro.__table__.columns
        )
        print(f"- {valores}")
    return registros


FOREIGN_KEY_CRUDS = {
    "id_cliente": (ClienteCrud, "cliente"),
    "id_entrenador": (EntrenadorCrud, "entrenador"),
    "id_sede": (SedeCrud, "sede"),
    "id_clase": (ClaseCrud, "clase"),
    "id_membresia": (MembresiaCrud, "membresía"),
}


def _validar_referencias(values: dict) -> None:
    for field_name, value in values.items():
        if value and field_name in FOREIGN_KEY_CRUDS:
            crud, label = FOREIGN_KEY_CRUDS[field_name]
            try:
                UUID(str(value))
            except (ValueError, TypeError, AttributeError) as exc:
                raise ValueError(
                    f"El ID de {label} debe ser un UUID válido de 36 caracteres. "
                    "Ingresa únicamente el valor, sin etiquetas como 'id_sede='."
                ) from exc
            if crud.get_by_id(db_session(), value) is None:
                raise ValueError(
                    f"El ID de {label} '{value}' no existe. "
                    "Consulta primero la opción Listar."
                )


def _crear_registro(
    crud, model, label: str, fields: list[tuple[str, str, object]]
) -> None:
    mostrar_titulo(f"CREAR {label}")
    values = {}
    try:
        for name, prompt, converter in fields:
            raw_value = input(f"{prompt}: ").strip()
            values[name] = converter(raw_value) if raw_value else None
        _validar_referencias(values)
        item = crud.create(db_session(), model(**values))
        print(f"Registro creado: {getattr(item, crud.id_field)}")
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}")
    except SQLAlchemyError as exc:
        db_session().rollback()
        print(f"No se pudo guardar el registro: {exc.orig}")


def _actualizar_registro(
    crud, label: str, fields: list[tuple[str, str, object]]
) -> None:
    registros = _mostrar_registros(crud, label)
    if not registros:
        return
    identifier = input("Ingrese el ID del registro a editar: ").strip()
    item = crud.get_by_id(db_session(), identifier)
    if item is None:
        print("No se encontró el registro.")
        return
    values = {}
    try:
        for name, prompt, converter in fields:
            current = getattr(item, name)
            raw_value = input(f"{prompt} ({current}): ").strip()
            if raw_value:
                values[name] = converter(raw_value)
        _validar_referencias(values)
        if values:
            crud.update(db_session(), identifier, values)
        print("Registro actualizado correctamente.")
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}")
    except SQLAlchemyError as exc:
        db_session().rollback()
        print(f"No se pudo actualizar el registro: {exc.orig}")


def _eliminar_registro(crud, label: str) -> None:
    registros = _mostrar_registros(crud, label)
    if not registros:
        return
    identifier = input("Ingrese el ID del registro a eliminar: ").strip()
    if crud.delete(db_session(), identifier):
        print("Registro eliminado correctamente.")
    else:
        print("No se encontró el registro.")


def _menu_entidad(
    crud, model, label: str, fields: list[tuple[str, str, object]]
) -> None:
    while True:
        mostrar_titulo(f"GESTIÓN DE {label}")
        print("1. Crear")
        print("2. Listar")
        print("3. Editar")
        print("4. Eliminar")
        print("5. Regresar")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            _crear_registro(crud, model, label, fields)
        elif opcion == "2":
            _mostrar_registros(crud, label)
        elif opcion == "3":
            _actualizar_registro(crud, label, fields)
        elif opcion == "4":
            _eliminar_registro(crud, label)
        elif opcion == "5":
            return
        else:
            print("Opción inválida.")


def menu_rutinas() -> None:
    fields = [
        ("nombre", "Nombre", str),
        ("descripcion", "Descripción", str),
        ("duracion_minutos", "Duración en minutos", int),
        ("nivel", "Nivel", str),
        ("objetivo", "Objetivo", str),
        ("id_cliente", "ID del cliente (opcional)", str),
        ("id_entrenador", "ID del entrenador (opcional)", str),
    ]
    _menu_entidad(RutinaCrud, RutinaModel, "RUTINAS", fields)


def menu_pagos() -> None:
    fields = [
        ("monto", "Monto", Decimal),
        ("metodo_pago", "Método de pago", str),
        ("estado", "Estado", str),
        ("id_cliente", "ID del cliente (opcional)", str),
        ("id_membresia", "ID de la membresía (opcional)", str),
    ]
    _menu_entidad(PagoCrud, PagoModel, "PAGOS", fields)


def menu_equipos() -> None:
    fields = [
        ("nombre", "Nombre", str),
        ("descripcion", "Descripción", str),
        ("categoria", "Categoría", str),
        ("estado", "Estado", str),
        ("id_sede", "ID de la sede (opcional)", str),
    ]
    _menu_entidad(EquipoCrud, EquipoModel, "EQUIPOS", fields)


def menu_entrenadores() -> None:
    fields = [
        ("primer_nombre", "Primer nombre", str),
        ("segundo_nombre", "Segundo nombre", str),
        ("primer_apellido", "Primer apellido", str),
        ("segundo_apellido", "Segundo apellido", str),
        ("correo", "Correo", str),
        ("telefono", "Teléfono", str),
        ("clave", "Clave", str),
        ("id_sede", "ID de la sede (opcional)", str),
    ]
    _menu_entidad(EntrenadorCrud, EntrenadorModel, "ENTRENADORES", fields)


def menu_clases() -> None:
    fields = [
        ("nombre", "Nombre", str),
        ("descripcion", "Descripción", str),
        ("capacidad_maxima", "Capacidad máxima", int),
        ("horario", "Horario", str),
        ("nivel", "Nivel", str),
        ("id_entrenador", "ID del entrenador (opcional)", str),
        ("id_sede", "ID de la sede (opcional)", str),
    ]
    _menu_entidad(ClaseCrud, ClaseModel, "CLASES", fields)


def menu_asistencias() -> None:
    fields = [
        ("estado", "Estado", str),
        ("id_cliente", "ID del cliente (opcional)", str),
        ("id_clase", "ID de la clase (opcional)", str),
    ]
    _menu_entidad(AsistenciaCrud, AsistenciaModel, "ASISTENCIAS", fields)


def menu_membresias() -> None:
    while True:
        mostrar_titulo("GESTIÓN DE MEMBRESIAS")
        print("1. Crear membresía")
        print("2. Listar membresías")
        print("3. Editar membresía")
        print("4. Eliminar membresía")
        print("5. Regresar")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            crear_membresia()
        elif opcion == "2":
            listar_membresias()
        elif opcion == "3":
            actualizar_membresia()
        elif opcion == "4":
            eliminar_membresia()
        elif opcion == "5":
            return
        else:
            print("Opción inválida.")


def menu_clientes() -> None:
    while True:
        mostrar_titulo("GESTIÓN DE CLIENTES")
        print("1. Crear cliente")
        print("2. Listar clientes")
        print("3. Editar cliente")
        print("4. Eliminar cliente")
        print("5. Regresar")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            actualizar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            return
        else:
            print("Opción inválida.")


def menu_sedes() -> None:
    while True:
        mostrar_titulo("GESTIÓN DE SEDES")
        print("1. Crear sede")
        print("2. Listar sedes")
        print("3. Editar sede")
        print("4. Eliminar sede")
        print("5. Regresar")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            crear_sede()
        elif opcion == "2":
            listar_sedes()
        elif opcion == "3":
            actualizar_sede()
        elif opcion == "4":
            eliminar_sede()
        elif opcion == "5":
            return
        else:
            print("Opción inválida.")


def menu_principal() -> None:
    global DB_SESSION
    init_db()
    with SessionLocal() as session:
        DB_SESSION = session
        _asegurar_usuario_admin()
        try:
            while True:
                mostrar_titulo("SISTEMA DE GESTIÓN")
                print("1. Iniciar sesión")
                print("2. Crear usuario")
                print("3. Salir")
                opcion = input("Seleccione una opción: ").strip()
                if opcion == "1":
                    usuario = iniciar_sesion()
                    if usuario:
                        while True:
                            mostrar_titulo(f"BIENVENIDO {usuario.upper()}")
                            print("1. Gestionar clientes")
                            print("2. Gestionar membresías")
                            print("3. Gestionar sedes")
                            print("4. Gestionar rutinas")
                            print("5. Gestionar pagos")
                            print("6. Gestionar equipos")
                            print("7. Gestionar entrenadores")
                            print("8. Gestionar clases")
                            print("9. Gestionar asistencias")
                            print("10. Cerrar sesión")
                            subopcion = input("Seleccione una opción: ").strip()
                            if subopcion == "1":
                                menu_clientes()
                            elif subopcion == "2":
                                menu_membresias()
                            elif subopcion == "3":
                                menu_sedes()
                            elif subopcion == "4":
                                menu_rutinas()
                            elif subopcion == "5":
                                menu_pagos()
                            elif subopcion == "6":
                                menu_equipos()
                            elif subopcion == "7":
                                menu_entrenadores()
                            elif subopcion == "8":
                                menu_clases()
                            elif subopcion == "9":
                                menu_asistencias()
                            elif subopcion == "10":
                                print("Sesión cerrada.")
                                break
                            else:
                                print("Opción inválida.")
                elif opcion == "2":
                    crear_usuario()
                elif opcion == "3":
                    print("Gracias por usar el sistema.")
                    break
                else:
                    print("Opción inválida.")
        finally:
            DB_SESSION = None
            try:
                session.rollback()
            except SQLAlchemyError:
                session.invalidate()


if __name__ == "__main__":
    menu_principal()
