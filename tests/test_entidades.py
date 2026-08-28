from uuid import uuid4
from datetime import date
from src.entities.clientes import Cliente, Membresia


def test_crear_cliente_y_membresia():
    membresia = Membresia(
        id_membresia=uuid4(),
        nombre="Gold",
        precio=49.99,
        fecha_inscripcion=date.today(),
    )

    cliente = Cliente(
        id_cliente=uuid4(),
        primer_nombre="Ana",
        primer_apellido="García",
        correo="ana@example.com",
        clave="secreta",
        id_membresia=membresia.id_membresia,
    )

    assert cliente.primer_nombre == "Ana"
    assert cliente.id_membresia == membresia.id_membresia
    assert membresia.nombre == "Gold"
    assert membresia.precio == 49.99
