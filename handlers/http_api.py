from __future__ import absolute_import

import ujson as json
from uuid import uuid4

from tornado import gen
from tornado.web import RequestHandler

from entities import Tag
from handlers.base import BaseHandler
from lib.cache import local_memoize
from services.repositories.tag import TagRepository


class TagHandler(RequestHandler):

    def get_nodes_html(self, tag_nodes):
        html = ''
        if tag_nodes:
            html += '<ul>'
            for node in tag_nodes:
                html += '<li>'
                html += '{type_}/{name} - <a href="{uuid}">{value}</a> <a href="/http_api/add_sub/{uuid}">add</a>'.format(
                    type_=node.tag.tag_type,
                    uuid=node.tag.uuid,
                    name=node.tag.tag_name,
                    value=node.tag.value
                )
                html += self.get_nodes_html(node.children)
            html += '</ul>'

        return html

    # @local_memoize
    @gen.coroutine
    def get(self, tag_uuid):
        self_node = TagRepository.read_one(tag_uuid)
        tag_nodes = TagRepository.read_chain(tag_uuid, max_depth=10)
        html = '<html><ul>'
        if self_node:
            html += '<li>'
            html += '{} - {} - {}'.format(self_node.tag_type, self_node.tag_name, self_node.value)
            html += self.get_nodes_html(tag_nodes)
        html += '</ul></html>'
        self.write(html)

    @gen.coroutine
    def post(self):
        # import pdb; pdb.set_trace()
        tag_type = self.get_argument('tag_type')
        tag_name = self.get_argument('tag_name')
        value = self.get_argument('value')
        uuid = self.get_argument('uuid')
        parent_uuid = self.get_argument('parent_uuid')
        data = {
            'tag_type': tag_type,
            'tag_name': tag_name,
            'value': value,
            'uuid': uuid,
            'parent_uuid': parent_uuid,
        }
        tag = Tag(data)
        TagRepository.upsert(tag)
        self.redirect('/')


class DeleteTagHandler(RequestHandler):

    @gen.coroutine
    def get(self, tag_uuid):
        TagRepository.delete(tag_uuid)
        self.redirect('/')


class EditTagHandler(BaseHandler):

    @gen.coroutine
    def get(self, tag_uuid):
        tag = TagRepository.read_one(tag_uuid)
        self.render("edit.html", title="Edit Node", tag=tag)
 
    @gen.coroutine
    def post(self):
        tag_type = self.get_argument('tag_type')
        tag_name = self.get_argument('tag_name')
        value = self.get_argument('value')
        uuid = self.get_argument('uuid')
        parent_uuid = self.get_argument('parent_uuid')
        data = {
            'tag_type': tag_type,
            'tag_name': tag_name,
            'value': value,
            'uuid': uuid,
            'parent_uuid': parent_uuid,
        }
        tag = Tag(data)
        try:
            TagRepository.upsert(tag)
            self.redirect('/')
        except Exception as ex:
            self.json_response({
                'data': data, 
                'error': str(ex)
            })


class AddSubTagHandler(RequestHandler):

    @gen.coroutine
    def get(self, tag_uuid):
        random_uuid = str(uuid4())
        tag = TagRepository.read_one(tag_uuid)
        self.render("add_sub.html", title="Add a Sub Node", tag=tag, random_uuid=random_uuid)

    @gen.coroutine
    def post(self):
        # import pdb; pdb.set_trace()
        tag_type = self.get_argument('tag_type')
        tag_name = self.get_argument('tag_name')
        value = self.get_argument('value')
        uuid = self.get_argument('uuid')
        parent_uuid = self.get_argument('parent_uuid')
        data = {
            'tag_type': tag_type,
            'tag_name': tag_name,
            'value': value,
            'uuid': uuid,
            'parent_uuid': parent_uuid,
        }
        tag = Tag(data)
        TagRepository.upsert(tag)
        self.redirect('/')
