from datetime import datetime
from typing import Union, Optional

from app.models import CharityProject, Donation


def exc_status_note(obj: Union[CharityProject, Donation]) -> None:
    """
    Обновляет статус объекта (благотворительного проекта или пожертвования),
    если он полностью финансируется, устанавливая его атрибут `fully_invested` в True
    и записывая текущую дату и время закрытия в `close_date`.
    """

    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


def investing(
    target: Union[CharityProject, Donation],
    sources: Optional[Union[list[CharityProject], list[Donation]]],
) -> Union[list[CharityProject], list[Donation]]:
    """
    Распределяет средства от источников (пожертвований или благотворительных проектов)
    к целевому объекту (благотворительный проект или пожертвование) до его полного финансирования.
    """

    invest_remeins: int = target.full_amount

    for cur_obj in sources:
        amount: int = cur_obj.full_amount - cur_obj.invested_amount

        if not invest_remeins:
            break

        if invest_remeins > amount:
            invest_remeins -= amount
            cur_obj.invested_amount += amount

        else:
            cur_obj.invested_amount += invest_remeins
            invest_remeins = 0

        exc_status_note(cur_obj)

    target.invested_amount = target.full_amount - invest_remeins
    exc_status_note(target)
    return sources
