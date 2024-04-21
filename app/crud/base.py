from typing import Optional, Any
from collections.abc import Iterable

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """
    Базовый класс для CRUD операций.
    """

    def __init__(self, model):
        """
        Инициализирует экземпляр с заданной моделью.
        """
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        """
        Получает объект по его ID.
        """
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """
        Получает все объекты модели.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession, user: Optional[User] = None):
        """
        Создает новый объект.
        """
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        """
        Обновляет существующий объект.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        return db_obj

    async def get_open_objects(self, session: AsyncSession):
        """
        Возвращает незавершенные объекты, сортированные по дате создания.
        """

        objs = await session.execute(
            select(self.model)
            .where(self.model.close_date.is_(None))
            .order_by(self.model.create_date)
        )
        return objs.scalars().all()

    async def get_object_by_attr(self, attr: str, value: Any, session: AsyncSession):
        """
        Поиск объектов по атрибуту и его значению.
        """

        object = await session.execute(
            select(self.model).where(getattr(self.model, attr) == value)
        )
        return object.scalars().all()

    async def remove(self, db_obj, session: AsyncSession):
        """
        Удаляет объект.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def refresh(self, objs, session: AsyncSession):
        """
        Обновляет состояние объектов в сессии.
        """
        if not isinstance(objs, Iterable):
            objs = (objs,)
        session.add_all(objs)
        await session.commit()
        for obj in objs:
            await session.refresh(obj)
