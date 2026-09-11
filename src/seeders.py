from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import SessionLocal, init_db
from src.models import (
    AsistenciaModel,
    Base,
    ClaseModel,
    ClienteModel,
    EntrenadorModel,
    EquipoModel,
    MembresiaModel,
    PagoModel,
    RutinaModel,
    SedeModel,
)


def seed_membresias(session: Session) -> list[MembresiaModel]:
    planes = [
        ("Plan diario", Decimal("5000.00")),
        ("Plan mensual", Decimal("80000.00")),
        ("Plan anual", Decimal("800000.00")),
    ]
    result = []
    for nombre, precio in planes:
        item = session.scalar(
            select(MembresiaModel).where(MembresiaModel.nombre == nombre)
        )
        if item is None:
            item = MembresiaModel(
                nombre=nombre, precio=precio, fecha_inscripcion=date.today()
            )
            session.add(item)
        result.append(item)
    session.flush()
    return result


def seed_sedes(session: Session) -> list[SedeModel]:
    sede = session.scalar(select(SedeModel).where(SedeModel.nombre == "Sede Principal"))
    if sede is None:
        sede = SedeModel(
            nombre="Sede Principal", direccion="Calle 10 # 20-30", ciudad="Bogota"
        )
        session.add(sede)
    session.flush()
    return [sede]


def seed_clientes(session: Session, membresia: MembresiaModel) -> list[ClienteModel]:
    cliente = session.scalar(
        select(ClienteModel).where(ClienteModel.correo == "ana.seed@example.com")
    )
    if cliente is None:
        cliente = ClienteModel(
            primer_nombre="Ana",
            primer_apellido="Gomez",
            correo="ana.seed@example.com",
            clave="cambiar-en-produccion",
            id_membresia=membresia.id_membresia,
        )
        session.add(cliente)
    session.flush()
    return [cliente]


def seed_entrenadores(session: Session, sede: SedeModel) -> list[EntrenadorModel]:
    entrenador = session.scalar(
        select(EntrenadorModel).where(
            EntrenadorModel.correo == "carlos.seed@example.com"
        )
    )
    if entrenador is None:
        entrenador = EntrenadorModel(
            primer_nombre="Carlos",
            primer_apellido="Perez",
            correo="carlos.seed@example.com",
            clave="cambiar-en-produccion",
            id_sede=sede.id_sede,
        )
        session.add(entrenador)
    session.flush()
    return [entrenador]


def seed_clases(
    session: Session, sede: SedeModel, entrenador: EntrenadorModel
) -> list[ClaseModel]:
    clase = session.scalar(
        select(ClaseModel).where(ClaseModel.nombre == "Entrenamiento funcional")
    )
    if clase is None:
        clase = ClaseModel(
            nombre="Entrenamiento funcional",
            capacidad_maxima=20,
            horario="07:00",
            nivel="Inicial",
            id_sede=sede.id_sede,
            id_entrenador=entrenador.id_entrenador,
        )
        session.add(clase)
    session.flush()
    return [clase]


def seed_rutinas(
    session: Session, cliente: ClienteModel, entrenador: EntrenadorModel
) -> list[RutinaModel]:
    rutina = session.scalar(
        select(RutinaModel).where(RutinaModel.nombre == "Rutina inicial")
    )
    if rutina is None:
        rutina = RutinaModel(
            nombre="Rutina inicial",
            duracion_minutos=45,
            nivel="Inicial",
            objetivo="Acondicionamiento",
            id_cliente=cliente.id_cliente,
            id_entrenador=entrenador.id_entrenador,
        )
        session.add(rutina)
    session.flush()
    return [rutina]


def seed_equipos(session: Session, sede: SedeModel) -> list[EquipoModel]:
    equipo = session.scalar(
        select(EquipoModel).where(EquipoModel.nombre == "Bicicleta estatica 1")
    )
    if equipo is None:
        equipo = EquipoModel(
            nombre="Bicicleta estatica 1",
            categoria="Cardio",
            estado="Disponible",
            id_sede=sede.id_sede,
        )
        session.add(equipo)
    session.flush()
    return [equipo]


def seed_asistencias(
    session: Session, cliente: ClienteModel, clase: ClaseModel
) -> list[AsistenciaModel]:
    asistencia = session.scalar(
        select(AsistenciaModel).where(AsistenciaModel.id_cliente == cliente.id_cliente)
    )
    if asistencia is None:
        asistencia = AsistenciaModel(
            fecha=date.today(),
            hora_entrada=datetime.now(),
            estado="Presente",
            id_cliente=cliente.id_cliente,
            id_clase=clase.id_clase,
        )
        session.add(asistencia)
    session.flush()
    return [asistencia]


def seed_pagos(
    session: Session, cliente: ClienteModel, membresia: MembresiaModel
) -> list[PagoModel]:
    pago = session.scalar(
        select(PagoModel).where(PagoModel.id_cliente == cliente.id_cliente)
    )
    if pago is None:
        pago = PagoModel(
            monto=membresia.precio,
            metodo_pago="Transferencia",
            estado="Pagado",
            fecha_pago=date.today(),
            id_cliente=cliente.id_cliente,
            id_membresia=membresia.id_membresia,
        )
        session.add(pago)
    session.flush()
    return [pago]


def seed_all(session: Session) -> dict[str, int]:
    membresias = seed_membresias(session)
    sedes = seed_sedes(session)
    clientes = seed_clientes(session, membresias[1])
    entrenadores = seed_entrenadores(session, sedes[0])
    clases = seed_clases(session, sedes[0], entrenadores[0])
    rutinas = seed_rutinas(session, clientes[0], entrenadores[0])
    equipos = seed_equipos(session, sedes[0])
    asistencias = seed_asistencias(session, clientes[0], clases[0])
    pagos = seed_pagos(session, clientes[0], membresias[1])
    session.commit()
    return {
        "membresias": len(membresias),
        "sedes": len(sedes),
        "clientes": len(clientes),
        "entrenadores": len(entrenadores),
        "clases": len(clases),
        "rutinas": len(rutinas),
        "equipos": len(equipos),
        "asistencias": len(asistencias),
        "pagos": len(pagos),
    }


if __name__ == "__main__":
    init_db()
    with SessionLocal() as session:
        print(seed_all(session))
