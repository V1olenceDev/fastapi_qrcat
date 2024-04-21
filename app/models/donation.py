from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import DonationBase


class Donation(DonationBase):
    """
    Модель пожертвования.

    Отражает пожертвование, сделанное пользователем на поддержку одного или нескольких благотворительных проектов.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
