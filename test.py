from uuid import uuid4

from entities.base import Attribute, Entity, EntityAttribute
from services.repositories.base import AttributeRepository, EntityRepository, EntityAttributeRepository

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

if __name__ == '__main__':
    entity_test()
    
