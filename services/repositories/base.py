from sqlalchemy.sql.expression import alias

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
            query = cls.Table.select().where(cls.Table.c.uuid == str(uuid))
            row = session.execute(query).first()
            # import pdb; pdb.set_trace()
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
    def read_one(cls, uuid):
        entity = super(EntityRepository, cls).read_one(uuid)
        entity.attributes = EntityRepository.read_attributes(uuid)
        return entity

    @classmethod
    def read_many_by_parent_uuid(cls, uuid):
        with ro_transaction() as session:
            query = cls.Table.select().where(cls.Table.c.parent_uuid == uuid)
            rows = session.execute(query)
            if rows:
                entities = map(cls.Mapper.to_entity_from_obj, list(rows))
                for e in entities:
                    e.attributes = EntityRepository.read_attributes(e.uuid) 
                return entities
            return []


    @classmethod
    def read_node_chain(cls, uuid, depth=0, max_depth=3):
        nodes = []
        if depth >= max_depth:
            return nodes
        children = cls.read_many_by_parent_uuid(uuid)
        for child in children:
            # print child.to_primitive()
            children_ = cls.read_node_chain(child.uuid, depth + 1, max_depth)
            node = EntityNode(child)
            node.children = children_
            nodes.append(node)
        return nodes


    @classmethod
    def read_attributes(cls, uuid):
        # import pdb; pdb.set_trace()
        attrs = EntityAttributeRepository.read_by_entity_uuid(uuid)
        ret = []
        for attr in attrs:
            attr_entity = AttributeRepository.read_one(attr.attribute_uuid)
            ret.append(attr_entity)
        return ret


class AttributeRepository(BaseRepository):

    Table = Attribute.__table__ 
    Mapper = AttributeMapper


def debug_query(query):
    from sqlalchemy.dialects import mysql
    print str(query.compile(dialect=mysql.dialect()))


class EntityAttributeRepository(BaseRepository):

    Table = EntityAttribute.__table__ 
    Mapper = EntityAttributeMapper
    EntityTable = EntityRepository.Table
    AttributeTable = AttributeRepository.Table

    @classmethod
    def _join_query(cls):
        query = cls.Table.join(cls.EntityTable).join(cls.AttributeTable)
        return query

    @classmethod
    def join_read_by_entity_uuid(cls, entity_uuid):
        with ro_transaction() as session:
            query = cls._join_query().select(use_labels=True).where(
                cls.Table.c.entity_uuid == entity_uuid
            )
            debug_query(query)
            rows = session.execute(query)
            if rows:
                return [cls.Mapper.to_entity_from_obj(
                    row,
                    cls.EntityTable,
                    cls.AttributeTable,
                    cls.Table
                ) for row in rows]

    @classmethod
    def read_by_entity_uuid(cls, entity_uuid):
        with ro_transaction() as session:
            query = cls.Table.select().where(
                cls.Table.c.entity_uuid == entity_uuid
            )
            rows = session.execute(query)
            if rows:
                entities = map(cls.Mapper.to_entity_from_obj, list(rows))
                return entities
            return []
