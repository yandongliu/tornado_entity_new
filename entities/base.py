from datetime import datetime
import uuid

from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import DateTimeType, StringType, UUIDType


class UuidStringType(StringType):
    def validate(self, value, context=None):
        try:
            uuid.UUID(value, version=4)
        except ValueError:
            raise ValidationError('Value should be valid UUID, got \'%s\' instead' % value)

    def to_primitive(self, value, context=None):
        return str(value)

    def to_native(self, value, context=None):
        return str(uuid.UUID(value, version=4))

    def _mock(self, context=None):
        return str(uuid.uuid4())


class BaseEntity(Model):

    created_at = DateTimeType(default=datetime.utcnow, required=True)
    updated_at = DateTimeType(default=datetime.utcnow, required=True)


class Entity(BaseEntity):

    uuid = UUIDType(required=True)
    parent_uuid = UUIDType(required=True)
    type_ = StringType(required=True)
    name = StringType(required=True)


class EntityNode(Model):

    def __init__(self, entity):
        self.entity = entity
        self.parent = None
        self.children = []

    def add_child(child):
        self.children.append(child)

    def to_primitive(self):
        return {
            'node': self.entity.to_primitive(),
            'children': [child.to_primitive() for child in self.children],
        }


class Attribute(BaseEntity):

    uuid = UUIDType(required=True)
    type_ = StringType(required=True)
    name = StringType(required=True)
    regex = StringType(required=False)


class EntityAttribute(BaseEntity):

    uuid = UUIDType(required=True)
    entity_uuid = UUIDType(required=True)
    attribute_uuid = UUIDType(required=True)
