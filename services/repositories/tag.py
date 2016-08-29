from models.base import session
from models import Tag
from mappers.tag import TagMapper


class TagRepository(object):

    Table = Tag.__table__

    @classmethod
    def read_one(cls, uuid):
        query = cls.Table.select().where(cls.Table.c.uuid == uuid)
        rows = session.execute(query)
        if rows:
            entities = map(TableMapper.to_entity_from_obj, list(rows))
            return entities[0]

    @classmethod
    def read_all(cls):
        query = cls.Table.select()
        rows = session.execute(query)
        if rows:
            entities = map(TagMapper.to_entity_from_obj, list(rows))
            return entities
