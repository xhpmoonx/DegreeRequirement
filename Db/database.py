from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase,MappedAsDataclass

SQLACHEMY_DATABASE_URL="sqlite+aiosqlite:///./Database.db"

engine=create_async_engine(SQLACHEMY_DATABASE_URL,echo=True)

sessionLocal=async_sessionmaker(bind=engine,class_=AsyncSession,autocommit=False,autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase,MappedAsDataclass):
    pass

async def get_db():
    session=sessionLocal()
    try:
        yield session
    finally:
        await session.close()
