from __future__ import absolute_import

import ujson as json
from uuid import uuid4

from tornado import gen
from tornado.web import RequestHandler

from services.repositories.tag import TagRepository
from entities import Tag


class TagHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        tags = TagRepository.read_all()
        self.write({'data': [r.to_primitive() for r in tags]})

    @gen.coroutine
    def post(self):
        # import pdb; pdb.set_trace()
        data = json.loads(self.request.body)
        tag = Tag(data)
        tag.validate()
        TagRepository.upsert(tag)
        self.write('OK')
