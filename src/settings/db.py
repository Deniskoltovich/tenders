from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from settings.app import settings

dsn = (
    f"postgresql+asyncpg://"
    f"{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}"
    f"/{settings.POSTGRES_DATABASE}"
)

engine = create_async_engine(dsn, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
