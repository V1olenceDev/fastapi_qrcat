from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """
    Асинхронная функция, вызываемая при запуске приложения.

    В рамках этой функции выполняется создание суперпользователя, если он не был создан ранее.
    Это обеспечивает наличие административного доступа к функциям приложения с момента его запуска.
    """
    await create_first_superuser()
