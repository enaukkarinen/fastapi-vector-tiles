from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
POSTGRES_DB = settings.POSTGRES_DB
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

local_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


from typing import AsyncGenerator


async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = local_session
    async with async_session() as db:
        yield db
