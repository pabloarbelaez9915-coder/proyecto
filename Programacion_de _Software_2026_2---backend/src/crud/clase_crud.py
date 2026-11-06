from src.crud.orm_crud import PersistentCrud
from src.models import ClaseModel


class ClaseCrud(PersistentCrud[ClaseModel]):
    model = ClaseModel
    id_field = "id_clase"
