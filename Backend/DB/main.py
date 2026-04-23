import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio.session import AsyncSession

from Backend.config.config import Config

db_url = Config.DATABASE_URL


engine = create_async_engine(
    db_url,
    echo=False,
    pool_pre_ping = True,
    pool_size = 10,
    max_overflow = 20
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()-> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(bind = engine, class_ = AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session