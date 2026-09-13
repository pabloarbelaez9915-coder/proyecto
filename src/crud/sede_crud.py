from src.crud.orm_crud import PersistentCrud
from src.models import SedeModel


class SedeCrud(PersistentCrud):
    model = SedeModel
    id_field = "id_sede"
