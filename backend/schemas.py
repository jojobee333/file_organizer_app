import asyncio

from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import relationship, declarative_base, DeclarativeBase
from constants import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Origin(Base):
    __tablename__ = "origins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String)


class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path = Column(String)
    formats = relationship("Format", back_populates="target")  # Set up relationship to Format


class Format(Base):
    __tablename__ = "formats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    target_id = Column(Integer, ForeignKey("targets.id"))  # Correct use of ForeignKey
    target = relationship("Target", back_populates="formats")  # Back-reference to Target


async def async_create_classes() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)



