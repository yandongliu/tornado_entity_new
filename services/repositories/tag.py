from .base import BaseRepository
from entities.tag import TagNode
from models.base import ro_transaction, rw_transaction
from models import Tag
from mappers.tag import TagMapper


class TagRepository(BaseRepository):

    Table = Tag.__table__

    @classmethod
    def read_many_by_parent_uuid(cls, uuid):
        with ro_transaction() as session:
            query = cls.Table.select().where(cls.Table.c.parent_uuid == uuid)
            rows = session.execute(query)
            if rows:
                entities = map(TagMapper.to_entity_from_obj, list(rows))
                return entities
            return []

    @classmethod
    def read_chain(cls, uuid, depth=0, max_depth=3):
        # read tag's children
        nodes = []
        if depth >= max_depth:
            return nodes
        children = cls.read_many_by_parent_uuid(uuid)
        for child in children:
            # print child.to_primitive()
            children_ = cls.read_chain(child.uuid, depth + 1, max_depth)
            node = TagNode(child)
            node.children = children_
            nodes.append(node)
        return nodes

    @classmethod
    def read_all(cls):
        with ro_transaction() as session:
            query = cls.Table.select().order_by(cls.Table.c.created_at.asc())
            rows = session.execute(query)
            if rows:
                entities = map(TagMapper.to_entity_from_obj, list(rows))
                return entities
