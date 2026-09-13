import argparse
from decimal import Decimal

from src.crud.membresia_crud import MembresiaCrud
from src.database import SessionLocal, init_db
from src.models import MembresiaModel


def main(pausar: bool = False) -> None:
    init_db()
    with SessionLocal() as session:
        creado = MembresiaCrud.create(
            session,
            MembresiaModel(nombre="Demo examen", precio=Decimal("99999.00")),
        )
        print(f"CREATE: {creado.id_membresia} | {creado.nombre}")
        if pausar:
            input("Verifica CREATE en Neon y presiona Enter para continuar...")

        consultado = MembresiaCrud.get_by_id(session, creado.id_membresia)
        print(f"READ: {consultado.id_membresia} | {consultado.nombre}")
        if pausar:
            input("Verifica READ en Neon y presiona Enter para continuar...")

        actualizado = MembresiaCrud.update(
            session, creado.id_membresia, {"nombre": "Demo examen actualizada"}
        )
        print(f"UPDATE: {actualizado.id_membresia} | {actualizado.nombre}")
        if pausar:
            input("Verifica UPDATE en Neon y presiona Enter para continuar...")

        eliminado = MembresiaCrud.delete(session, creado.id_membresia)
        print(f"DELETE: {eliminado}")
        if pausar:
            input("Verifica DELETE en Neon y presiona Enter para finalizar...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demostración CRUD contra SQLAlchemy")
    parser.add_argument(
        "--pause",
        action="store_true",
        help="pausa después de cada operación para consultar Neon",
    )
    args = parser.parse_args()
    main(pausar=args.pause)
