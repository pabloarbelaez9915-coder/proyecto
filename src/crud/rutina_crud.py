from src.crud.orm_crud import PersistentCrud
from src.models import RutinaModel


class RutinaCrud(PersistentCrud):
    model = RutinaModel
    id_field = "id_rutina"
