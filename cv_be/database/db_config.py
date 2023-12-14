import os
from fastapi import HTTPException, status
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from typing import Generic, TypeVar
from sqlalchemy.orm import sessionmaker
import env
from config import JDTXT_PATH, JDSCORE_PATH, CV_EXTRACTION_PATH, JD_EXTRACTION_PATH, CVPDF_PATH, TMP_PATH

T = TypeVar('T')

DATABASE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Cannot execute database request - commit roll back inited",
    headers={"error":"DATABASE ERROR"}
)

class AsyncDataBaseConnection:
    def __init__(self):
        self.async_engine = self.get_asyncengine()
        self.session_maker = self.get_session()

    def get_asyncengine(self):
        # db_url = os.getenv('DATABASE_URL')
        db_url = env.DATABASE_URL
        if not db_url:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="MISSING DATABASE URL ENV VARIABLE")
        return AsyncEngine(create_engine(db_url, echo=True, future=True))
    
    async def init_db(self):
        os.makedirs(JDSCORE_PATH, exist_ok=True)
        os.makedirs(JDTXT_PATH, exist_ok=True)
        os.makedirs(CV_EXTRACTION_PATH, exist_ok=True)
        os.makedirs(JD_EXTRACTION_PATH, exist_ok=True)
        os.makedirs(CVPDF_PATH, exist_ok=True)
        os.makedirs(TMP_PATH, exist_ok=True)
        async with self.async_engine.begin() as conn:
            # await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
    
    async def get_session(self) -> AsyncSession:
        async_session = sessionmaker(
            self.async_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session
        
db = AsyncDataBaseConnection()

async def commit_rollback(session: AsyncSession, model: Generic[T] = None):
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise DATABASE_EXCEPTION
    if model:
        await session.refresh(model)

