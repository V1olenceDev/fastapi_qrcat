from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

# Включение маршрутов аутентификации
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

# Включение маршрутов регистрации
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

# Включение маршрутов управления пользователями
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True
)
def delete_user(id: str):
    """
    Эндпоинт для удаления пользователя. Эта операция запрещена и отмечена как устаревшая.

    Данная функция всегда возвращает ошибку HTTP 405 (Method Not Allowed),
    рекомендуя вместо удаления деактивировать пользователей.
    """
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!"
    )
