from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text


class Base(DeclarativeBase): pass


metadata = Base.metadata


class Presentation(Base):
    __tablename__ = 'presentation'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    presenter = Column(String, nullable=False)
    time = Column(String, nullable=False)


class Shedule(Base):
    __tablename__ = 'shedule'

    id = Column(Integer, primary_key=True, index=True)
    pr_id = Column(Integer, nullable=False)
    pr_name = Column(String, nullable=False)
    presenter = Column(String, nullable=False)
    room_id = Column(Integer, nullable=False)
    time = Column(String, nullable=False)
    listeners = Column(Text)


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, index=True)
    room = Column(Integer, nullable=False)