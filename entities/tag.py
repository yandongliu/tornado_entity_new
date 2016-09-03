from datetime import datetime
import re

from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import DateTimeType, IntType, StringType, UUIDType
from schematics.types.compound import ListType, ModelType

from .base import UuidStringType


p_tag_type = re.compile('^[\d\w_]+$')

class Tag(Model):

    uuid = UUIDType(required=True)
    tag_type = StringType(required=True)
    tag_name = StringType(required=True)
    value = StringType(required=True)
    parent_uuid = UUIDType(required=True)
    created_at = DateTimeType(default=datetime.utcnow, required=True)
 
    def validate(self):
        if not p_tag_type.match(self.tag_type):
            raise ValidationError('Improper tag type')
        super(Tag, self).validate()


class TagNode(Model):

    def __init__(self, tag):
        self.tag = tag
        self.parent = None
        self.children = []

    def add_child(child):
        self.children.append(child)

    def to_primitive(self):
        return {
            'node': self.tag.to_primitive(),
            'children': [child.to_primitive() for child in self.children],
        }
