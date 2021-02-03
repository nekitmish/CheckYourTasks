import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f'{self.__name__}'