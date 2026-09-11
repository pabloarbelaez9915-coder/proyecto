from decimal import Decimal

from src.crud.membresia_crud import MembresiaCrud
from src.database import SessionLocal, init_db
from src.models import MembresiaModel


def main() -> None:
    init_db()
    with SessionLocal() as session:
        creado = MembresiaCrud.create(
            session,
            MembresiaModel(nombre="Demo examen", precio=Decimal("99999.00")),
        )
        print(f"CREATE: {creado.id_membresia} | {creado.nombre}")

        consultado = MembresiaCrud.get_by_id(session, creado.id_membresia)
        print(f"READ: {consultado.id_membresia} | {consultado.nombre}")

        actualizado = MembresiaCrud.update(
            session, creado.id_membresia, {"nombre": "Demo examen actualizada"}
        )
        print(f"UPDATE: {actualizado.id_membresia} | {actualizado.nombre}")

        eliminado = MembresiaCrud.delete(session, creado.id_membresia)
        print(f"DELETE: {eliminado}")


if __name__ == "__main__":
    main()
