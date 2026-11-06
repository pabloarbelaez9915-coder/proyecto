from src.crud.orm_crud import PersistentCrud
from src.models import PagoModel


class PagoCrud(PersistentCrud[PagoModel]):
    model = PagoModel
    id_field = "id_pago"
