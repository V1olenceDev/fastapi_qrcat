from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_exists,
    check_lockup_dfields_value,
    check_lockup_update_fields,
    check_close_date_status,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.services.investment import exc_status_note, investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Создает новый благотворительный проект. Доступно только для суперпользователей.
    После создания проекта автоматически запускается процесс распределения средств
    от открытых пожертвований к этому проекту.
    """

    await check_name_duplicate(project.name, session)

    new_project = await charity_project_crud.create(project, session)
    open_donations = await donation_crud.get_open_objects(session)
    modify = investing(new_project, open_donations)
    await charity_project_crud.refresh([new_project] + modify, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_charityproject(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список всех благотворительных проектов. Доступен для всех пользователей,
    включая неавторизованных.
    """
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновляет данные благотворительного проекта по его ID. Доступно только для суперпользователей.
    Проверяет различные условия перед обновлением, включая дублирование имени и проверку на изменение
    суммы сбора на значение меньше уже собранных средств.
    """

    project = await check_project_exists(project_id, session)
    await check_close_date_status(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_lockup_update_fields(
            project.invested_amount, obj_in.full_amount
        )
    project = await charity_project_crud.update(project, obj_in, session)
    exc_status_note(project)
    await charity_project_crud.refresh(project, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charityproject(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет благотворительный проект. Доступно только для суперпользователей.
    Удаление возможно только если в проект еще не были вложены средства и он не был закрыт.
    """

    project = await check_project_exists(project_id, session)
    await check_lockup_dfields_value(project)
    await check_close_date_status(project)
    project = await charity_project_crud.remove(project, session)
    return project
