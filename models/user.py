from sqlalchemy import CHAR, Column, DateTime, Integer, String

from .base import Model, CreatedUpdatedDeletedTimestamp


class User(Model, CreatedUpdatedDeletedTimestamp):

    __tablename__ = 'user'

    attrs = [
        'uuid',
        'name',
        'value',
        'created_at',
    ]

    uuid = Column(CHAR(36), primary_key=True)
    email = Column(String(100), nullable=False)
    passwd = Column(String(100), nullable=False)
