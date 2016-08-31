from datetime import datetime

from schematics.models import Model
from schematics.types import DateTimeType, IntType, StringType, UUIDType

from .base import UuidStringType


class Tag(Model):

    uuid = UUIDType(required=True)
    tag_type = StringType(required=True)
    tag_name = StringType(required=True)
    parent_uuid = UUIDType(required=True)
    created_at = DateTimeType(default=datetime.utcnow, required=True)
