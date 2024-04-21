import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

# Создание контекстных менеджеров для удобной работы с асинхронными сессиями и пользователями
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr, password: str, is_superuser: bool = False
):
    """
    Асинхронно создает нового пользователя или суперпользователя.

    Использует контекстные менеджеры для управления асинхронной сессией базы данных,
    доступа к базе данных пользователей и их управления. Если пользователь с указанным
    email уже существует, исключение UserAlreadyExists перехватывается и обрабатывается,
    чтобы предотвратить прерывание процесса.
    """
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """
    Асинхронно создает суперпользователя на основе данных из настроек.

    Проверяет, заданы ли email и пароль суперпользователя в настройках приложения,
    и если да, то создает суперпользователя с этими учетными данными. Эта функция
    предназначена для использования при инициализации приложения.

    """
    if (settings.first_superuser_email is not None and
            settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
