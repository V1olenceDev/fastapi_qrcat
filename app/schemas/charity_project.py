from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt

from app.constants import MAX_LENGTH, MIN_LENGTH


class CharityProjectBase(BaseModel):
    """
    Базовая модель для благотворительных проектов с опциональными полями.
    Используется как основа для других схем.
    """
    name: Optional[str] = Field(None, min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_LENGTH)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    """
    Схема для создания нового благотворительного проекта.
    Все поля являются обязательными.
    """
    name: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(min_length=MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """
    Схема для обновления существующего благотворительного проекта.
    Запрещает добавление дополнительных полей.
    """
    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """
    Схема представления благотворительного проекта в базе данных.
    Включает идентификатор, сумму инвестиций, статус полного финансирования,
    даты создания и закрытия проекта.
    """
    id: int
    invested_amount: NonNegativeInt = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
