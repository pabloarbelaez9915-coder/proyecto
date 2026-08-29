from uuid import uuid4
from datetime import date
from src.entities.clientes import Cliente, Membresia
from src.main import parse_precio


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


def test_parse_precio_acepta_valores_con_moneda():
    assert parse_precio("68.000$") == 68.0
    assert parse_precio("1,200.50") == 1200.5
