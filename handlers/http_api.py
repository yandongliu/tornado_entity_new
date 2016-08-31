from __future__ import absolute_import

import ujson as json
from uuid import uuid4

from tornado import gen
from tornado.web import RequestHandler

from services.repositories.tag import TagRepository
from entities import Tag


class TagHandler(RequestHandler):

    @gen.coroutine
    def get(self, tag_uuid):
        tag = TagRepository.read_one(tag_uuid)
        if tag:
            self.write({'data': tag.to_primitive()})
        else:
            self.write('404')

    @gen.coroutine
    def post(self):
        # import pdb; pdb.set_trace()
        tag_type = self.get_argument('tag_type')
        tag_name = self.get_argument('tag_name')
        uuid = self.get_argument('uuid')
        parent_uuid = self.get_argument('parent_uuid')
        data = {
            'tag_type': tag_type,
            'tag_name': tag_name,
            'uuid': uuid,
            'parent_uuid': parent_uuid,
        }
        tag = Tag(data)
        tag.validate()
        TagRepository.upsert(tag)
        self.write('OK')
