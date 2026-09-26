from src.crud.orm_crud import PersistentCrud
from src.models import ClienteModel


class ClienteCrud(PersistentCrud[ClienteModel]):
    model = ClienteModel
    id_field = "id_cliente"
