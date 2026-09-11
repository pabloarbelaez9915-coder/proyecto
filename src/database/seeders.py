from __future__ import annotations

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.database.models import (
    Asistencia,
    Clase,
    Cliente,
    Entrenador,
    Equipo,
    Membresia,
    Pago,
    Rutina,
    Sede,
)


def clear_all_data(session: Session) -> None:
    session.execute(delete(Asistencia))
    session.execute(delete(Pago))
    session.execute(delete(Rutina))
    session.execute(delete(Clase))
    session.execute(delete(Cliente))
    session.execute(delete(Entrenador))
    session.execute(delete(Equipo))
    session.execute(delete(Membresia))
    session.execute(delete(Sede))
    session.commit()


def seed_sedes(session: Session) -> list[Sede]:
    sedes = [
        Sede(
            id_sede=str(uuid4()),
            nombre="Sede Norte",
            direccion="Cra 10 # 20-30",
            telefono="3001234567",
            ciudad="Bogotá",
            descripcion="Sede principal del centro deportivo.",
            activo=True,
        ),
        Sede(
            id_sede=str(uuid4()),
            nombre="Sede Sur",
            direccion="Av 50 # 15-40",
            telefono="3007654321",
            ciudad="Medellín",
            descripcion="Sede para entrenamiento funcional.",
            activo=True,
        ),
    ]
    session.add_all(sedes)
    session.commit()
    return sedes


def seed_membresias(session: Session) -> list[Membresia]:
    membresias = [
        Membresia(
            id_membresia=str(uuid4()),
            nombre="Gold",
            descripcion="Acceso ilimitado y clases premium.",
            precio=79900.00,
            fecha_inscripcion=date.today(),
            activo=True,
        ),
        Membresia(
            id_membresia=str(uuid4()),
            nombre="Plus",
            descripcion="Acceso a gimnasia y cardio.",
            precio=49900.00,
            fecha_inscripcion=date.today(),
            activo=True,
        ),
    ]
    session.add_all(membresias)
    session.commit()
    return membresias


def seed_clientes(session: Session, membresias: list[Membresia]) -> list[Cliente]:
    clientes = [
        Cliente(
            id_cliente=str(uuid4()),
            primer_nombre="Ana",
            segundo_nombre="María",
            primer_apellido="García",
            segundo_apellido="López",
            correo="ana.garcia@email.com",
            telefono="3012001100",
            clave="clave123",
            id_membresia=membresias[0].id_membresia,
            activo=True,
        ),
        Cliente(
            id_cliente=str(uuid4()),
            primer_nombre="Luis",
            segundo_nombre="Felipe",
            primer_apellido="Pérez",
            segundo_apellido=None,
            correo="luis.perez@email.com",
            telefono="3023002200",
            clave="clave456",
            id_membresia=membresias[1].id_membresia,
            activo=True,
        ),
    ]
    session.add_all(clientes)
    session.commit()
    return clientes


def seed_entrenadores(session: Session, sedes: list[Sede]) -> list[Entrenador]:
    entrenadores = [
        Entrenador(
            id_entrenador=str(uuid4()),
            primer_nombre="Carlos",
            segundo_nombre="Andrés",
            primer_apellido="Ramírez",
            segundo_apellido="Mora",
            correo="carlos.ramirez@email.com",
            telefono="3105551212",
            clave="entrenador1",
            id_sede=sedes[0].id_sede,
            activo=True,
        ),
        Entrenador(
            id_entrenador=str(uuid4()),
            primer_nombre="Sofia",
            segundo_nombre=None,
            primer_apellido="Torres",
            segundo_apellido="Vega",
            correo="sofia.torres@email.com",
            telefono="3116661313",
            clave="entrenador2",
            id_sede=sedes[1].id_sede,
            activo=True,
        ),
    ]
    session.add_all(entrenadores)
    session.commit()
    return entrenadores


def seed_clases(session: Session, entrenadores: list[Entrenador], sedes: list[Sede]) -> list[Clase]:
    clases = [
        Clase(
            id_clase=str(uuid4()),
            nombre="Yoga Avanzado",
            descripcion="Clase de flexibilidad y relajación.",
            capacidad_maxima=20,
            horario="Lunes 18:00",
            nivel="Avanzado",
            id_entrenador=entrenadores[0].id_entrenador,
            id_sede=sedes[0].id_sede,
            activo=True,
        ),
        Clase(
            id_clase=str(uuid4()),
            nombre="CrossFit",
            descripcion="Entrenamiento funcional de alta intensidad.",
            capacidad_maxima=15,
            horario="Miércoles 19:00",
            nivel="Intermedio",
            id_entrenador=entrenadores[1].id_entrenador,
            id_sede=sedes[1].id_sede,
            activo=True,
        ),
    ]
    session.add_all(clases)
    session.commit()
    return clases


