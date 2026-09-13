from src.crud.orm_crud import PersistentCrud
from src.models import EquipoModel


class EquipoCrud(PersistentCrud):
    model = EquipoModel
    id_field = "id_equipo"
