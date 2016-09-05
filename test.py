import ujson as json
from uuid import uuid4

from entities.base import Attribute, Entity, EntityAttribute, EntityNode
from services.repositories.base import AttributeRepository, EntityRepository, EntityAttributeRepository
from handlers.http_api_entity import NodeHtml

class EntityAttributeTest:

    @staticmethod
    def get():
        entity_uuid = '2dbdfc12-0265-4fa8-b29a-c128123c0755'
        e = EntityRepository.read_one(entity_uuid)
        print e.get_attributes()
        # attrs = EntityRepository.read_attributes(entity_uuid)
        # e.attributes = attrs
        print e.to_primitive()

class AttributeTest:

    @staticmethod
    def inserts():
        attribute = Attribute.get_mock_object()
        attribute.type_ = 'address'
        attribute.name = 'Address'
        print attribute.to_primitive()
        # attribute.entity_uuid = '2dbdfc12-0265-4fa8-b29a-c128123c0755'
        AttributeRepository.upsert(attribute)


    @staticmethod
    def insert_relation():
        ea = EntityAttribute.get_mock_object()
        ea.entity_uuid = '2dbdfc12-0265-4fa8-b29a-c128123c0755'
        ea.attribute_uuid = '24f28076-8d0c-4405-a6b2-2e164520a118'
        print ea.to_primitive()
        EntityAttributeRepository.upsert(ea)


class EntityTest:

    @staticmethod
    def entity_test():
        entity = Entity.get_mock_object()
        entity.parent_uuid = entity.uuid
        EntityRepository.upsert(entity)
        print entity.to_primitive()

        attribute = Attribute.get_mock_object()
        AttributeRepository.upsert(attribute)
        print attribute.to_primitive()

        entity_attribute = EntityAttribute.get_mock_object()
        entity_attribute.entity_uuid = entity.uuid
        entity_attribute.attribute_uuid = attribute.uuid
        EntityAttributeRepository.upsert(entity_attribute)
        print entity_attribute.to_primitive()

    @staticmethod
    def read_by_parent():
        root_uuid = 'b0a026a3-2c46-457a-aa24-6b44fc250c82'
        entities = EntityRepository.read_many_by_parent_uuid(root_uuid)
        for e in entities:
            print e.to_primitive()

    @staticmethod
    def read_chain():
        root_uuid = 'b0a026a3-2c46-457a-aa24-6b44fc250c82'
        nodes = EntityRepository.read_node_chain(root_uuid)
        # import pdb; pdb.set_trace()
        print json.dumps([n.to_primitive() for n in nodes])

    @staticmethod
    def node_html():
        root_uuid = 'b0a026a3-2c46-457a-aa24-6b44fc250c82'
        entity = EntityRepository.read_one(root_uuid)
        nodes = EntityRepository.read_node_chain(root_uuid, max_depth=10)
        node = EntityNode(entity, nodes)
        import pdb; pdb.set_trace()
        print NodeHtml.get_node_html(node)
        # print json.dumps([n.to_primitive() for n in nodes])

    @staticmethod
    def joinload():
        root_uuid = 'b0a026a3-2c46-457a-aa24-6b44fc250c82'
        entity = EntityRepository.read_one(root_uuid)
        print entity.attributes
        # import pdb; pdb.set_trace()
        # print json.dumps([n.to_primitive() for n in nodes])

if __name__ == '__main__':
    # entity_test()
    # EntityTest.read_chain()
    # EntityTest.node_html()
    # EntityTest.joinload()
    # AttributeTest.inserts()
    # AttributeTest.insert_relation()
    EntityAttributeTest.get()
    
