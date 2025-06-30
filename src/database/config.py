from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

from src.users.models import UserOrm,VolunteerOrm,NeedyOrm
from src.requests.models import RequestOrm
from .base import  Base

from src.config.settings import db_settings

async_engine = create_async_engine(url= f"postgresql+asyncpg://{db_settings.db_user}:{db_settings.db_pass}@{db_settings.db_host}/{db_settings.db_name}")

async_session = async_sessionmaker(bind=async_engine)

async def init_db():
    async with async_engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


