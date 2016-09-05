from __future__ import absolute_import

import ujson as json
from uuid import uuid4

from tornado import gen
from tornado.web import RequestHandler

from entities import Attribute, Entity, EntityNode
from handlers.base import BaseHandler
from lib.cache import local_memoize
from services.repositories.base import AttributeRepository


class ShowHandler(RequestHandler):

    @gen.coroutine
    def get(self, uuid):
        attr = AttributeRepository.read_one(uuid)
        html = '<html>'
        html += '<a href="/">HOME</a>'
        html += '<hr/>'
        if attr:
            html += '<form method=POST action="/http_api/attr/">'
            html += '<label>UUID</label> <input name="uuid" type=text value="{}" size=50 />'.format(attr.uuid)
            html += '<br/>'
            html += '<label>type_</label> <input name="type_" type=text value="{}" size=50 />'.format(attr.type_)
            html += '<br/>'
            html += '<label>name</label> <input name="name" type=text value="{}" size=50 />'.format(attr.name)
            html += '<br/>'
            html += '<label>regex</label> <input name="regex" type=text value="{}" size=50 />'.format(attr.regex)
            html += '<br/>'
            html += '<input type=submit />'
            html += '</form>'
        html += '</html>'
        self.write(html)

    @gen.coroutine
    def post(self, uuid=None):
        # import pdb; pdb.set_trace()
        uuid = self.get_argument('uuid')
        type_ = self.get_argument('type_')
        name = self.get_argument('name')
        regex = self.get_argument('regex')
        data = {
            'uuid': uuid,
            'type_': type_,
            'name': name,
            'regex': regex,
        }
        attr = Attribute(data)
        AttributeRepository.upsert(attr)
        self.redirect('/')


class DeleteHandler(RequestHandler):

    @gen.coroutine
    def get(self, uuid):
        EntityRepository.delete(uuid)
        self.redirect('/')


class EditHandler(BaseHandler):

    @gen.coroutine
    def get(self, uuid=None):
        entity = EntityRepository.read_one(uuid)
        if entity:
            self.render("entity/edit.html", title="Edit Node", entity=entity)
        else:
            self.return_404('Entity not found')
 
    @gen.coroutine
    def post(self, uuid=None):
        uuid = self.get_argument('uuid')
        parent_uuid = self.get_argument('parent_uuid')
        type_ = self.get_argument('type_')
        name = self.get_argument('name')
        data = {
            'uuid': uuid,
            'parent_uuid': parent_uuid,
            'type_': type_,
            'name': name,
        }
        entity = Entity(data)
        try:
            EntityRepository.upsert(entity)
            self.redirect('/')
        except Exception as ex:
            self.json_response({
                'data': data, 
                'error': str(ex)
            })


class AddSubHandler(RequestHandler):

    @gen.coroutine
    def get(self, uuid):
        random_uuid = str(uuid4())
        entity = EntityRepository.read_one(uuid)
        self.render("entity/add_sub.html", title="Add a Sub Node", entity=entity, random_uuid=random_uuid)

    @gen.coroutine
    def post(self, uuid):
        # import pdb; pdb.set_trace()
        type_ = self.get_argument('type_')
        name = self.get_argument('name')
        uuid = self.get_argument('uuid')
        parent_uuid = self.get_argument('parent_uuid')
        data = {
            'uuid': uuid,
            'parent_uuid': parent_uuid,
            'type_': type_,
            'name': name,
        }
        entity = Entity(data)
        EntityRepository.upsert(entity)
        self.redirect('/')