def seed_rutinas(session: Session, clientes: list[Cliente], entrenadores: list[Entrenador]) -> list[Rutina]:
    rutinas = [
        Rutina(
            id_rutina=str(uuid4()),
            nombre="Rutina de fuerza",
            descripcion="Ejercicios para mejorar fuerza muscular.",
            duracion_minutos=45,
            nivel="Intermedio",
            objetivo="Ganancia muscular",
            id_cliente=clientes[0].id_cliente,
            id_entrenador=entrenadores[0].id_entrenador,
            activo=True,
        ),
        Rutina(
            id_rutina=str(uuid4()),
            nombre="Rutina de resistencia",
            descripcion="Ejercicios cardiovasculares y de resistencia.",
            duracion_minutos=35,
            nivel="Principiante",
            objetivo="Mejorar resistencia",
            id_cliente=clientes[1].id_cliente,
            id_entrenador=entrenadores[1].id_entrenador,
            activo=True,
        ),
    ]
    session.add_all(rutinas)
    session.commit()
    return rutinas


def seed_equipos(session: Session, sedes: list[Sede]) -> list[Equipo]:
    equipos = [
        Equipo(
            id_equipo=str(uuid4()),
            nombre="Bicicleta estática",
            descripcion="Equipo cardiovascular",
            categoria="Cardio",
            estado="Operativo",
            id_sede=sedes[0].id_sede,
            activo=True,
        ),
        Equipo(
            id_equipo=str(uuid4()),
            nombre="Mancuerna 20kg",
            descripcion="Equipo de fuerza",
            categoria="Fuerza",
            estado="Operativo",
            id_sede=sedes[1].id_sede,
            activo=True,
        ),
    ]
    session.add_all(equipos)
    session.commit()
    return equipos


def seed_pagos(session: Session, clientes: list[Cliente], membresias: list[Membresia]) -> list[Pago]:
    pagos = [
        Pago(
            id_pago=str(uuid4()),
            monto=79900.00,
            metodo_pago="Nequi",
            estado="Pagado",
            fecha_pago=date.today(),
            id_cliente=clientes[0].id_cliente,
            id_membresia=membresias[0].id_membresia,
            activo=True,
        ),
        Pago(
            id_pago=str(uuid4()),
            monto=49900.00,
            metodo_pago="Tarjeta",
            estado="Pagado",
            fecha_pago=date.today(),
            id_cliente=clientes[1].id_cliente,
            id_membresia=membresias[1].id_membresia,
            activo=True,
        ),
    ]
    session.add_all(pagos)
    session.commit()
    return pagos


def seed_asistencias(session: Session, clientes: list[Cliente], clases: list[Clase]) -> list[Asistencia]:
    asistencias = [
        Asistencia(
            id_asistencia=str(uuid4()),
            fecha=date.today(),
            hora_entrada=datetime.now(),
            hora_salida=datetime.now(),
            estado="Presente",
            id_cliente=clientes[0].id_cliente,
            id_clase=clases[0].id_clase,
            activo=True,
        ),
        Asistencia(
            id_asistencia=str(uuid4()),
            fecha=date.today(),
            hora_entrada=datetime.now(),
            hora_salida=datetime.now(),
            estado="Tardanza",
            id_cliente=clientes[1].id_cliente,
            id_clase=clases[1].id_clase,
            activo=True,
        ),
    ]
    session.add_all(asistencias)
    session.commit()
    return asistencias


def seed_all(session: Session) -> dict[str, list]:
    clear_all_data(session)
    sedes = seed_sedes(session)
    membresias = seed_membresias(session)
    clientes = seed_clientes(session, membresias)
    entrenadores = seed_entrenadores(session, sedes)
    clases = seed_clases(session, entrenadores, sedes)
    rutinas = seed_rutinas(session, clientes, entrenadores)
    equipos = seed_equipos(session, sedes)
    pagos = seed_pagos(session, clientes, membresias)
    asistencias = seed_asistencias(session, clientes, clases)
    return {
        "sedes": sedes,
        "membresias": membresias,
        "clientes": clientes,
        "entrenadores": entrenadores,
        "clases": clases,
        "rutinas": rutinas,
        "equipos": equipos,
        "pagos": pagos,
        "asistencias": asistencias,
    }


if __name__ == "__main__":
    from src.database.config import SessionLocal
    from src.database.migrate import create_all_tables

    create_all_tables()
    with SessionLocal() as session:
        seed_all(session)
    print("Seeders ejecutados correctamente.")
