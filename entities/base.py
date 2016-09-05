from datetime import datetime
import uuid

from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import DateTimeType, StringType, UUIDType
from schematics.types.compound import ListType, ModelType


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


class Base(Model):
    """When you want to manage the two timestamps, extend from this class"""

    created_at = DateTimeType(default=datetime.utcnow, required=True)
    updated_at = DateTimeType(default=datetime.utcnow, required=True)


# We let MySQL manage created_at/updated_at
class Attribute(Model):

    uuid = UUIDType(required=True)
    type_ = StringType(required=True)
    name = StringType(required=True)
    regex = StringType(required=False)


class Entity(Model):

    uuid = UUIDType(required=True)
    parent_uuid = UUIDType(required=True)
    type_ = StringType(required=True)
    name = StringType(required=True)

    attributes = ListType(ModelType(Attribute))

    def get_attributes(self):
        return ' '.join(attr.name for attr in self.attributes)

    def get_attributes_html(self):
        s = ''
        for attr in self.attributes:
            s += ' <a href="/http_api/attr/{}">{}</a>'.format(attr.uuid, attr.name)
        return s

class EntityNode(Model):

    def __init__(self, entity, children=None):
        self.entity = entity
        # self.parent = None
        if not children:
            self.children = []
        else:
            self.children = children

    def add_child(node):
        self.children.append(node)

    def to_primitive(self):
        return {
            'node': self.entity.to_primitive(),
            'children': [child.to_primitive() for child in self.children],
        }


class EntityAttribute(Model):

    uuid = UUIDType(required=True)
    entity_uuid = UUIDType(required=True)
    attribute_uuid = UUIDType(required=True)

    entity = ModelType(Entity)
    # attribute = ModelType(Attribute)
