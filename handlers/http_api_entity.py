from __future__ import absolute_import

import ujson as json
from uuid import uuid4

from tornado import gen
from tornado.web import RequestHandler

from entities import Entity, EntityNode
from handlers.base import BaseHandler
from lib.cache import local_memoize
from services.repositories.base import EntityRepository


class NodeHtml(object):
    
    @classmethod
    def get_node_html(cls, node):
        """Generate html to a node"""
        html = ''
        if node is not None:
            html += '<li>'
            html += '{type_} - <a href="{uuid}">{name}</a> || <a href="/http_api/entity/add_sub/{uuid}">add</a> <a href="/http_api/entity/add_attr/{uuid}">add attr</a> <a href="/http_api/entity/edit/{uuid}">edit</a> <a href="/http_api/entity/delete/{uuid}">delete</a> Attrs:{attrs}'.format(
                uuid=node.entity.uuid,
                name=node.entity.name,
                type_=node.entity.type_,
                attrs=node.entity.get_attributes_html(),
            )
            html += cls.get_nodes_html(node.children)

        return html

    @classmethod
    def get_nodes_html(cls, nodes):
        """Generate html to a list of nodes"""
        html = ''
        if nodes:
            html += '<ul>'
            for node in nodes:
                html += cls.get_node_html(node)
            html += '</ul>'

        return html

class ShowHandler(RequestHandler):


    # @local_memoize
    @gen.coroutine
    def get(self, uuid):
        entity = EntityRepository.read_one(uuid)
        html = '<html>'
        html += '<a href="/">HOME</a>'
        if entity:
            nodes = EntityRepository.read_node_chain(uuid, max_depth=10)
            _node = EntityNode(entity, nodes)
            html += NodeHtml.get_node_html(_node)
        html += '</html>'
        self.write(html)

    @gen.coroutine
    def post(self):
        # import pdb; pdb.set_trace()
        type_ = self.get_argument('type_')
        name = self.get_argument('name')
        uuid = self.get_argument('uuid')
        parent_uuid = self.get_argument('parent_uuid')
        data = {
            'type_': type_,
            'name': name,
            'uuid': uuid,
            'parent_uuid': parent_uuid,
        }
        entity = Entity(data)
        EntityRepository.upsert(entity)
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
