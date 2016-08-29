from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Model, CreatedTimestamp


class Tag(Model, CreatedTimestamp):

    __tablename__ = 'tag'

    uuid = Column(CHAR(36), primary_key=True)
    tag_type = Column(String(36), nullable=False, index=False)
    tag_name = Column(String(36), nullable=False, index=False)
    parent_uuid = Column(CHAR(36), ForeignKey('tag.uuid'), nullable=False, index=True)

    # parent_tag = relationship("Tag")
