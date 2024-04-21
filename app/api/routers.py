from fastapi import APIRouter
from app.api.endpoints import charity_project_router, donation_router, user_router

# Создание основного роутера приложения.
main_router = APIRouter()

# Подключение роутера проектов благотворительности.
# Этот роутер обрабатывает все операции, связанные с благотворительными проектами.
main_router.include_router(
    charity_project_router, prefix='/charity_project', tags=['Charity Projects']
)

# Подключение роутера пожертвований.
# Этот роутер обрабатывает все операции, связанные с пожертвованиями.
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donations']
)

# Подключение роутера пользователей.
# Этот роутер обрабатывает операции, связанные с пользователями.
main_router.include_router(user_router)
