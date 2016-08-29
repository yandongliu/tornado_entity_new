from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Model, CreatedUpdatedDeletedTimestamp


class Item(Model, CreatedUpdatedDeletedTimestamp):

    __tablename__ = 'item'

    attrs = [
        'uuid',
        'name',
        'value',
        'user_uuid',
        'created_at',
    ]

    uuid = Column(CHAR(36), primary_key=True)
    name = Column(String(100), nullable=False)
    value = Column(Integer)
    user_uuid = Column(CHAR(36), ForeignKey('user.uuid'), nullable=False)

    user = relationship("User")
