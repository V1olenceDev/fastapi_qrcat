from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Схема для чтения данных пользователя.

    Наследует и использует все поля из BaseUser схемы `fastapi-users`,
    предназначена для вывода общедоступной информации о пользователе.
    """
    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Схема для создания нового пользователя.

    Наследует и использует все поля из BaseUserCreate схемы `fastapi-users`,
    включая такие поля, как email и пароль, необходимые при регистрации пользователя.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема для обновления данных пользователя.

    Наследует и использует поля из BaseUserUpdate схемы `fastapi-users`,
    позволяя обновить информацию пользователя, например, пароль или email.
    """
    pass
