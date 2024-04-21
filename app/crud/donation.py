from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    """
    CRUD операции для модели пожертвований.

    Наследуется от общего базового класса CRUDBase и добавляет функциональность,
    специфичную для модели Donation.
    """
    pass


# Создание экземпляра CRUD операций для пожертвований.
donation_crud = CRUDDonation(Donation)
