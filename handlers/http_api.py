from __future__ import absolute_import

import ujson as json
from uuid import uuid4

from tornado import gen
from tornado.web import RequestHandler

from services.repositories.tag import TagRepository
from entities import Tag


class TagHandler(RequestHandler):

    def get_nodes_html(self, tag_nodes):
        html = ''
        if tag_nodes:
            html += '<ul>'
            for node in tag_nodes:
                html += '<li>'
                html += '{type_}/{name} - <a href="{uuid}">{value}</a>'.format(
                    type_=node.tag.tag_type,
                    uuid=node.tag.uuid,
                    name=node.tag.tag_name,
                    value=node.tag.value
                )
                html += self.get_nodes_html(node.children)
            html += '</ul>'

        return html

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
        tag.validate()
        TagRepository.upsert(tag)
        self.redirect('/')


class DeleteTagHandler(RequestHandler):

    @gen.coroutine
    def get(self, tag_uuid):
        TagRepository.delete(tag_uuid)
        self.write('ok')
