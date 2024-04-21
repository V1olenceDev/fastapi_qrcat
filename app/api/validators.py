from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(project_name: str, session: AsyncSession) -> None:
    """
    Проверяет, существует ли благотворительный проект с данным именем.
    Если проект найден, вызывает исключение HTTPException.
    """
    project = await charity_project_crud.get_object_by_attr('name', project_name, session)
    if project:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_lockup_dfields_value(project: CharityProject) -> None:
    """
    Проверяет, были ли уже вложены средства в проект.
    Если средства были вложены, запрещает удаление проекта, вызывая исключение HTTPException.
    """

    if project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Проект нельзя удалить, так как в него уже были внесены средства!',
        )


async def check_project_exists(project_id: int, session: AsyncSession) -> CharityProject:
    """
    Проверяет существование благотворительного проекта по его ID.
    В случае отсутствия проекта вызывает исключение HTTPException.
    """
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден')
    return project


async def check_close_date_status(project) -> None:
    """
    Проверяет, завершен ли сбор средств для проекта.
    Если сбор завершен, вызывает исключение HTTPException, запрещая любые изменения проекта.
    """

    if project.close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Сбор завершен! Проект нельзя удалить!',
        )


async def check_lockup_update_fields(cur_amount: int, new_amount: int) -> None:
    """
    Проверяет, можно ли изменить общую сумму проекта на меньшую, чем уже вложенная.
    Если текущая сумма инвестиций больше новой запрашиваемой суммы, вызывает исключение HTTPException.
    """
    if cur_amount > new_amount:
        raise HTTPException(
            status_code=422,
            detail='Нелья установить значение full_amount меньше уже вложенной суммы!',
        )