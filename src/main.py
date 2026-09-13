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

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.entities.clientes import Cliente, Membresia
else:
    from src.entities.clientes import Cliente, Membresia

from src.crud import ClienteCrud, MembresiaCrud, SedeCrud
from src.database import SessionLocal, init_db
from src.models import ClienteModel, MembresiaModel, SedeModel


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


USUARIOS: Dict[str, str] = {
    "admin": "1234",
}
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
    if usuario in USUARIOS:
        print("Ese usuario ya existe.")
        return
    USUARIOS[usuario] = clave
    print(f"Usuario '{usuario}' registrado correctamente.")


def iniciar_sesion() -> Optional[str]:
    mostrar_titulo("LOGIN")
    usuario = input("Usuario: ").strip()
    clave = input("Clave: ").strip()
    if USUARIOS.get(usuario) == clave:
        print(f"Bienvenido, {usuario}.")
        return usuario
    print("Usuario o contraseña incorrectos.")
    return None


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
                            print("4. Cerrar sesión")
                            subopcion = input("Seleccione una opción: ").strip()
                            if subopcion == "1":
                                menu_clientes()
                            elif subopcion == "2":
                                menu_membresias()
                            elif subopcion == "3":
                                menu_sedes()
                            elif subopcion == "4":
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
