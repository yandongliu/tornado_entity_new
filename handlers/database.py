from __future__ import absolute_import

from uuid import uuid4

from tornado import gen
from tornado.web import RequestHandler

from lib import cache
from services.repositories.item import ItemRepository
from services.repositories.tag import TagRepository
from entities import Tag


class DatabaseHandler(RequestHandler):

    @cache.local_memoize
    @gen.coroutine
    def get(self):
        items = ItemRepository.read_all()
        tags = TagRepository.read_all()
        tags.append(Tag.get_mock_object())
        self.write({'data': [r.to_primitive() for r in tags]})

    @gen.coroutine
    def post(self):
        # import pdb; pdb.set_trace()
        tag_type = self.get_argument('tag_type')
        tag_name = self.get_argument('tag_name')
        tag_uuid = uuid4()
        tag = Tag({
            'uuid': tag_uuid,
            'tag_type': tag_type,
            'tag_name': tag_name,
            'parent_uuid': parent_uuid,
        })
        self.write('OK')
