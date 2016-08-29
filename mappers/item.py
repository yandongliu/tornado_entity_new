from __future__ import absolute_import

from entities.item import Item
from .base import EntityMapper


class ItemMapper(EntityMapper):
    _entity = Item

