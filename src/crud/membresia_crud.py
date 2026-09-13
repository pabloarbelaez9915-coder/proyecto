from src.crud.orm_crud import PersistentCrud
from src.models import MembresiaModel


class MembresiaCrud(PersistentCrud):
    model = MembresiaModel
    id_field = "id_membresia"
