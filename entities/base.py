import uuid

from schematics.exceptions import ValidationError
from schematics.types import StringType


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
