from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from constants import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)

Base = declarative_base()


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


Base.metadata.create_all(engine)
