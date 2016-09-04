from entities.base import EntityNode

from mappers.base import AttributeMapper, EntityMapper, EntityAttributeMapper
from models.base import ro_transaction, rw_transaction
from models.base import Attribute, Entity, EntityAttribute


class BaseRepository(object):

    Table = None
    Mapper = None


    @classmethod
    def read_one(cls, uuid):
        with ro_transaction() as session:
            query = cls.Table.select().where(cls.Table.c.uuid == uuid)
            row = session.execute(query).first()
            if row:
                return cls.Mapper.to_entity_from_obj(row)

    @classmethod
    def upsert(cls, entity):
        entity.validate()
        with rw_transaction() as session:
            _entity = cls.read_one(entity.uuid)
            if _entity:
                query = cls.Table.update().where(
                    cls.Table.c.uuid == entity.uuid
                ).values(cls.Mapper.to_record(entity))
                session.execute(query)
            else:
                query = cls.Table.insert().values(cls.Mapper.to_record(entity))
                session.execute(query)

    @classmethod
    def delete(cls, tag_uuid):
        with rw_transaction() as session:
            query = cls.Table.delete().where(
                cls.Table.c.uuid == tag_uuid
            )
            session.execute(query)


class EntityRepository(BaseRepository):

    Table = Entity.__table__ 
    Mapper = EntityMapper

    @classmethod
    def read_many_by_parent_uuid(cls, uuid):
        with ro_transaction() as session:
            query = cls.Table.select().where(cls.Table.c.parent_uuid == uuid)
            rows = session.execute(query)
            if rows:
                entities = map(cls.Mapper.to_entity_from_obj, list(rows))
                return entities
            return []


    @classmethod
    def read_chain(cls, uuid, depth=0, max_depth=3):
        nodes = []
        if depth >= max_depth:
            return nodes
        children = cls.read_many_by_parent_uuid(uuid)
        for child in children:
            # print child.to_primitive()
            children_ = cls.read_chain(child.uuid, depth + 1, max_depth)
            node = EntityNode(child)
            node.children = children_
            nodes.append(node)
        return nodes


class AttributeRepository(BaseRepository):

    Table = Attribute.__table__ 
    Mapper = AttributeMapper


class EntityAttributeRepository(BaseRepository):

    Table = EntityAttribute.__table__ 
    Mapper = EntityAttributeMapper
