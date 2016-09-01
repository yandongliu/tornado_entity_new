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
        self_node = TagRepository.read_one(tag_uuid)
        tag_nodes = TagRepository.read_chain(tag_uuid)
        if self_node:
            self.write({
                'self': self_node.to_primitive(),
                'children': [node.to_primitive() for node in tag_nodes]
            })
        else:
            self.write('404')

    @gen.coroutine
    def post(self):
        # import pdb; pdb.set_trace()
        data = json.loads(self.request.body)
        tag = Tag(data)
        tag.validate()
        TagRepository.upsert(tag)
        self.write('OK')
