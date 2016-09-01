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
        # import pdb; pdb.set_trace()
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


class DeleteTagHandler(RequestHandler):

    @gen.coroutine
    def get(self, tag_uuid):
        TagRepository.delete(tag_uuid)
        self.write('ok')
