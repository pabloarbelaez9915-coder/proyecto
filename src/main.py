from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID, uuid4

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.entities.clientes import Cliente, Membresia
else:
    from src.entities.clientes import Cliente, Membresia


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


def parse_precio(valor: object) -> float:
    texto = str(valor).strip()
    if not texto:
        raise ValueError("El precio no puede estar vacío.")

    texto = re.sub(r"[^0-9,\.]", "", texto)
    if not texto:
        raise ValueError("El precio debe ser un número válido.")

    if "," in texto and "." in texto:
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "," in texto:
        partes = texto.split(",")
        if len(partes) > 2:
            texto = "".join(partes)
        elif len(partes[-1]) <= 2:
            texto = ".".join(partes)
        else:
            texto = "".join(partes)

    return float(texto)


def pedir_precio(label: str = "Precio") -> float:
    ejemplo = "sin símbolo monetario (ej: 68.000 o 1,200.50; también acepta $68.000)"
    valor = input(f"{label} ({ejemplo}): ").strip()
    return parse_precio(valor or 0)


def crear_membresia() -> None:
    mostrar_titulo("CREAR MEMBRESIA")
    nombre = input("Nombre: ").strip()
    try:
        precio = pedir_precio("Precio")
        membresia = Membresia(
            nombre=nombre, precio=precio, fecha_inscripcion=date.today()
        )
        MEMBRESIAS.append(membresia)
        print(f"Membresía creada: {membresia}")
    except ValueError as exc:
        print(f"Error: {exc}")


def listar_membresias() -> None:
    mostrar_titulo("MEMBRESIAS")
    if not MEMBRESIAS:
        print("No hay membresías registradas.")
        return
    for item in MEMBRESIAS:
        print(
            f"- {item.id_membresia} | {item.nombre} | ${item.precio} | Inscrita: {item.fecha_inscripcion}"
        )


def actualizar_membresia() -> None:
    listar_membresias()
    if not MEMBRESIAS:
        return
    id_buscar = input("Ingrese el ID de la membresía a editar: ").strip()
    for item in MEMBRESIAS:
        if str(item.id_membresia) == id_buscar:
            try:
                nuevo_nombre = (
                    input(f"Nuevo nombre ({item.nombre}): ").strip() or item.nombre
                )
                nuevo_precio = item.precio
                if input(
                    f"Desea cambiar el precio actual de {item.precio}? (s/n): "
                ).strip().lower() in {"s", "si", "y", "yes"}:
                    nuevo_precio = pedir_precio("Nuevo precio")
                item.actualizar(
                    nombre=nuevo_nombre,
                    precio=nuevo_precio,
                )
                print("Membresía actualizada correctamente.")
                return
            except ValueError as exc:
                print(f"Error: {exc}")
                return
    print("No se encontró la membresía.")


def eliminar_membresia() -> None:
    listar_membresias()
    if not MEMBRESIAS:
        return
    id_buscar = input("Ingrese el ID de la membresía a eliminar: ").strip()
    for idx, item in enumerate(MEMBRESIAS):
        if str(item.id_membresia) == id_buscar:
            del MEMBRESIAS[idx]
            print("Membresía eliminada.")
            return
    print("No se encontró la membresía.")


def seleccionar_membresia(permitir_vacia: bool = True) -> Optional[Membresia]:
    if not MEMBRESIAS:
        print("No hay membresías registradas.")
        return None

    print("Membresías disponibles:")
    for idx, membresia in enumerate(MEMBRESIAS, start=1):
        print(f"  {idx}. {membresia.nombre} - ${membresia.precio}")

    opcion = input(
        "Seleccione una membresía por número "
        + ("(deje vacío para sin membresía): " if permitir_vacia else ": ")
    ).strip()

    if not opcion and permitir_vacia:
        return None

    try:
        indice = int(opcion)
    except ValueError:
        print("Opción inválida. Ingrese un número válido.")
        return seleccionar_membresia(permitir_vacia)

    if 1 <= indice <= len(MEMBRESIAS):
        return MEMBRESIAS[indice - 1]

    print("Número fuera de rango.")
    return seleccionar_membresia(permitir_vacia)


def crear_cliente() -> None:
    mostrar_titulo("CREAR CLIENTE")
    primer_nombre = input("Primer nombre: ").strip()
    segundo_nombre = input("Segundo nombre: ").strip()
    primer_apellido = input("Primer apellido: ").strip()
    segundo_apellido = input("Segundo apellido: ").strip()
    correo = input("Correo: ").strip()
    telefono = input("Teléfono: ").strip()
    clave = input("Clave: ").strip()

    membresia_seleccionada = seleccionar_membresia(permitir_vacia=True)

    try:
        cliente = Cliente(
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            correo=correo,
            telefono=telefono,
            clave=clave,
            id_membresia=(
                membresia_seleccionada.id_membresia if membresia_seleccionada else None
            ),
        )
        CLIENTES.append(cliente)
        print(f"Cliente creado: {cliente}")
    except ValueError as exc:
        print(f"Error: {exc}")


