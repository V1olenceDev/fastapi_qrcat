from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя для аутентификации и авторизации в приложении.

    Наследует поля и методы из SQLAlchemyBaseUserTable, предоставляемого fastapi-users,
    для удобной работы с аутентификацией, авторизацией и управлением пользователями
    в приложении FastAPI. Поддерживает все основные функции, необходимые для работы с пользователями,
    включая регистрацию, вход, выход и изменение пользовательских данных.
    """
    pass
