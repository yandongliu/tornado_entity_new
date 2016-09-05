import contextlib
import datetime

from sqlalchemy import create_engine, CHAR, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship, scoped_session, sessionmaker

import config

engine = create_engine(config.get('database').get('url'), echo=False)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

class Base(object):

    def to_dict(self):
        if not self.attrs:
            raise Exception('No attrs defined')
        desp = {}
        for attr in self.attrs:
            value = getattr(self, attr)
            desp[attr] = value

        return desp

Model = declarative_base(cls=Base)


class CreatedTimestamp(object):
    """Mixin for a ``created_at`` columns."""
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )

class CreatedUpdatedTimestamp(object):
    """Mixin for a ``created_at`` and ``updated_at`` columns."""
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        index=True,
        nullable=False,
    )


class CreatedUpdatedDeletedTimestamp(CreatedUpdatedTimestamp):
    """Mixin for a ``created_at`` ``updated_at`` and ``deleted_at`` columns."""
    deleted_at = Column(DateTime, index=True, nullable=True)


def create_all_tables():
    Model.metadata.create_all(bind=engine)


@contextlib.contextmanager
def rw_transaction():
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise


@contextlib.contextmanager
def ro_transaction():
    try:
        yield session
        session.rollback()
    except:
        session.rollback()
        raise


class Entity(Model):

    __tablename__ = 'entity'

    uuid = Column(CHAR(36), primary_key=True)
    parent_uuid = Column(CHAR(36), ForeignKey('tag.uuid'), nullable=False, index=True)
    type_ = Column(String(30), nullable=False, index=True)
    name = Column(String(50), nullable=False, index=False)

    # attributes = relationship(
    #     'attribute',
    #     foreign_keys='entity_attribute.attri',
    #     lazy='joined'
    # )


class Attribute(Model):

    __tablename__ = 'attribute'

    uuid = Column(CHAR(36), primary_key=True)
    type_ = Column(String(30), nullable=False, index=True)
    name = Column(String(36), nullable=False, index=False)
    regex = Column(String(36), nullable=False, index=False)


class EntityAttribute(Model):

    __tablename__ = 'entity_attribute'

    uuid = Column(CHAR(36), primary_key=True)
    entity_uuid = Column(CHAR(36), ForeignKey('entity.uuid'), nullable=False, index=True)
    attribute_uuid = Column(CHAR(36), ForeignKey('attribute.uuid'), nullable=False, index=True)

    # entity = relationship('Entity')
    entity = relationship(
        'Entity',
        foreign_keys='entity.uuid',
        lazy='joined')
