from datetime import datetime

from schematics.models import Model
from schematics.types import DateTimeType, StringType

from .base import UuidStringType


class User(Model):

    uuid = UuidStringType(required=True)
    email = StringType(required=True)
    passwd = StringType(required=True)
    created_at = DateTimeType(default=datetime.utcnow, required=True)
    updated_at = DateTimeType(default=datetime.utcnow, required=True)
    deleted_at = DateTimeType(default=datetime.utcnow)
