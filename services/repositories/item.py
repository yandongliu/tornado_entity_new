from models.base import session
from models import Item
from mappers.item import ItemMapper


class ItemRepository(object):

    ItemTable = Item.__table__

    @classmethod
    def read_one(cls, uuid):
        query = cls.ItemTable.select().where(ItemTable.c.uuid == uuid)
        rows = session.execute(query)
        if rows:
            entities = map(ItemMapper.to_entity_from_obj, list(rows))
            return entities[0]

    @classmethod
    def read_all(cls):
        query = cls.ItemTable.select()
        rows = session.execute(query)
        if rows:
            entities = map(ItemMapper.to_entity_from_obj, list(rows))
            return entities
