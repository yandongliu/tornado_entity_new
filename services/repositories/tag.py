from models.base import ro_transaction, rw_transaction
from models import Tag
from mappers.tag import TagMapper


class TagRepository(object):

    Table = Tag.__table__

    @classmethod
    def read_one(cls, uuid):
        with ro_transaction() as session:
            query = cls.Table.select().where(cls.Table.c.uuid == uuid)
            row = session.execute(query).first()
            if row:
                return TagMapper.to_entity_from_obj(row)

    @classmethod
    def read_all(cls):
        with ro_transaction() as session:
            query = cls.Table.select()
            rows = session.execute(query)
            if rows:
                entities = map(TagMapper.to_entity_from_obj, list(rows))
                return entities

    @classmethod
    def upsert(cls, entity):
        with rw_transaction() as session:
            _entity = cls.read_one(entity.uuid)
            if _entity:
                query = cls.Table.update().where(
                    cls.Table.c.uuid == entity.uuid
                ).values(TagMapper.to_record(entity))
                session.execute(query)
            else:
                query = cls.Table.insert().values(TagMapper.to_record(entity))
                session.execute(query)
