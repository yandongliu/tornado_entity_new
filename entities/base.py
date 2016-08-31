import uuid

from schematics.exceptions import ValidationError
from schematics.types import StringType


class UuidStringType(StringType):
    # def validate(self, value, context=None):
    def validate(self, value):
        # import pdb; pdb.set_trace()
        try:
            uuid.UUID(value, version=4)
        except ValueError:
            raise ValidationError('Value should be valid UUID, got \'%s\' instead' % value)

    def to_primitive(self, value, context=None):
        # import pdb; pdb.set_trace()
        return str(value)
        # return '123'

    def to_native(self, value, context=None):
        """Convert the UUID value to a string UUID."""
        if isinstance(value, uuid.UUID):
            return str(value)
        try:
            uuid.UUID(value)
        except (TypeError, ValueError):
            raise ConversionError(self.MESSAGES['convert'].format(value))
        return value

    def to_native(self, value, context=None):
        # import pdb; pdb.set_trace()
        return str(uuid.UUID(value, version=4))
        # return uuid.UUID(value, version=4)
        # return '456'

    def _mock(self, context=None):
        return str(uuid.uuid4())
