from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject

MESSAGE_NOT_NONE = 'Поле обязательное!'
MESSAGE_EXIST_NAME = 'Проект с таким именем уже существует!'
MESSAGE_NOT_PROJECT = 'Данного проекта нет!'
MESSAGE_HAVE_MONEY = 'Нельзя удалить проект с деньгами!'
MESSAGE_DELETE_CLOSED_PROJECT = 'Нельзя удалить закрытый проект!'
MESSAGE_PATCH_CLOSED_PROJECT = 'Нельзя редактировать закрытый проект!'
MESSAGE_PATCH_NOT_EMPTY_PROJECT = (
    'Нельзя При редактировании проекта '
    'устанавливать требуемую сумму меньше внесённой.')


async def check_info_none(
        object: str,
        session: AsyncSession,
) -> None:
    if object is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=MESSAGE_NOT_NONE
        )


async def check_name_duplicate(
        charity_project: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        charity_project, session)
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MESSAGE_EXIST_NAME
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        object_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=MESSAGE_NOT_PROJECT
        )
    return charity_project


async def check_delete_project_invested(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        object_id=project_id, session=session
    )
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MESSAGE_HAVE_MONEY
        )
    return charity_project


async def check_delete_project_closed(
        project_id: int,
        session: AsyncSession,
):
    charity_project = await charity_project_crud.get(
        object_id=project_id, session=session
    )
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MESSAGE_DELETE_CLOSED_PROJECT
        )
    return charity_project


async def check_update_project_closed(
        project_id: int,
        session: AsyncSession,
):
    charity_project = await charity_project_crud.get(
        object_id=project_id, session=session
    )
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MESSAGE_PATCH_CLOSED_PROJECT
        )
    return charity_project


async def check_update_project_invested(
        project,
        new_full_amount,
):
    if new_full_amount:
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=MESSAGE_PATCH_NOT_EMPTY_PROJECT
            )
    return project
