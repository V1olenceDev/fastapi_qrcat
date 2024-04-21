from sqlalchemy import Column, Text, String

from app.core.db import DonationBase
from app.constants import MAX_LENGTH


class CharityProject(DonationBase):
    """
    Модель благотворительного проекта.

    Представляет собой благотворительный проект, который может получать пожертвования от пользователей.
    Включает информацию о названии проекта, его описании, целевой и уже инвестированной суммах, а также
    статусе проекта (открыт/закрыт) и даты его создания и закрытия.
    """
    name = Column(String(MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
