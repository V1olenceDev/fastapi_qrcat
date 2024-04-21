from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings
from app.constants import INV_AMOUNT


class PreBase:
    """
    Базовый класс для всех моделей.
    Определяет общие атрибуты и поведение для таблиц.
    """

    @declared_attr
    def __tablename__(cls):
        """
        Автоматически генерирует имя таблицы на основе имени класса.
        """
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)  # Универсальный первичный ключ


Base = declarative_base(cls=PreBase)  # Создание базового класса с помощью PreBase


class DonationBase(Base):
    """
    Базовый класс для моделей CharityProject и Donation.
    Определяет общие атрибуты и ограничения для этих моделей.
    """

    __abstract__ = True
    __table_args__ = (CheckConstraint(
        'full_amount > 0',
        name='check_pos_full_amount',),
        CheckConstraint(
            'full_amount >= invested_amount',
            name='check_full_invest_amount',),
    )
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=INV_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        """
        Базовый класс для моделей CharityProject и Donation.
        Определяет общие атрибуты и ограничения для этих моделей.
        """
        if self.close_date:
            return (
                f"Объект {self.__class__.__name__}, закрыт {self.close_date}"
            )
        return f"Объект {self.__class__.__name__}. Общая сумма: {self.full_amount}. Текущая: {self.invested_amount}"


engine = create_async_engine(settings.database_url)  # Асинхронный движок SQLAlchemy

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)  # Фабрика асинхронных сессий


async def get_async_session():
    """
    Провайдер асинхронной сессии для использования в зависимостях FastAPI.
    Создает и управляет жизненным циклом асинхронной сессии.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
