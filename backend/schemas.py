import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase
from constants import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Origin(Base):
    __tablename__ = "origins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    path = Column(String)


class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    path = Column(String, unique=True)
    formats = relationship("Format", back_populates="target")  # Set up relationship to Format


class Format(Base):
    __tablename__ = "formats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    target_id = Column(Integer, ForeignKey("targets.id"), nullable=False)  # Correct use of ForeignKey
    target = relationship("Target", back_populates="formats")  # Back-reference to Target


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    origin_name = Column(String)
    files_moved = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.now)


async def async_create_classes() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
