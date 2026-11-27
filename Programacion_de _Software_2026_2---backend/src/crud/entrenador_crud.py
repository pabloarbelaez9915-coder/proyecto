from src.crud.orm_crud import PersistentCrud
from src.models import EntrenadorModel


class EntrenadorCrud(PersistentCrud[EntrenadorModel]):
    model = EntrenadorModel
    id_field = "id_entrenador"
