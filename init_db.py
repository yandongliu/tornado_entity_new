from uuid import uuid4

from entities.base import Attribute, Entity, EntityAttribute
from services.repositories.base import AttributeRepository, EntityRepository, EntityAttributeRepository

def insert_roots():
    _root_uuid = 'b0a026a3-2c46-457a-aa24-6b44fc250c82'
    root_uuid = 'ba578557-5caf-45cd-b2aa-3860d896906e'
    _root = Entity({
        'uuid': _root_uuid,
        'parent_uuid': _root_uuid,
        'type_': '_root',
        'name': '_root',
    })
    _root.validate()
    print _root.to_primitive()
    EntityRepository.upsert(_root)
    root = Entity({
        'uuid': root_uuid,
        'parent_uuid': _root_uuid,
        'type_': 'root',
        'name': 'root',
    })
    EntityRepository.upsert(root)

if __name__ == '__main__':
    insert_roots()
    
