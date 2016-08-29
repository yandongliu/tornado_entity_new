from __future__ import absolute_import

from entities.tag import Tag
from .base import EntityMapper


class TagMapper(EntityMapper):
    _entity = Tag

