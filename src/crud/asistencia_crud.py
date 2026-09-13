from src.crud.orm_crud import PersistentCrud
from src.models import AsistenciaModel


class AsistenciaCrud(PersistentCrud):
    model = AsistenciaModel
    id_field = "id_asistencia"