def listar_clientes() -> None:
    mostrar_titulo("CLIENTES")
    if not CLIENTES:
        print("No hay clientes registrados.")
        return
    for item in CLIENTES:
        membresia = next(
            (m.nombre for m in MEMBRESIAS if m.id_membresia == item.id_membresia),
            "Sin membresía",
        )
        print(
            f"- {item.id_cliente} | {item.primer_nombre} {item.primer_apellido} | {item.correo} | Membresía: {membresia}"
        )


def actualizar_cliente() -> None:
    listar_clientes()
    if not CLIENTES:
        return
    id_buscar = input("Ingrese el ID del cliente a editar: ").strip()
    for item in CLIENTES:
        if str(item.id_cliente) == id_buscar:
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
                nueva_clave = input("Nueva clave (dejar vacío para mantener): ").strip()
                nueva_id_membresia = item.id_membresia

                respuesta = (
                    input("¿Desea cambiar la membresía? (s/n): ").strip().lower()
                )
                if respuesta in {"s", "si", "y", "yes"}:
                    membresia_seleccionada = seleccionar_membresia(permitir_vacia=True)
                    nueva_id_membresia = (
                        membresia_seleccionada.id_membresia
                        if membresia_seleccionada is not None
                        else None
                    )

                item.actualizar(
                    primer_nombre=nuevo_nombre,
                    primer_apellido=nuevo_apellido,
                    correo=nuevo_correo,
                    clave=nueva_clave or item.clave,
                    id_membresia=nueva_id_membresia,
                )
                print("Cliente actualizado correctamente.")
                return
            except ValueError as exc:
                print(f"Error: {exc}")
                return
    print("No se encontró el cliente.")


def eliminar_cliente() -> None:
    listar_clientes()
    if not CLIENTES:
        return
    id_buscar = input("Ingrese el ID del cliente a eliminar: ").strip()
    for idx, item in enumerate(CLIENTES):
        if str(item.id_cliente) == id_buscar:
            del CLIENTES[idx]
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
        SEDES.append(sede)
        print(f"Sede creada: {sede}")
    except ValueError as exc:
        print(f"Error: {exc}")


def listar_sedes() -> None:
    mostrar_titulo("SEDES")
    if not SEDES:
        print("No hay sedes registradas.")
        return
    for item in SEDES:
        print(
            f"- {item.id_sede} | {item.nombre} | {item.ciudad} | {item.direccion} | {item.telefono} | {'Activa' if item.activo else 'Inactiva'}"
        )


def actualizar_sede() -> None:
    listar_sedes()
    if not SEDES:
        return
    id_buscar = input("Ingrese el ID de la sede a editar: ").strip()
    for item in SEDES:
        if str(item.id_sede) == id_buscar:
            nombre = input(f"Nuevo nombre ({item.nombre}): ").strip() or item.nombre
            direccion = (
                input(f"Nueva dirección ({item.direccion}): ").strip() or item.direccion
            )
            telefono = (
                input(f"Nuevo teléfono ({item.telefono}): ").strip() or item.telefono
            )
            ciudad = input(f"Nueva ciudad ({item.ciudad}): ").strip() or item.ciudad
            activo = input("¿Está activa? (s/n): ").strip().lower()
            item.actualizar(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                ciudad=ciudad,
                activo=activo != "n" if activo else item.activo,
            )
            print("Sede actualizada correctamente.")
            return
    print("No se encontró la sede.")


def eliminar_sede() -> None:
    listar_sedes()
    if not SEDES:
        return
    id_buscar = input("Ingrese el ID de la sede a eliminar: ").strip()
    for idx, item in enumerate(SEDES):
        if str(item.id_sede) == id_buscar:
            del SEDES[idx]
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
        print("5. Regresar al menú principal")
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
            print("Volviendo al menú principal...\n")
            return
        else:
            print("Opción inválida. Intente nuevamente.")


def menu_clientes() -> None:
    while True:
        mostrar_titulo("GESTIÓN DE CLIENTES")
        print("1. Crear cliente")
        print("2. Listar clientes")
        print("3. Editar cliente")
        print("4. Eliminar cliente")
        print("5. Regresar al menú principal")
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
            print("Volviendo al menú principal...\n")
            return
        else:
            print("Opción inválida. Intente nuevamente.")


def menu_sedes() -> None:
    while True:
        mostrar_titulo("GESTIÓN DE SEDES")
        print("1. Crear sede")
        print("2. Listar sedes")
        print("3. Editar sede")
        print("4. Eliminar sede")
        print("5. Regresar al menú principal")
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
            print("Volviendo al menú principal...\n")
            return
        else:
            print("Opción inválida. Intente nuevamente.")


def menu_principal() -> None:
    while True:
        mostrar_titulo("SISTEMA DE GESTIÓN")
        print("1. Iniciar sesión")
        print("2. Crear usuario")
        print("3. Salir del sistema")
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
                        print("Sesión cerrada correctamente.\n")
                        break
                    else:
                        print("Opción inválida. Intente nuevamente.")
        elif opcion == "2":
            crear_usuario()
        elif opcion == "3":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()
