from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """
    CRUD операции для модели благотворительного проекта.

    Наследуется от общего базового класса CRUDBase и добавляет специфичную для модели
    CharityProject функциональность.
    """
    pass


# Создание экземпляра CRUD операций для благотворительных проектов.
charity_project_crud = CRUDCharityProject(CharityProject)
