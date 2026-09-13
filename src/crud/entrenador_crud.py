from src.crud.orm_crud import PersistentCrud
from src.models import EntrenadorModel


class EntrenadorCrud(PersistentCrud):
    model = EntrenadorModel
    id_field = "id_entrenador"
