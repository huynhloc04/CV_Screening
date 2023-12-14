from typing import Generic, TypeVar
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.future import select
from database.db_config import db, commit_rollback
from sqlmodel.ext.asyncio.session import AsyncSession


T = TypeVar('T')

class BaseHandler:
    """support base handler for CRUD in database by id"""
    model = Generic[T]
    # create_model = Generic[T]

    @classmethod
    async def create(cls, session: AsyncSession, model: Generic[T]):
        # model = cls.create_model(**kwargs)
        session.add(model)
        await commit_rollback(session, model=model)
        print(f"==> Add data to database")
        return model

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls.model)
        return(await session.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: str):
        query = select(cls.model).where(cls.model.id == id)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, id: int, **kwargs):
        query = sql_update(cls.model).where(cls.model.id == id).values(
            **kwargs).execution_options(synchronize_session="fetch")
        await session.execute(query)
        await commit_rollback(session)

    @classmethod
    async def delete(cls, session: AsyncSession, id: str):
        query = sql_delete(cls.model).where(cls.model.id == id)
        await session.execute(query)
        await commit_rollback(session)

