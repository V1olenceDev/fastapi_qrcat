from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    """
    Базовая модель для пожертвований, определяющая основные поля, используемые во всех операциях.
    Запрещает добавление дополнительных полей не описанных в модели.
    """
    full_amount: PositiveInt = Field(description="Целевая сумма пожертвования.")
    comment: Optional[str] = Field(None, description="Комментарий к пожертвованию.")

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """
    Модель для создания пожертвования. Использует все поля базовой модели.
    """
    pass


class DonationView(DonationBase):
    """
    Модель для представления пожертвования, добавляет идентификатор и дату создания.
    Предназначена для вывода информации о пожертвовании.
    """
    id: int = Field(description="Уникальный идентификатор пожертвования.")
    create_date: datetime = Field(description="Дата и время создания пожертвования.")

    class Config:
        orm_mode = True


class DonationDB(DonationView):
    """
    Расширенная модель пожертвования для базы данных, включает поля пользователя, инвестированной суммы,
    статуса полного инвестирования и даты закрытия пожертвования.
    """
    user_id: Optional[int] = Field(None, description="Идентификатор пользователя, сделавшего пожертвование.")
    invested_amount: NonNegativeInt = Field(0, description="Сумма, уже инвестированная в проекты.")
    fully_invested: bool = Field(False, description="Флаг, показывающий, полностью ли инвестировано пожертвование.")
    close_date: Optional[datetime] = Field(None, description="Дата и время закрытия пожертвования.")
